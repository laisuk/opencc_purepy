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
slots, such as `DictSlot.STPhrases`, `DictSlot.TSPhrases`, `DictSlot.STPunctuations`, and other OpenCC slots.
There is no generic `UserDict` slot.

Dictionary slot mappings support both:

- `DictSlot` (recommended)
- string slot names such as `"st_phrases"` (backward compatible)

---

### Recommended: load-time append mode

Use `appends={...}` to load built-in dictionaries first, then custom entries. Duplicate keys use late-comer wins, so
custom entries override built-in entries. This is recommended for most users.

```python
from opencc_purepy import DictSlot, OpenCC

cc = OpenCC.from_dicts(
    config="s2t",
    appends={
        DictSlot.STPhrases: "./UserDict.txt",
    },
)

print(cc.convert("帕兰蒂尔是一家公司"))
```

String slot names remain supported for compatibility:

```python
from opencc_purepy import OpenCC

cc = OpenCC.from_dicts(
    config="s2t",
    appends={
        "st_phrases": "./UserDict.txt",
    },
)
```

The same `appends={...}` and `overrides={...}` arguments are also supported by `DictionaryMaxlength.from_dicts()` when
you want to create and reuse a dictionary instance yourself.

---

### Post-load file customization

Use `DictionaryMaxlength.with_custom_dict_files()` when you already have a dictionary instance and want to apply
OpenCC-compatible text dictionary files after loading it. Post-load customization supports both `appends={...}` and
`overrides={...}`.

```python
from opencc_purepy import DictSlot, OpenCC
from opencc_purepy.dictionary_lib import DictionaryMaxlength

dictionary = DictionaryMaxlength.from_json().with_custom_dict_files(
    appends={
        DictSlot.STPhrases: "./UserDict.txt",
    },
)

cc = OpenCC(config="s2t", dictionary=dictionary)

print(cc.convert("帕兰蒂尔是一家公司"))
```

Create a private dictionary instance first with `DictionaryMaxlength.from_json()` or `DictionaryMaxlength.from_dicts()`.
Do not mutate the shared global provider returned by `DictionaryMaxlength.get_provider()` or
`DictionaryMaxlength.new()`; the post-load customization APIs are intended for private dictionary instances.

---

### Exact in-memory pairs

Use `DictionaryMaxlength.with_custom_dicts()` for exact in-memory custom pairs. This preserves keys exactly, including
leading spaces and embedded spaces.

```python
from opencc_purepy import DictSlot, OpenCC
from opencc_purepy.dictionary_lib import DictionaryMaxlength

dictionary = DictionaryMaxlength.from_json().with_custom_dicts(
    appends={
        DictSlot.STPhrases: {
            " 著": " 著",
            "AI 模型": "AI 模型",
            "帕兰蒂尔": "帕蘭蒂爾",
        },
    },
)

cc = OpenCC(config="s2t", dictionary=dictionary)

print(cc.convert("馬斯克 著"))
print(cc.convert("AI 模型"))
```

---

### Dictionary text format

Custom dictionary files are UTF-8 text files in OpenCC lexicon format. Use one mapping per line:

```text
# Custom company terms
帕兰蒂尔	帕蘭蒂爾
AI模型 AI模型
```

Each entry is parsed as `key<TAB>value` or `key whitespace value`. Blank lines are ignored, comments are allowed with
`#`, and duplicate keys use late-comer wins.

Because file parsing follows OpenCC dictionary rules, leading spaces and embedded spaces in keys are not preserved. Use
`with_custom_dicts()` when the custom key itself contains spaces.

---

### Override mode

Use `overrides={...}` to replace an entire dictionary slot. This is for advanced users who maintain a full replacement
for a selected OpenCC dictionary slot.

```python
from opencc_purepy import DictSlot, OpenCC

cc = OpenCC.from_dicts(
    config="s2t",
    overrides={
        DictSlot.STPhrases: "./company/STPhrases.txt",
    },
)
```

Post-load override mode works the same way:

```python
from opencc_purepy import DictSlot
from opencc_purepy.dictionary_lib import DictionaryMaxlength

dictionary = DictionaryMaxlength.from_json().with_custom_dict_files(
    overrides={
        DictSlot.STPhrases: "./CompanyOnlySTPhrases.txt",
    },
)
```

---

### Supported slots

