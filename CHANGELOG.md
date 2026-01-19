# Changelog

All notable changes to this project will be documented in this file. See [commitizen](https://github.com/commitizen/cz-cli) for commit guidelines.

## 1.0.0 (2026-01-19)

### Features

- Migrate UI test suite from Selenium to Playwright (3c174d1)
- Add test rerun functionality and remove Firefox support (428eb57, f3c661f, 764445b)
- Enable trace viewer and inspector in `run_tests.sh` (57d3bfe)
- Initial project setup with Playwright QA tests (de36200)

### Bug Fixes

- Resolve Firefox sandbox and permission issues in Docker (8c8e197, 9c16fff)
- Fix `pytest` failure on delete actions (f147a96)

### Refactors

- Improve Page Object Model (POM) classes with a consistent pattern (19f24dc, 84ab4c7, e85ec20, 7237151)
- Reorganize source code structure (e7437cf)
- Use `ADDRESS` environment variable for base URL (c18d1a2)
- Update dependencies in `pyproject.toml` (3e212bc)

### Documentation

- Update README to reflect Playwright migration (b7c6ef0)
- Cleanup changelog from template repository (0fa1566)
