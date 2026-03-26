"""Core NanopubTestSuite connector.

Downloads the nanopub-testsuite archive from GitHub, extracts it to a
temporary directory, and indexes all test entries for programmatic use.
"""

from __future__ import annotations

import io
import re
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path
from typing import Iterator

from rdflib import RDF, URIRef, Dataset

from .models import SigningKeyPair, TestSuiteEntry, TestSuiteSubfolder, TransformTestCase

_GITHUB_ARCHIVE_URL = (
    "https://github.com/Nanopublication/nanopub-testsuite/archive/{ref}.tar.gz"
)

_SUBFOLDER_MAP: dict[str, TestSuiteSubfolder] = {sf.value: sf for sf in TestSuiteSubfolder}


class NanopubTestSuite:
    """Programmatic accessor for the Nanopublication Test Suite.

    Typical usage::

        from nanopub_testsuite_connector import NanopubTestSuite

        suite = NanopubTestSuite.get_latest()
        for entry in suite.get_valid(TestSuiteSubfolder.PLAIN):
            print(entry.name, entry.path)

    The constructor is not meant to be called directly — use the
    class-method factories :py:meth:`get_latest` or
    :py:meth:`get_at_commit`.
    """

    # ------------------------------------------------------------------ #
    # Factories                                                            #
    # ------------------------------------------------------------------ #

    @classmethod
    def get_latest(cls) -> "NanopubTestSuite":
        """Download and load the *latest* test suite (``main`` branch).

        Returns:
            A fully-initialized :class:`NanopubTestSuite` instance.
        """
        return cls._load(ref="main")

    @classmethod
    def get_at_commit(cls, commit_sha: str) -> "NanopubTestSuite":
        """Download and load the test suite at a specific commit SHA.

        Args:
            commit_sha: Full or abbreviated commit SHA on the ``main`` branch.

        Returns:
            A fully-initialized :class:`NanopubTestSuite` instance.
        """
        return cls._load(ref=commit_sha)

    # ------------------------------------------------------------------ #
    # Internal init                                                        #
    # ------------------------------------------------------------------ #

    def __init__(
            self,
            root: Path,
            version: str,
            valid_entries: list[TestSuiteEntry],
            invalid_entries: list[TestSuiteEntry],
            transform_cases: list[TransformTestCase],
            signing_keys: dict[str, SigningKeyPair],
    ) -> None:
        self._root = root
        self._version = version
        self._valid: list[TestSuiteEntry] = valid_entries
        self._invalid: list[TestSuiteEntry] = invalid_entries
        self._transform_cases: list[TransformTestCase] = transform_cases
        self._signing_keys: dict[str, SigningKeyPair] = signing_keys

        # Build lookup indices
        self._by_artifact_code: dict[str, TestSuiteEntry] = {}
        self._by_nanopub_uri: dict[str, TestSuiteEntry] = {}
        for entry in (*self._valid, *self._invalid):
            if entry.valid and entry.subfolder == TestSuiteSubfolder.SIGNED:
                code = _artifact_code_from_nanopub(entry.path)
                if code:
                    self._by_artifact_code[code] = entry
            uri = _nanopub_uri_from_nanopub(entry.path)
            if uri:
                self._by_nanopub_uri[uri] = entry

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    @property
    def version(self) -> str:
        """Git ref (branch name or commit SHA) used to fetch this suite."""
        return self._version

    @property
    def root(self) -> Path:
        """Temporary directory that holds the extracted archive."""
        return self._root

    # --- valid / invalid ---

    def get_valid(
            self,
            subfolder: TestSuiteSubfolder | None = None,
    ) -> list[TestSuiteEntry]:
        """Return all *valid* test entries, optionally filtered by subfolder.

        Args:
            subfolder: When given, only entries from that subfolder are
                       returned (``PLAIN``, ``SIGNED``, or ``TRUSTY``).

        Returns:
            A list of :class:`~nanopub_testsuite_connector.TestSuiteEntry`.
        """
        return self._filter(self._valid, subfolder)

    def get_invalid(
            self,
            subfolder: TestSuiteSubfolder | None = None,
    ) -> list[TestSuiteEntry]:
        """Return all *invalid* test entries, optionally filtered by subfolder.

        Args:
            subfolder: When given, only entries from that subfolder are
                       returned (``PLAIN``, ``SIGNED``, or ``TRUSTY``).

        Returns:
            A list of :class:`~nanopub_testsuite_connector.TestSuiteEntry`.
        """
        return self._filter(self._invalid, subfolder)

    # --- transforms ---

    def get_transform_cases(
            self,
            key_name: str | None = None,
    ) -> list[TransformTestCase]:
        """Return transform test cases, optionally filtered by signing key.

        Args:
            key_name: When given (e.g. ``"rsa-key1"``), only cases that
                      use that key are returned.

        Returns:
            A list of :class:`~nanopub_testsuite_connector.TransformTestCase`.
        """
        if key_name is None:
            return list(self._transform_cases)
        return [tc for tc in self._transform_cases if tc.key_name == key_name]

    # --- signing keys ---

    def get_signing_key(self, key_name: str) -> SigningKeyPair:
        """Return the signing key pair for the given key name.

        Args:
            key_name: Key directory name (e.g. ``"rsa-key1"``).

        Returns:
            A :class:`~nanopub_testsuite_connector.SigningKeyPair`.

        Raises:
            KeyError: If *key_name* was not found in the suite.
        """
        try:
            return self._signing_keys[key_name]
        except KeyError:
            available = ", ".join(sorted(self._signing_keys))
            raise KeyError(
                f"Signing key {key_name!r} not found. Available: {available}"
            ) from None

    # --- lookups ---

    def get_by_artifact_code(self, code: str) -> TestSuiteEntry:
        """Look up an entry by its Trusty URI artifact code.

        Args:
            code: The artifact code portion of the Trusty URI
                  (e.g. ``"RA1sViVmXf-W2aZW4Qk74KTaiD9gpLBPe2LhMsinHKKz8"``).

        Returns:
            The matching :class:`~nanopub_testsuite_connector.TestSuiteEntry`.

        Raises:
            KeyError: If no entry matches *code*.
        """
        try:
            return self._by_artifact_code[code]
        except KeyError:
            raise KeyError(f"No entry found for artifact code {code!r}") from None

    def get_by_nanopub_uri(self, uri: str) -> TestSuiteEntry:
        """Look up an entry by its full nanopublication URI.

        Args:
            uri: Full nanopub URI
                 (e.g. ``"http://purl.org/np/RAPPdsJK..."``).

        Returns:
            The matching :class:`~nanopub_testsuite_connector.TestSuiteEntry`.

        Raises:
            KeyError: If no entry matches *uri*.
        """
        try:
            return self._by_nanopub_uri[uri]
        except KeyError:
            raise KeyError(f"No entry found for nanopub URI {uri!r}") from None

    # --- iteration helpers ---

    def __iter__(self) -> Iterator[TestSuiteEntry]:
        """Iterate over *all* entries (valid + invalid)."""
        return iter([*self._valid, *self._invalid])

    def __repr__(self) -> str:
        return (
            f"NanopubTestSuite(version={self._version!r}, "
            f"valid={len(self._valid)}, invalid={len(self._invalid)}, "
            f"transforms={len(self._transform_cases)})"
        )

    # ------------------------------------------------------------------ #
    # Private helpers                                                      #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _filter(
            entries: list[TestSuiteEntry],
            subfolder: TestSuiteSubfolder | None,
    ) -> list[TestSuiteEntry]:
        if subfolder is None:
            return list(entries)
        return [e for e in entries if e.subfolder == subfolder]

    @classmethod
    def _load(cls, ref: str) -> "NanopubTestSuite":
        url = _GITHUB_ARCHIVE_URL.format(ref=ref)
        data = _download(url)
        tmpdir = tempfile.mkdtemp(prefix="nanopub-testsuite-")
        root = Path(tmpdir)
        _extract_tar(data, root)

        # GitHub wraps contents in a top-level directory like
        # ``nanopub-testsuite-<sha>/``.  Find it.
        subdirs = [p for p in root.iterdir() if p.is_dir()]
        if len(subdirs) == 1:
            root = subdirs[0]

        valid_entries = _index_entries(root / "valid", valid=True)
        invalid_entries = _index_entries(root / "invalid", valid=False)
        transform_cases, signing_keys = _index_transforms(root / "transform")

        return cls(
            root=root,
            version=ref,
            valid_entries=valid_entries,
            invalid_entries=invalid_entries,
            transform_cases=transform_cases,
            signing_keys=signing_keys,
        )