| `DictSlot`                      | Legacy key                | Default file                |
|---------------------------------|---------------------------|-----------------------------|
| `DictSlot.STCharacters`         | `st_characters`           | `STCharacters.txt`          |
| `DictSlot.STPhrases`            | `st_phrases`              | `STPhrases.txt`             |
| `DictSlot.STPunctuations`       | `st_punctuations`         | `STPunctuations.txt`        |
| `DictSlot.TSCharacters`         | `ts_characters`           | `TSCharacters.txt`          |
| `DictSlot.TSPhrases`            | `ts_phrases`              | `TSPhrases.txt`             |
| `DictSlot.TSPunctuations`       | `ts_punctuations`         | `TSPunctuations.txt`        |
| `DictSlot.TWPhrases`            | `tw_phrases`              | `TWPhrases.txt`             |
| `DictSlot.TWPhrasesRev`         | `tw_phrases_rev`          | `TWPhrasesRev.txt`          |
| `DictSlot.TWVariants`           | `tw_variants`             | `TWVariants.txt`            |
| `DictSlot.TWVariantsRev`        | `tw_variants_rev`         | `TWVariantsRev.txt`         |
| `DictSlot.TWVariantsRevPhrases` | `tw_variants_rev_phrases` | `TWVariantsRevPhrases.txt`  |
| `DictSlot.HKVariants`           | `hk_variants`             | `HKVariants.txt`            |
| `DictSlot.HKVariantsRev`        | `hk_variants_rev`         | `HKVariantsRev.txt`         |
| `DictSlot.HKVariantsRevPhrases` | `hk_variants_rev_phrases` | `HKVariantsRevPhrases.txt`  |
| `DictSlot.JPSCharacters`        | `jps_characters`          | `JPShinjitaiCharacters.txt` |
| `DictSlot.JPSPhrases`           | `jps_phrases`             | `JPShinjitaiPhrases.txt`    |
| `DictSlot.JPVariants`           | `jp_variants`             | `JPVariants.txt`            |
| `DictSlot.JPVariantsRev`        | `jp_variants_rev`         | `JPVariantsRev.txt`         |

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
- Use `with_custom_dict_files()` to apply OpenCC-compatible text files to a private dictionary after loading it.
- Use `with_custom_dicts()` for exact in-memory pairs, especially keys with leading or embedded spaces.
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
> Benchmark separates cold startup, first post-init conversion, and warm cached conversion.

### Runner Platform

| Field     | Value                                                                                                                      |
|-----------|----------------------------------------------------------------------------------------------------------------------------|
| Runner    | Linux X64                                                                                                                  |
| Image     | ubuntu24 20260513.135.3                                                                                                    |
| Kernel    | `Linux runnervmrw5os 6.17.0-1013-azure #13~24.04.1-Ubuntu SMP Wed Apr 15 16:52:17 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux` |
| CPU       | AMD EPYC 9V74 80-Core Processor                                                                                            |
| CPU Cores | 4                                                                                                                          |
| Memory    |                                                                                                                            |
| Python    | Python 3.10.20                                                                                                             |

### Results

#### opencc-purepy v1.3.0

| Input Size        | Cold Total (ms) | Post-init Cold (ms) |  Warm (ms) |
|-------------------|----------------:|--------------------:|-----------:|
| **100 chars**     |       21.849 ms |           19.419 ms |   0.171 ms |
| **1,000 chars**   |       21.572 ms |           21.409 ms |   1.643 ms |
| **10,000 chars**  |       34.063 ms |           32.584 ms |  13.480 ms |
| **100,000 chars** |      158.355 ms |          156.202 ms | 136.870 ms |

*`cold_total` includes `OpenCC(config)` setup plus conversion. `post_init_cold` measures the first conversion after
initialization. `warm` measures conversion after the union cache has already been built. Results depend on runner
hardware and background system load.*

### Notes

> Despite being implemented in pure Python, `opencc_purepy` achieves competitive conversion throughput through
> aggressive caching and starter-index optimizations.
>
> The warm conversion path is practical for large-text workloads such as document conversion, GUI applications, and
> batch processing.

---

## Projects That Use `opencc-purepy`

[OpenccPurepyGui](https://github.com/laisuk/OpenccPurepyGui)

---

## 📄 License

This project is licensed under the [MIT License](https://github.com/laisuk/opencc_purepy/blob/master/LICENSE).

---

Powered by **Pure Python** and **OpenCC** Lexicons.
