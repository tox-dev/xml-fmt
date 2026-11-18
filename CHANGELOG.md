# Changelog

<!-- towncrier release notes start -->

<a name="release-1-2-3"></a>

## 1.2.3 (2026-11-18)

<a name="release-1-2-3-documentation"></a>

### Documentation

- Clarify that external DTD references are not fetched, while entity declarations are rejected
  ([#157](https://github.com/tox-dev/xml-fmt/pull/157)) by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-1-2-3-security"></a>

### Security

- Reject XML entity declarations before formatting untrusted files ([#155](https://github.com/tox-dev/xml-fmt/pull/155))
  by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-1-2-3-packaging"></a>

### Packaging

- Every wheel now carries a [PEP 770](https://peps.python.org/pep-0770/) CycloneDX SBOM in its `.dist-info/sboms`
  directory, written at build time by [python-sbom](https://github.com/tox-dev/python-sbom)
  ([#152](https://github.com/tox-dev/xml-fmt/pull/152)) by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-1-2-2"></a>

## 1.2.2 (2026-11-04)

<a name="release-1-2-1"></a>

## 1.2.1 (2026-10-27)

<a name="release-1-2-1-fixed"></a>

### Fixed

- Fix repository links in the PyPI project description ([#127](https://github.com/tox-dev/xml-fmt/pull/127)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-1-2-1-packaging"></a>

### Packaging

- Include the tox configuration in source distributions ([#127](https://github.com/tox-dev/xml-fmt/pull/127)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-1-2-0"></a>

## 1.2.0 (2026-10-10)

<a name="release-1-2-0-added"></a>

### Added

- Require Python 3.11 ([#120](https://github.com/tox-dev/xml-fmt/pull/120)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-1-1-0"></a>

## 1.1.0 (2026-10-01)

<a name="release-1-1-0-added"></a>

### Added

- Add Python 3.14 and 3.15 support ([#117](https://github.com/tox-dev/xml-fmt/pull/117)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-1-0-2"></a>

## 1.0.2 (2026-07-07)

<a name="release-1-0-2-fixed"></a>

### Fixed

- Fix the pre-commit hook file matching ([#9](https://github.com/tox-dev/xml-fmt/pull/9)) by
  [@jevinskie](https://github.com/jevinskie).

<a name="release-1-0-1"></a>

## 1.0.1 (2025-01-31)

<a name="release-1-0-1-documentation"></a>

### Documentation

- Correct the README's pre-commit hook ID from `pyproject-fmt` to `xml-fmt` by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-1-0-0"></a>

## 1.0.0 (2025-01-31)

<a name="release-1-0-0-added"></a>

### Added

- Publish the first version of the XML formatter ([#1](https://github.com/tox-dev/xml-fmt/pull/1)) by
  [@gaborbernat](https://github.com/gaborbernat).