# ------------------------------------------------------------------ #
# Module-level helpers                                                #
# ------------------------------------------------------------------ #


def _download(url: str) -> bytes:
    """Fetch *url* and return its content as bytes."""
    with urllib.request.urlopen(url) as resp:  # noqa: S310
        return resp.read()


def _extract_tar(data: bytes, dest: Path) -> None:
    """Extract a gzipped tarball from *data* into *dest*."""
    extract_kwargs = {"path": dest}
    if sys.version_info >= (3, 12):
        extract_kwargs["filter"] = "data"

    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
        tf.extractall(**extract_kwargs)


def _index_entries(base: Path, *, valid: bool) -> list[TestSuiteEntry]:
    """Walk *base* (``valid/`` or ``invalid/``) and build entry list."""
    if not base.exists():
        return []
    entries: list[TestSuiteEntry] = []
    for sub_path in sorted(base.iterdir()):
        if not sub_path.is_dir():
            continue
        sf = _SUBFOLDER_MAP.get(sub_path.name)
        if sf is None:
            continue
        for file_path in sorted(sub_path.glob("*.trig")):
            entries.append(
                TestSuiteEntry(
                    name=file_path.name,
                    path=file_path,
                    subfolder=sf,
                    valid=valid,
                )
            )
    return entries


