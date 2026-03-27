[![Tests](https://github.com/Nanopublication/nanopub-testsuite-connector-py/actions/workflows/test.yml/badge.svg)](https://github.com/Nanopublication/nanopub-testsuite-connector-py/actions/workflows/test.yml)
[![semantic-release: angular](https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release)](https://github.com/semantic-release/semantic-release)

# Nanopublication Test Suite Connector — Python

A Python connector that downloads and exposes the
[Nanopublication Test Suite](https://github.com/nanopublication/nanopub-testsuite)
contents for programmatic use.

This package provides a lightweight, **zero-dependency** API to fetch the
official Nanopub Test Suite from GitHub (as a `.tar.gz` archive), extract it
locally, and index test cases so other code can easily consume valid/invalid
test nanopublications, transform test cases, and signing keys.

---

## Table of contents

- [Installation](#installation)
- [Quick examples](#quick-examples)
- [API overview](#api-overview)
- [Notes & troubleshooting](#notes--troubleshooting)

---

## Installation

```bash
pip install nanopub-testsuite-connector
```

Or add it to your project's test dependencies:

**`pyproject.toml`**

```toml
[dependency-groups]
test = [
    "nanopub-testsuite-connector>=1.0.0",
]
```

---

## Quick examples

### Load the latest suite and list all valid PLAIN entries

```python
from nanopub_testsuite_connector import NanopubTestSuite, TestSuiteSubfolder

suite = NanopubTestSuite.get_latest()
for entry in suite.get_valid(TestSuiteSubfolder.PLAIN):
    print(entry.name, "->", entry.path)
```

### Load the testsuite at a specific commit

```python
suite = NanopubTestSuite.get_at_commit("a1b2c3d")
print("Loaded testsuite version:", suite.version)
```

### Look up an entry by artifact code or nanopub URI

```python
suite = NanopubTestSuite.get_latest()

entry = suite.get_by_artifact_code("RA1sViVmXf-W2aZW4Qk74KTaiD9gpLBPe2LhMsinHKKz8")
print("Entry for artifact code:", entry.name)

entry = suite.get_by_nanopub_uri("http://purl.org/np/RAPPdsJKoVVp7KZTjdS3D2MvxfkNa-G4JDrnLjeMQFwnY")
print("Entry for URI:", entry.name)
```

### Access transform cases for a named signing key

```python
for tc in suite.get_transform_cases("rsa-key1"):
    print(tc.plain.name, "->", tc.signed.name, "| expected code:", tc.out_code)
```

### Read a signing key pair

```python
kp = suite.get_signing_key("rsa-key1")
print("Private key path:", kp.private_key)
print("Public key path: ", kp.public_key)
```

### Use entries in pytest

```python
import pytest
from nanopub_testsuite_connector import NanopubTestSuite, TestSuiteSubfolder


@pytest.fixture(scope="session")
def testsuite():
    return NanopubTestSuite.get_latest()


@pytest.mark.parametrize(
    "entry",
    NanopubTestSuite.get_latest().get_valid(TestSuiteSubfolder.PLAIN),
    ids=lambda e: e.name,
)
def test_valid_plain(entry):
    content = entry.read_text()
    assert "@prefix" in content
```

---

## API overview

### `NanopubTestSuite`

| Method / property                     | Description                                  |
|---------------------------------------|----------------------------------------------|
| `NanopubTestSuite.get_latest()`       | Download & load the `main` branch.           |
| `NanopubTestSuite.get_at_commit(sha)` | Download & load a specific commit SHA.       |
| `suite.version`                       | Git ref used when fetching this instance.    |
| `suite.root`                          | `Path` to the extracted temporary directory. |
| `suite.get_valid()`                   | All valid `TestSuiteEntry` instances.        |
| `suite.get_valid(subfolder)`          | Filter by `PLAIN`, `SIGNED`, or `TRUSTY`.    |
| `suite.get_invalid()`                 | All invalid `TestSuiteEntry` instances.      |
| `suite.get_invalid(subfolder)`        | Filter by `PLAIN`, `SIGNED`, or `TRUSTY`.    |
| `suite.get_transform_cases()`         | All `TransformTestCase` instances.           |
| `suite.get_transform_cases(key_name)` | Filter by signing key (e.g. `"rsa-key1"`).   |
| `suite.get_signing_key(key_name)`     | Returns a `SigningKeyPair`.                  |
| `suite.get_by_artifact_code(code)`    | Lookup by Trusty URI artifact code.          |
| `suite.get_by_nanopub_uri(uri)`       | Lookup by full nanopub URI.                  |
| `iter(suite)`                         | Iterate over all entries (valid + invalid).  |

### `TestSuiteEntry`

| Attribute      | Type                 | Description                                          |
|----------------|----------------------|------------------------------------------------------|
| `name`         | `str`                | Filename (e.g. `nanopub1.trig`).                     |
| `path`         | `Path`               | Absolute path to the extracted file.                 |
| `subfolder`    | `TestSuiteSubfolder` | `PLAIN`, `SIGNED`, or `TRUSTY`.                      |
| `valid`        | `bool`               | `True` if from `valid/`, `False` if from `invalid/`. |
| `read_text()`  | `str`                | Full file content as a string.                       |
| `read_bytes()` | `bytes`              | Raw file bytes.                                      |

### `TestSuiteSubfolder`

```python
class TestSuiteSubfolder(str, Enum):
    PLAIN = "plain"
    SIGNED = "signed"
    TRUSTY = "trusty"
```

### `TransformTestCase`

| Attribute  | Type             | Description                                          |
|------------|------------------|------------------------------------------------------|
| `key_name` | `str`            | Signing key used (e.g. `rsa-key1`).                  |
| `plain`    | `TestSuiteEntry` | Input nanopub (from `transform/plain`).              |
| `signed`   | `TestSuiteEntry` | Expected output (from `transform/signed/<key>`).     |
| `out_code` | `str \| None`    | Expected artifact code from `*.out.code`, or `None`. |

### `SigningKeyPair`

| Attribute     | Type   | Description                           |
|---------------|--------|---------------------------------------|
| `name`        | `str`  | Key directory name (e.g. `rsa-key1`). |
| `private_key` | `Path` | Path to the private key file.         |
| `public_key`  | `Path` | Path to the public key file.          |

---

## Notes & troubleshooting

- The connector downloads GitHub tarballs (`archive/<ref>.tar.gz`).
  An internet connection is required when fetching a new version or commit.
- Downloaded data is extracted into a temporary directory created with
  `tempfile.mkdtemp`. The directory persists for the lifetime of your process.
  Clean it up manually via `suite.root.parent` if needed.
- If extraction fails, ensure your environment allows outgoing HTTPS traffic.

---

## License

[MIT](LICENSE)
