# Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and uses
the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.

---

## [1.1.0] - 2025-08-02

### Added

- Add Parallel processing for input text >= 1,000,000 characters.

### Changed

- Changed flag --office to subcommand office
- Office helper now use pathlib module to avoid path string type mismatch warnings.
- Added split string ranges parameters: delimiters inclusive/exclusive.
- Optimized text split for conversion.
- Some minor code optimizations.
- Updated STPhrases.txt

---

## [1.0.3] – 2025-07-06

### Changed

- Optimized internal dictionary caching for better performance.
- Improved punctuation replacement logic using `str.translate()` fallback.
- Improved UTF-8 byte-limit handling in zho_check() by using safe character slicing based on actual encoded byte count
- Ensured accurate language detection without cutting multibyte characters mid-way
- Clarified that the module is compatible with Python 2.7+ (core only).
- Optimized conversion code to reduce intermediate allocations.

---

## [1.0.2] – 2025-06-27

### Fixed

- Improved Chinese text detection accuracy for mixed input.

### Changed

- Rebuilt JSON dictionary after lexicon structure optimization.
- General code cleanup and performance tuning.

---

## [1.0.1] – 2025-06-26

### Added

- Support for Office document (`.docx`, `.xlsx`, `.pptx`, `.odt`) and EPUB text conversion.

### Changed

- Rebuilt dictionary with minor lexicon corrections.
- Codebase optimization and structural cleanup.

---

## [1.0.0] – 2025-06-18

### Added

- Initial release of `opencc-purepy` on PyPI.
- Pure Python OpenCC-compatible engine for Chinese text conversion.
- Supported standard OpenCC configs:
    - `s2t`, `s2tw`, `s2twp`, `s2hk`, `t2s`, `tw2s`, `tw2sp`, `hk2s`, `jp2t`, `t2jp`
- CLI tool: `python -m opencc_purepy` for simple command-line conversion.
