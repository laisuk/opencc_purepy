# Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and uses
the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.

---

## [1.3.0-beta1] - unreleased

### Added

- Added `StarterUnion` / `UnionCache` conversion pipeline for faster warm conversions.
- Added `DictSlot` enum for strongly-typed OpenCC dictionary slot selection.
- Added `DictSlotLike` compatibility type for accepting both `DictSlot` and legacy `str` slot keys.
- Added `st_punctuations` and `ts_punctuations` dictionary slots.
- Added `DictSlot.ST_PUNCTUATIONS` and `DictSlot.TS_PUNCTUATIONS` for punctuation dictionary customization.
- Added bundled `STPunctuations.txt` and `TSPunctuations.txt` dictionaries.
- Added post-load custom dictionary APIs:
    - `DictionaryMaxlength.with_custom_dicts()`
    - `DictionaryMaxlength.with_custom_dict_files()`
- Added support for exact in-memory custom dictionary keys, including keys containing spaces.
- Added protection against mutating the shared global `DictionaryMaxlength` provider through post-load custom dictionary
  APIs.
- Added enhanced benchmark scenarios:
    - `cold_total`
    - `post_init_cold`
    - `warm`

### Changed

- Refactored the main `OpenCC` conversion path to use cached starter-union dictionaries while preserving the legacy
  public conversion methods and config validation behavior.
- Refactored `DictionaryMaxlength.from_dicts()` to support typed dictionary slot mappings.
- Improved dictionary slot validation with centralized slot normalization helpers.
- Added support for both enum-name (`"ST_PHRASES"`) and legacy attribute-style (`"st_phrases"`) slot resolution.
- Preserved backward compatibility for existing `str`-based dictionary slot APIs.
- Preserved custom dictionary append and override semantics:
    - append mode remains late-comer-wins for duplicate keys.
    - override mode still replaces the entire target slot before appends are applied.
- Refactored public API typing hints for improved IDE completion and static analysis support.
- Improved `from_dicts()` documentation and examples to include `DictSlot` usage.
- Moved dictionary slot definitions into dedicated `dict_slot.py` module for cleaner public API organization.
- Updated dictionary JSON schema for punctuation slot support.
- Kept older JSON dictionaries without `st_punctuations` or `ts_punctuations` loadable by defaulting missing
  punctuation slots to empty dictionaries.
- Kept legacy custom dictionary directories loadable when punctuation text files are absent.
- Clarified the distinction between OpenCC-compatible text dictionary files and exact in-memory custom dictionary pairs.
- Improved large-text steady-state conversion performance.

### Performance

- Warm conversions reuse cached starter indexes after the first conversion for a given dictionary/config path.
- First conversion may include union-cache initialization cost, so benchmark output now separates total cold startup,
  post-init cold conversion, and warm conversion timings.

### Tests

- Added coverage for basic `s2t` / `t2s` conversion, punctuation conversion through the new punctuation slots,
  append mode, override mode, post-load custom dictionary APIs, exact-key custom dictionary pairs,
  shared-provider mutation protection, `DictSlot` punctuation enum usage, old JSON compatibility,
  legacy dictionary directories without punctuation files, and the warm union-cache path.

---

## [1.2.4] - 2026-05-15

### Added

- Added custom dictionary loading through OpenCC-compatible dictionary slots, including append mode for user/company
  terms and override mode for full dictionary replacements.
- Added `OpenCC.from_dicts(...)` for creating converters directly from TXT dictionaries with `appends` and
  `overrides`.
- Added direct `DictionaryMaxlength` customization support through `DictionaryMaxlength.from_dicts(...)`, allowing one
  loaded dictionary container to be shared across many `OpenCC` instances.
- Added the `dictgen` CLI subcommand for generating `dictionary_maxlength.json` from TXT dictionary files.

### Notes

- Custom dictionaries follow the OpenCC lexicon structure and attach to existing slots such as `st_phrases` or
  `ts_phrases`; this release does not introduce a generic `UserDict.txt` slot.
- No breaking public API changes.

---

## [1.2.3] - 2026-05-14

### Changed

- Preserved public config normalization in CLI parsing so values such as `S2t` and `s2TW` are accepted and normalized
  consistently with `OpenCC`.
- Normalized Office CLI `--format` values case-insensitively while still rejecting unsupported formats.
- Refined punctuation translation typing with a public local translate-table alias for stricter type-checker
  compatibility.

---

## [1.2.2] - 2026-05-14

### Changed

- Updated dictionary data.
- Tightened public config validation so unsupported `OpenCC` configs raise `ValueError` instead of silently falling back
  to `s2t`.
- Updated CLI config and Office format parsing to reuse the public supported-config and supported-format lists.
- Applied punctuation conversion consistently across all public conversion methods.
- Refined punctuation translation typing with a public local translate-table alias for stricter type-checker
  compatibility.

### Fixed

- Included the bundled OpenCC dictionary license file in packaged data.

### Notes

- This release remains based on the legacy sequential conversion pipeline.
- The next major version (`v1.3.0`) is planned to introduce `StarterUnion` + `UnionCache` optimizations to reduce
  repeated dictionary lookup overhead and improve conversion performance.

---

## [1.2.1] - 2026-05-08

### Added

- Added PyPI publishing workflow.

### Changed

- Update dictionary data.
- Benchmark results from GitHub CI instead of local.

---

## [1.2.0] - 2026-04-08

### Added

- Added `OpenccConfig` enum for canonical config names and typed config handling.

### Changed

- Updated dictionary data.
- Optimized core conversion and config normalization.
- Improved serial conversion strategy by preferring delimiter-based split ranges for punctuated text while keeping
  direct conversion for single-range input and parallel conversion for very large input.

### Notes

- No breaking public API change.

---

## [1.1.0] - 2025-08-13

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