def _index_transforms(
        transform_dir: Path,
) -> tuple[list[TransformTestCase], dict[str, SigningKeyPair]]:
    """Parse the ``transform/`` directory into cases and key pairs."""
    if not transform_dir.exists():
        return [], {}

    plain_dir = transform_dir / "plain"
    plain_entries: dict[str, TestSuiteEntry] = {}
    if plain_dir.exists():
        for p in sorted(plain_dir.glob("*.in.trig")):
            entry = TestSuiteEntry(
                name=p.name,
                path=p,
                subfolder=TestSuiteSubfolder.PLAIN,
                valid=True,
            )
            base = p.stem[:-3] if p.stem.endswith(".in") else p.stem
            plain_entries[base] = entry

    cases: list[TransformTestCase] = []
    signing_keys: dict[str, SigningKeyPair] = {}

    signed_dir = transform_dir / "signed"
    if not signed_dir.exists():
        return cases, signing_keys

    for key_dir in sorted(signed_dir.iterdir()):
        if not key_dir.is_dir():
            continue
        key_name = key_dir.name

        # Collect signing key pair
        key_subdir = key_dir / "key"
        private_key_path = key_subdir / "id_rsa"
        public_key_path = key_subdir / "id_rsa.pub"

        if private_key_path.exists() and public_key_path.exists():
            signing_keys[key_name] = SigningKeyPair(
                name=key_name,
                private_key=private_key_path,
                public_key=public_key_path,
            )

        # Pair each signed nanopub with its plain counterpart
        for signed_file in sorted(key_dir.glob("*.out.trig")):
            stem = signed_file.stem
            base_stem = stem[:-4] if stem.endswith(".out") else stem
            plain_entry = plain_entries.get(base_stem)
            if plain_entry is None:
                continue

            signed_entry = TestSuiteEntry(
                name=signed_file.name,
                path=signed_file,
                subfolder=TestSuiteSubfolder.SIGNED,
                valid=True,
            )

            out_code_file = signed_file.with_name(base_stem + ".out.code")
            out_code: str | None = None
            if out_code_file.exists():
                out_code = out_code_file.read_text(encoding="utf-8").strip()

            cases.append(
                TransformTestCase(
                    key_name=key_name,
                    plain=plain_entry,
                    signed=signed_entry,
                    out_code=out_code,
                )
            )

    return cases, signing_keys


# ------------------------------------------------------------------ #
# Nanopub URI / artifact code extraction                              #
# ------------------------------------------------------------------ #

_TRUSTY_CODE_RE = re.compile(r"RA[A-Za-z0-9_\-]{40,}")
_NANOPUB_URI_RE = re.compile(r"http(?:s)?://[^\s<>\"]+/np/R[A-Za-z0-9_\-]{40,}")


def _artifact_code_from_nanopub(path: Path) -> str | None:
    """Opens the file and extracts the artifact code (trusty code) of the nanopub"""
    print(path)
    try:
        ds = Dataset()
        ds.parse(path, format="trig")
        # Search across all named/default graphs
        for subject, _, _, _ in ds.quads((None, RDF.type, URIRef("http://www.nanopub.org/nschema#Nanopublication"), None)):
            if isinstance(subject, URIRef):
                uri = str(subject)
                m = _TRUSTY_CODE_RE.search(uri)
                if m:
                    return m.group(0)
    except Exception:
        # Keep the same fail-soft behavior as before
        pass
    return None


def _nanopub_uri_from_nanopub(path: Path) -> str | None:
    """Opens the file and searches for a nanopublication URI in the RDF content."""
    try:
        ds = Dataset()
        ds.parse(path, format="trig")

        # Search across all named/default graphs
        for subject, _, _, _ in ds.quads((None, RDF.type, URIRef("http://www.nanopub.org/nschema#Nanopublication"), None)):
            if isinstance(subject, URIRef):
                return str(subject)
    except Exception:
        # Keep the same fail-soft behavior as before
        pass
    return None
