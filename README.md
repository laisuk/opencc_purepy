# opencc_purepy

[![PyPI version](https://img.shields.io/pypi/v/opencc-purepy)](https://pypi.org/project/opencc-purepy/)
[![License](https://img.shields.io/github/license/laisuk/opencc_pyo3)](https://github.com/laisuk/opencc_purepy/blob/master/LICENSE)
[![Downloads](https://static.pepy.tech/personalized-badge/opencc-purepy?period=month&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/opencc-purepy)
[![Build & Release](https://github.com/laisuk/opencc_purepy/actions/workflows/release.yml/badge.svg)](https://github.com/laisuk/opencc_purepy/actions/workflows/release.yml)

**opencc_purepy** is a **pure Python** implementation
of [OpenCC (Open Chinese Convert)](https://github.com/BYVoid/OpenCC),
supporting conversion between Simplified, Traditional, Hong Kong, Taiwan, and Japanese Kanji.  
It uses dictionary-based segmentation and mapping logic inspired by the original OpenCC.

---

## 🚩 Features

- **Pure Python** – no native dependencies
- **Multiple Chinese locale conversions** (Simplified, Traditional, HK, TW, JP)
- **Punctuation style conversion** (optional)
- **Automatic code detection** (Simplified/Traditional)
- **CLI** with Office document support (`.docx`, `.xlsx`, `.pptx`, `.odt`, `.ods`, `.odp`, `.epub`)

> 🐍 `opencc_purepy` requires **Python 3.7 or later**.

---

## 🔁 Supported Conversion Configs

| Code    | Description                                    |
|---------|------------------------------------------------|
| `s2t`   | Simplified → Traditional                       |
| `t2s`   | Traditional → Simplified                       |
| `s2tw`  | Simplified → Traditional (Taiwan)              |
| `tw2s`  | Traditional (Taiwan) → Simplified              |
| `s2twp` | Simplified → Traditional (Taiwan) with idioms  |
| `tw2sp` | Traditional (Taiwan) → Simplified with idioms  |
| `s2hk`  | Simplified → Traditional (Hong Kong)           |
| `hk2s`  | Traditional (Hong Kong) → Simplified           |
| `t2tw`  | Traditional → Traditional (Taiwan)             |
| `tw2t`  | Traditional (Taiwan) → Traditional             |
| `t2twp` | Traditional → Traditional (Taiwan) with idioms |
| `tw2tp` | Traditional (Taiwan) → Traditional with idioms |
| `t2hk`  | Traditional → Traditional (Hong Kong)          |
| `hk2t`  | Traditional (Hong Kong) → Traditional          |
| `t2jp`  | Japanese Kyujitai → Shinjitai                  |
| `jp2t`  | Japanese Shinjitai → Kyujitai                  |

---

## 📦 Installation

```bash
pip install opencc-purepy
```

---

## 🚀 Usage

### Python

```python
from opencc_purepy import OpenCC

text = "“春眠不觉晓，处处闻啼鸟。”"
opencc = OpenCC("s2t")
converted = opencc.convert(text, punctuation=True)
print(converted)  # 「春眠不覺曉，處處聞啼鳥。」
```

### CLI

#### Text File Conversion

```sh
python -m opencc_purepy convert -i input.txt -o output.txt -c s2t -p
# or, if installed as a script:
opencc-purepy convert -i input.txt -o output.txt -c s2t -p
```

#### Office Document Conversion subcommand (`office`)

Supports: `.docx`, `.xlsx`, `.pptx`, `.odt`, `.ods`, `.odp`, `.epub`

```sh
# Convert Word document with font preservation
opencc-purepy office -i example.docx -c t2s --keep-font

# Convert EPUB and auto-detect output name
opencc-purepy office -i book.epub -c s2t --auto-ext

# Convert Excel and specify output path and format
opencc-purepy office -i sheet.xlsx -o result.xlsx -c s2tw --format xlsx
```

> ℹ️ With `office` subcommand, the input is processed as an Office or EPUB document and OpenCC conversion is applied
> internally.

---

## 📚 Custom Dictionaries

`opencc_purepy` follows the OpenCC lexicon structure. Custom entries are loaded through existing OpenCC dictionary
slots, such as `DictSlot.ST_PHRASES` or `DictSlot.TS_PHRASES`; do not use or document a generic `UserDict.txt` slot.

This keeps `DictionaryMaxlength`, `DictRefs`, and future acceleration structures such as `UnionCache` stable and
OpenCC-compatible.

Dictionary slot mappings support both:

- `DictSlot` (recommended)
- legacy `str` keys (backward compatible)

---

### Append mode

Use `appends={...}` to load built-in dictionaries first, then custom entries. Duplicate keys use late-comer wins, so
custom entries override built-in entries. This is recommended for most users.

```python
from opencc_purepy import DictSlot, OpenCC

cc = OpenCC.from_dicts(
    config="s2t",
    appends={
        DictSlot.ST_PHRASES: "./UserDict.txt",
    },
)

print(cc.convert("帕兰蒂尔是一家公司"))
```

Legacy string keys remain supported:

```python
from opencc_purepy import OpenCC

cc = OpenCC.from_dicts(
    config="s2t",
    appends={
        "st_phrases": "./UserDict.txt",
    },
)
```

---

### Override mode

Use `overrides={...}` to replace an entire dictionary slot with a custom file. This is intended for advanced users or
proprietary full dictionary copies.

```python
from opencc_purepy import DictSlot, OpenCC

cc = OpenCC.from_dicts(
    config="s2t",
    overrides={
        DictSlot.ST_PHRASES: "./company/STPhrases.txt",
    },
)
```

---

### Direct dictionary injection

```python
from opencc_purepy import DictSlot, OpenCC
from opencc_purepy.dictionary_lib import DictionaryMaxlength

dictionary = DictionaryMaxlength.from_dicts(
    appends={
        DictSlot.ST_PHRASES: "./UserDict.txt",
    },
)

cc = OpenCC(config="s2t", dictionary=dictionary)
```

---

### Dictionary text format

Custom dictionary files are UTF-8 text files. Use one mapping per line in `phrase<TAB>translation` format. Blank lines
are ignored, lines starting with `#` are comments, and duplicate keys are resolved by late-comer wins.

```text
# Custom company terms
帕兰蒂尔	帕蘭蒂爾
```

---

### Supported slots

| `DictSlot`                         | Legacy key                | Default file                |
|------------------------------------|---------------------------|-----------------------------|
| `DictSlot.ST_CHARACTERS`           | `st_characters`           | `STCharacters.txt`          |
| `DictSlot.ST_PHRASES`              | `st_phrases`              | `STPhrases.txt`             |
| `DictSlot.ST_PUNCTUATIONS`         | `st_punctuations`         | `STPunctuations.txt`        |
| `DictSlot.TS_CHARACTERS`           | `ts_characters`           | `TSCharacters.txt`          |
| `DictSlot.TS_PHRASES`              | `ts_phrases`              | `TSPhrases.txt`             |
| `DictSlot.TS_PUNCTUATIONS`         | `ts_punctuations`         | `TSPunctuations.txt`        |
| `DictSlot.TW_PHRASES`              | `tw_phrases`              | `TWPhrases.txt`             |
| `DictSlot.TW_PHRASES_REV`          | `tw_phrases_rev`          | `TWPhrasesRev.txt`          |
| `DictSlot.TW_VARIANTS`             | `tw_variants`             | `TWVariants.txt`            |
| `DictSlot.TW_VARIANTS_REV`         | `tw_variants_rev`         | `TWVariantsRev.txt`         |
| `DictSlot.TW_VARIANTS_REV_PHRASES` | `tw_variants_rev_phrases` | `TWVariantsRevPhrases.txt`  |
| `DictSlot.HK_VARIANTS`             | `hk_variants`             | `HKVariants.txt`            |
| `DictSlot.HK_VARIANTS_REV`         | `hk_variants_rev`         | `HKVariantsRev.txt`         |
| `DictSlot.HK_VARIANTS_REV_PHRASES` | `hk_variants_rev_phrases` | `HKVariantsRevPhrases.txt`  |
| `DictSlot.JPS_CHARACTERS`          | `jps_characters`          | `JPShinjitaiCharacters.txt` |
| `DictSlot.JPS_PHRASES`             | `jps_phrases`             | `JPShinjitaiPhrases.txt`    |
| `DictSlot.JP_VARIANTS`             | `jp_variants`             | `JPVariants.txt`            |
| `DictSlot.JP_VARIANTS_REV`         | `jp_variants_rev`         | `JPVariantsRev.txt`         |

---

### Generate JSON with dictgen

TXT dictionaries are human-editable source files. `dictionary_maxlength.json` is a generated/cache format, so prefer
`dictgen` instead of manually editing JSON.

```sh
opencc-purepy dictgen -d ./my_dicts -o dictionary_maxlength.json
```

```python
from opencc_purepy import OpenCC
from opencc_purepy.dictionary_lib import DictionaryMaxlength

dictionary = DictionaryMaxlength.from_json("./dictionary_maxlength.json")

cc = OpenCC(
    config="s2t",
    dictionary=dictionary,
)
```

---

### Which mode should I use?

- Use `appends` for a few user or company terms.
- Use `overrides` when maintaining a full proprietary replacement of an OpenCC dictionary file.
- Use `dictgen` when you want to bake TXT dictionaries into JSON for reuse or faster loading.
- Use direct dictionary injection when sharing one loaded dictionary across many `OpenCC` instances.
- Prefer `DictSlot` for new code and IDE-friendly type checking.
- Legacy `str` slot keys remain fully supported for backward compatibility.

---

## 🧩 API Reference

### Exports

- `OpenCC`
- `OpenccConfig`

### `OpenCC` class

- `OpenCC(config: str | OpenccConfig = "s2t")`  
  Create a converter with a supported config string or `OpenccConfig` enum value. Raises `ValueError` for unsupported
  configs.
- `set_config(config: str | OpenccConfig) -> None`  
  Update the active conversion config. Raises `ValueError` for unsupported configs.
- `get_config() -> str`  
  Return the current canonical config name.
- `supported_configs() -> list[str]`  
  Return all supported config names.
- `get_last_error() -> str | None`  
  Return the last validation or conversion error, if any.
- `convert(input: str, punctuation: bool = False) -> str`  
  Convert text using the active config, with optional punctuation conversion.
- `s2t(input: str, punctuation: bool = False) -> str`  
  Simplified Chinese to Traditional Chinese.
- `t2s(input: str, punctuation: bool = False) -> str`  
  Traditional Chinese to Simplified Chinese.
- `s2tw(input: str, punctuation: bool = False) -> str`  
  Simplified Chinese to Taiwan Traditional.
- `tw2s(input: str, punctuation: bool = False) -> str`  
  Taiwan Traditional to Simplified Chinese.
- `s2twp(input: str, punctuation: bool = False) -> str`  
  Simplified Chinese to Taiwan Traditional with idiom and phrase conversion.
- `tw2sp(input: str, punctuation: bool = False) -> str`  
  Taiwan Traditional with idioms to Simplified Chinese.
- `s2hk(input: str, punctuation: bool = False) -> str`  
  Simplified Chinese to Hong Kong Traditional.
- `hk2s(input: str, punctuation: bool = False) -> str`  
  Hong Kong Traditional to Simplified Chinese.
- `t2tw(input: str, punctuation: bool = False) -> str`  
  Traditional Chinese to Taiwan Traditional.
- `t2twp(input: str, punctuation: bool = False) -> str`  
  Traditional Chinese to Taiwan Traditional with phrase mappings.
- `tw2t(input: str, punctuation: bool = False) -> str`  
  Taiwan Traditional to standard Traditional Chinese.
- `tw2tp(input: str, punctuation: bool = False) -> str`  
  Taiwan Traditional to standard Traditional Chinese with phrase reversal.
- `t2hk(input: str, punctuation: bool = False) -> str`  
  Traditional Chinese to Hong Kong variant.
- `hk2t(input: str, punctuation: bool = False) -> str`  
  Hong Kong Traditional to standard Traditional Chinese.
- `t2jp(input: str, punctuation: bool = False) -> str`  
  Traditional Chinese to Japanese variants.
- `jp2t(input: str, punctuation: bool = False) -> str`  
  Japanese Shinjitai to Traditional Chinese.
- `st(input: str) -> str`  
  Character-only Simplified to Traditional conversion.
- `ts(input: str) -> str`  
  Character-only Traditional to Simplified conversion.
- `zho_check(input: str) -> int`  
  Detect the input text type:  
  &nbsp;&nbsp;`1` - Traditional, `2` - Simplified, `0` - Others

### `OpenccConfig` enum

- Members include: `S2T`, `T2S`, `S2TW`, `TW2S`, `S2TWP`, `TW2SP`, `S2HK`, `HK2S`, `T2TW`, `TW2T`, `T2TWP`, `TW2TP`,
  `T2HK`, `HK2T`, `T2JP`, `JP2T`
- `to_canonical_name() -> str`  
  Return the lowercase OpenCC config string.
- `parse(value: str) -> OpenccConfig`  
  Parse a config string into an enum value.

---

## 🛠 Development

- Python bindings: [
  `opencc_purepy/__init__.py`](https://github.com/laisuk/opencc_purepy/blob/master/opencc_purepy/__init__.py), [
  `opencc_purepy/core.py`](https://github.com/laisuk/opencc_purepy/blob/master/opencc_purepy/core.py)
- CLI: [`opencc_purepy/__main__.py`](https://github.com/laisuk/opencc_purepy/blob/master/opencc_purepy/__main__.py)

---

## ⚡ Benchmark

> Measured on GitHub Actions `ubuntu-latest` using the default `s2t` configuration.  
> Each test averaged over 20 runs with the shared dictionary cache reused across runs.

### Runner Platform

| Field     | Value                                                                                                                      |
|-----------|----------------------------------------------------------------------------------------------------------------------------|
| Runner    | Linux X64                                                                                                                  |
| Image     | ubuntu24 20260413.86.1                                                                                                     |
| Kernel    | `Linux runnervmeorf1 6.17.0-1010-azure #10~24.04.1-Ubuntu SMP Fri Mar  6 22:00:57 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux` |
| CPU       | Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz                                                                              |
| CPU Cores | 4                                                                                                                          |
| Memory    | Not reported                                                                                                               |
| Python    | Python 3.10.20                                                                                                             |

### Results

| Input Size        | Avg. Time (ms) |
|-------------------|---------------:|
| **100 chars**     |       0.221 ms |
| **1,000 chars**   |       1.769 ms |
| **10,000 chars**  |      17.584 ms |
| **100,000 chars** |     173.838 ms |

*Timings reuse the shared dictionary cache, but still include per-run `OpenCC` instance setup; results depend on runner
hardware and background system load.*


---

## Projects That Use `opencc-purepy`

[OpenccPurepyGui](https://github.com/laisuk/OpenccPurepyGui)

---

## 📄 License

This project is licensed under the [MIT License](https://github.com/laisuk/opencc_purepy/blob/master/LICENSE).

---

Powered by **Pure Python** and **OpenCC** Lexicons.
