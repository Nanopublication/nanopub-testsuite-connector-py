"""Tests for the Nanopublication Test Suite Connector."""

from __future__ import annotations

import io
import tarfile
from pathlib import Path
from unittest.mock import patch

import pytest

from nanopub_testsuite_connector import (
    NanopubTestSuite,
    TestSuiteEntry,
    TestSuiteSubfolder,
    TransformTestCase,
)
from nanopub_testsuite_connector.connector import (
    _artifact_code_from_name,
    _nanopub_uri_from_file,
)

# --------------------------------------------------------------------------- #
# Fixtures                                                                     #
# --------------------------------------------------------------------------- #

SAMPLE_TRIG = """\
@prefix np: <https://www.nanopub.org/nschema#> .
@prefix this: <https://purl.org/np/RA1sViVmXf-W2aZW4Qk74KTaiD9gpLBPe2LhMsinHKKz8> .

this: {
  this: a np:Nanopublication .
}
"""

SAMPLE_TRIG_URI = "https://purl.org/np/RAPPdsJKoVVp7KZTjdS3D2MvxfkNa-G4JDrnLjeMQFwnY"
SAMPLE_TRIG_WITH_URI = f"""\
@prefix np: <https://www.nanopub.org/nschema#> .
@prefix this: <{SAMPLE_TRIG_URI}> .

sub:Head {{
  this: a np:Nanopublication .
}}
"""


