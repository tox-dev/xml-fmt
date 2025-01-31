# xml-fmt

[![PyPI](https://img.shields.io/pypi/v/xml-fmt?style=flat-square)](https://pypi.org/project/xml-fmt)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/xml-fmt?style=flat-square)](https://pypi.org/project/xml-fmt)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/xml-fmt?style=flat-square)](https://pypi.org/project/xml-fmt)
[![Downloads](https://static.pepy.tech/badge/xml-fmt/month)](https://pepy.tech/project/xml-fmt)
[![PyPI - License](https://img.shields.io/pypi/l/xml-fmt?style=flat-square)](https://opensource.org/licenses/MIT)
[![check](https://github.com/tox-dev/xml-fmt/actions/workflows/check.yaml/badge.svg)](https://github.com/tox-dev/xml-fmt/actions/workflows/check.yaml)

### Using `xml-fmt` with pre-commit

Add it to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/tox-dev/xml-fmt
  rev: "" # Use the sha / tag you want to point at
  hooks:
    - id: pyproject-fmt
```
