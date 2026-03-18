"""Data models for the Nanopublication Test Suite Connector."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class TestSuiteSubfolder(str, Enum):
    """Subfolder categories within valid/invalid test entries."""
    __test__ = False

    PLAIN = "plain"
    SIGNED = "signed"
    TRUSTY = "trusty"


@dataclass(frozen=True)
class TestSuiteEntry:
    """Represents a single nanopublication test file in the test suite.

    Attributes:
        name:       Filename (e.g. ``nanopub1.trig``).
        path:       Absolute path to the extracted file.
        subfolder:  Which category this entry belongs to.
        valid:      ``True`` if this entry lives under ``valid/``,
                    ``False`` if it lives under ``invalid/``.
    """
    __test__ = False

    name: str
    path: Path
    subfolder: TestSuiteSubfolder
    valid: bool

    def read_text(self, encoding: str = "utf-8") -> str:
        """Return the full content of the test file as a string."""
        return self.path.read_text(encoding=encoding)

    def read_bytes(self) -> bytes:
        """Return the raw bytes of the test file."""
        return self.path.read_bytes()


@dataclass(frozen=True)
class SigningKeyPair:
    """Paths to a private/public RSA key pair used in transform test cases.

    Attributes:
        name:        Key name (e.g. ``rsa-key1``).
        private_key: Path to the private key PEM file.
        public_key:  Path to the public key PEM file.
    """

    name: str
    private_key: Path
    public_key: Path


@dataclass(frozen=True)
class TransformTestCase:
    """Pairs a plain nanopub with its expected signed/trusty output.

    Attributes:
        key_name:   Signing key used for this transform (e.g. ``rsa-key1``).
        plain:      The input ``TestSuiteEntry`` (from ``transform/plain``).
        signed:     The expected signed ``TestSuiteEntry``
                    (from ``transform/signed/<key_name>``).
        out_code:   Expected artifact code string read from the
                    ``*.out.code`` file, or ``None`` if not present.
    """

    key_name: str
    plain: TestSuiteEntry
    signed: TestSuiteEntry
    out_code: str | None