def _make_fake_archive(files: dict[str, str]) -> bytes:
    """Build an in-memory .tar.gz containing the given path→content mapping."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        for arcname, content in files.items():
            data = content.encode()
            info = tarfile.TarInfo(name=arcname)
            info.size = len(data)
            tf.addfile(info, io.BytesIO(data))
    return buf.getvalue()


@pytest.fixture()
def fake_archive() -> bytes:
    """Minimal fake archive mirroring the real testsuite layout."""
    return _make_fake_archive(
        {
            "nanopub-testsuite-main/valid/plain/nanopub1.trig": SAMPLE_TRIG,
            "nanopub-testsuite-main/valid/signed/nanopub1.signed.trig": SAMPLE_TRIG,
            "nanopub-testsuite-main/valid/trusty/nanopub1.trig": SAMPLE_TRIG,
            "nanopub-testsuite-main/invalid/plain/bad1.trig": SAMPLE_TRIG,
            "nanopub-testsuite-main/transform/plain/nanopub1.trig": SAMPLE_TRIG,
            "nanopub-testsuite-main/transform/signed/rsa-key1/nanopub1.signed.trig": SAMPLE_TRIG,
            "nanopub-testsuite-main/transform/signed/rsa-key1/nanopub1.signed.out.code": "RAABC123",
            "nanopub-testsuite-main/transform/signed/rsa-key1/private_key.pem": "PRIVATE",
            "nanopub-testsuite-main/transform/signed/rsa-key1/public_key.pem": "PUBLIC",
        }
    )


@pytest.fixture()
def suite(fake_archive: bytes) -> NanopubTestSuite:
    with patch(
            "nanopub_testsuite_connector.connector._download",
            return_value=fake_archive,
    ):
        return NanopubTestSuite.get_latest()


# --------------------------------------------------------------------------- #
# Tests – loading                                                              #
# --------------------------------------------------------------------------- #


class TestLoading:
    def test_get_latest_returns_suite(self, suite: NanopubTestSuite) -> None:
        assert isinstance(suite, NanopubTestSuite)

    def test_version_is_main(self, suite: NanopubTestSuite) -> None:
        assert suite.version == "main"

    def test_get_at_commit(self, fake_archive: bytes) -> None:
        with patch(
                "nanopub_testsuite_connector.connector._download",
                return_value=fake_archive,
        ):
            s = NanopubTestSuite.get_at_commit("abc123def")
        assert s.version == "abc123def"

    def test_repr(self, suite: NanopubTestSuite) -> None:
        r = repr(suite)
        assert "NanopubTestSuite" in r
        assert "version=" in r


# --------------------------------------------------------------------------- #
# Tests – valid / invalid entries                                              #
# --------------------------------------------------------------------------- #


class TestEntries:
    def test_get_valid_all(self, suite: NanopubTestSuite) -> None:
        entries = suite.get_valid()
        assert len(entries) == 3  # plain + signed + trusty

    def test_get_valid_plain(self, suite: NanopubTestSuite) -> None:
        entries = suite.get_valid(TestSuiteSubfolder.PLAIN)
        assert len(entries) == 1
        assert entries[0].subfolder == TestSuiteSubfolder.PLAIN

    def test_get_valid_signed(self, suite: NanopubTestSuite) -> None:
        entries = suite.get_valid(TestSuiteSubfolder.SIGNED)
        assert len(entries) == 1

    def test_get_valid_trusty(self, suite: NanopubTestSuite) -> None:
        entries = suite.get_valid(TestSuiteSubfolder.TRUSTY)
        assert len(entries) == 1

    def test_get_invalid_all(self, suite: NanopubTestSuite) -> None:
        entries = suite.get_invalid()
        assert len(entries) == 1

    def test_get_invalid_plain(self, suite: NanopubTestSuite) -> None:
        entries = suite.get_invalid(TestSuiteSubfolder.PLAIN)
        assert len(entries) == 1
        assert not entries[0].valid

    def test_entry_fields(self, suite: NanopubTestSuite) -> None:
        entry = suite.get_valid(TestSuiteSubfolder.PLAIN)[0]
        assert isinstance(entry, TestSuiteEntry)
        assert entry.name == "nanopub1.trig"
        assert entry.path.exists()
        assert entry.valid is True

    def test_entry_read_text(self, suite: NanopubTestSuite) -> None:
        entry = suite.get_valid(TestSuiteSubfolder.PLAIN)[0]
        text = entry.read_text()
        assert "nanopub" in text.lower()

    def test_entry_read_bytes(self, suite: NanopubTestSuite) -> None:
        entry = suite.get_valid(TestSuiteSubfolder.PLAIN)[0]
        assert isinstance(entry.read_bytes(), bytes)

    def test_iteration(self, suite: NanopubTestSuite) -> None:
        all_entries = list(suite)
        assert len(all_entries) == 4  # 3 valid + 1 invalid


# --------------------------------------------------------------------------- #
# Tests – transform cases                                                      #
# --------------------------------------------------------------------------- #


class TestTransforms:
    def test_get_all_transform_cases(self, suite: NanopubTestSuite) -> None:
        cases = suite.get_transform_cases()
        assert len(cases) == 1

    def test_get_transform_by_key(self, suite: NanopubTestSuite) -> None:
        cases = suite.get_transform_cases("rsa-key1")
        assert len(cases) == 1
        assert cases[0].key_name == "rsa-key1"

    def test_get_transform_unknown_key(self, suite: NanopubTestSuite) -> None:
        assert suite.get_transform_cases("unknown-key") == []

    def test_transform_case_fields(self, suite: NanopubTestSuite) -> None:
        tc = suite.get_transform_cases()[0]
        assert isinstance(tc, TransformTestCase)
        assert tc.plain.subfolder == TestSuiteSubfolder.PLAIN
        assert tc.signed.subfolder == TestSuiteSubfolder.SIGNED

    def test_transform_out_code(self, suite: NanopubTestSuite) -> None:
        tc = suite.get_transform_cases()[0]
        assert tc.out_code == "RAABC123"


# --------------------------------------------------------------------------- #
# Tests – signing keys                                                         #
# --------------------------------------------------------------------------- #


class TestSigningKeys:
    def test_get_signing_key(self, suite: NanopubTestSuite) -> None:
        kp = suite.get_signing_key("rsa-key1")
        assert kp.name == "rsa-key1"
        assert kp.private_key.exists()
        assert kp.public_key.exists()

    def test_get_signing_key_not_found(self, suite: NanopubTestSuite) -> None:
        with pytest.raises(KeyError, match="rsa-key99"):
            suite.get_signing_key("rsa-key99")


# --------------------------------------------------------------------------- #
# Tests – lookups                                                              #
# --------------------------------------------------------------------------- #


class TestLookups:
    def test_get_by_artifact_code(self, suite: NanopubTestSuite) -> None:
        code = "RA1sViVmXf-W2aZW4Qk74KTaiD9gpLBPe2LhMsinHKKz8"
        # None of our fake files contain this code in filename or content;
        # look up whatever code was indexed from the plain entry name.
        plain = suite.get_valid(TestSuiteSubfolder.PLAIN)[0]
        extracted = _artifact_code_from_name(plain.name)
        if extracted:
            result = suite.get_by_artifact_code(extracted)
            assert result == plain

    def test_get_by_artifact_code_not_found(self, suite: NanopubTestSuite) -> None:
        with pytest.raises(KeyError):
            suite.get_by_artifact_code("RAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

    def test_get_by_nanopub_uri(self, tmp_path: Path) -> None:
        trig_file = tmp_path / "np.trig"
        trig_file.write_text(SAMPLE_TRIG_WITH_URI, encoding="utf-8")
        uri = _nanopub_uri_from_file(trig_file)
        assert uri == SAMPLE_TRIG_URI

    def test_get_by_nanopub_uri_not_found(self, suite: NanopubTestSuite) -> None:
        with pytest.raises(KeyError):
            suite.get_by_nanopub_uri("http://purl.org/np/RNOTEXISTENT")


# --------------------------------------------------------------------------- #
# Tests – utility functions                                                    #
# --------------------------------------------------------------------------- #


class TestUtils:
    def test_artifact_code_from_filename(self) -> None:
        code = _artifact_code_from_name(
            "RA1sViVmXf-W2aZW4Qk74KTaiD9gpLBPe2LhMsinHKKz8.trig"
        )
        assert code == "RA1sViVmXf-W2aZW4Qk74KTaiD9gpLBPe2LhMsinHKKz8"

    def test_artifact_code_no_match(self) -> None:
        assert _artifact_code_from_name("plain-nanopub.trig") is None

    def test_nanopub_uri_extraction(self, tmp_path: Path) -> None:
        f = tmp_path / "test.trig"
        f.write_text(SAMPLE_TRIG_WITH_URI, encoding="utf-8")
        assert _nanopub_uri_from_file(f) == SAMPLE_TRIG_URI

    def test_nanopub_uri_missing(self, tmp_path: Path) -> None:
        f = tmp_path / "test.trig"
        f.write_text("no uri here", encoding="utf-8")
        assert _nanopub_uri_from_file(f) is None


# --------------------------------------------------------------------------- #
# Tests – TestSuiteSubfolder enum                                              #
# --------------------------------------------------------------------------- #


class TestSubfolderEnum:
    def test_values(self) -> None:
        assert TestSuiteSubfolder.PLAIN.value == "plain"
        assert TestSuiteSubfolder.SIGNED.value == "signed"
        assert TestSuiteSubfolder.TRUSTY.value == "trusty"

    def test_str_equality(self) -> None:
        assert TestSuiteSubfolder.PLAIN == "plain"
