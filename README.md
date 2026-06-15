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

| Code    | Description                                                              |
|---------|--------------------------------------------------------------------------|
| `s2t`   | Simplified → Traditional                                                 |
| `t2s`   | Traditional → Simplified                                                 |
| `s2tw`  | Simplified → Traditional (Taiwan)                                        |
| `tw2s`  | Traditional (Taiwan) → Simplified                                        |
| `s2twp` | Simplified → Traditional (Taiwan) with phrase and variant normalization  |
| `tw2sp` | Traditional (Taiwan) → Simplified with idioms                            |
| `s2hk`  | Simplified → Traditional (Hong Kong)                                     |
| `hk2s`  | Traditional (Hong Kong) → Simplified                                     |
| `s2hkp` | Simplified → Hong Kong Traditional with phrase and variant normalization |
| `hk2sp` | Hong Kong Traditional with phrases/variants → Simplified                 |
| `t2tw`  | Traditional → Traditional (Taiwan)                                       |
| `tw2t`  | Traditional (Taiwan) → Traditional                                       |
| `t2twp` | Traditional → Traditional (Taiwan) with idioms                           |
| `tw2tp` | Traditional (Taiwan) → Traditional with idioms                           |
| `t2hk`  | Traditional → Traditional (Hong Kong)                                    |
| `hk2t`  | Traditional (Hong Kong) → Traditional                                    |
| `t2jp`  | Japanese Kyujitai → Shinjitai                                            |
| `jp2t`  | Japanese Shinjitai → Kyujitai                                            |

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
        DictSlot.TWVariantsPhrases: "./custom/TWVariantsPhrases.txt",
        DictSlot.HKVariantsPhrases: "./custom/HKVariantsPhrases.txt",
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
        DictSlot.TWVariantsPhrases: "./custom/TWVariantsPhrases.txt",
        DictSlot.HKVariantsPhrases: "./custom/HKVariantsPhrases.txt",
    },
)

cc = OpenCC(config="s2t", dictionary=dictionary)

print(cc.convert("帕兰蒂尔是一家公司"))
```

Create a private dictionary instance first with `DictionaryMaxlength.from_json()` or `DictionaryMaxlength.from_dicts()`.
Do not mutate the shared global provider returned by `DictionaryMaxlength.get_provider()` or
`DictionaryMaxlength.new()`; the post-load customization APIs are intended for private dictionary instances.

---

### Tofu-risk / Extension Unicode fallback pairs

Use `DictionaryMaxlength.with_custom_dicts()` for exact in-memory custom pairs when you need to patch
tofu-risk characters or Extension Unicode mappings without restructuring the built-in OpenCC dictionaries.

This is useful for platforms where some CJK Extension characters may render as tofu boxes, or where you want
to provide a temporary project-local fallback before the upstream dictionary data is updated.

```python
from opencc_purepy import DictSlot, OpenCC
from opencc_purepy.dictionary_lib import DictionaryMaxlength

dictionary = DictionaryMaxlength.from_json().with_custom_dicts(
    appends={
        DictSlot.STPhrases: {
            # Project-local fallback pairs for tofu-risk / Extension Unicode cases.
            # Keep these patches small, explicit, and easy to remove later.
            "骖𬴂": "驂騑",
            "𫜩合": "齧合",
            "𫜩蘗吞针": "齧蘗吞針",

            # Normal custom phrase pairs may be mixed in as well.
            "帕兰蒂尔": "帕蘭蒂爾",
        },
        DictSlot.TWVariantsPhrases: {
            "喫茶小舖": "喫茶小舖",
        },
        DictSlot.HKVariantsPhrases: {
            "喫茶小舖": "喫茶小舖",
        },
    },
)

cc = OpenCC(config="s2t", dictionary=dictionary)

print(cc.convert("骖𬴂"))
print(cc.convert("𫜩合"))
print(cc.convert("帕兰蒂尔"))
```

This keeps the core dictionary structure unchanged while still allowing applications to patch specific
high-risk entries at load time.

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

| `DictSlot`                      | Legacy key                | Default file                   |
|---------------------------------|---------------------------|--------------------------------|
| `DictSlot.STCharacters`         | `st_characters`           | `STCharacters.txt`             |
| `DictSlot.STPhrases`            | `st_phrases`              | `STPhrases.txt`                |
| `DictSlot.STPunctuations`       | `st_punctuations`         | `STPunctuations.txt`           |
| `DictSlot.TSCharacters`         | `ts_characters`           | `TSCharacters.txt`             |
| `DictSlot.TSPhrases`            | `ts_phrases`              | `TSPhrases.txt`                |
| `DictSlot.TSPunctuations`       | `ts_punctuations`         | `TSPunctuations.txt`           |
| `DictSlot.TWPhrases`            | `tw_phrases`              | `TWPhrases.txt`                |
| `DictSlot.TWPhrasesRev`         | `tw_phrases_rev`          | `TWPhrasesRev.txt`             |
| `DictSlot.TWVariantsPhrases`    | `tw_variants_phrases`     | `TWVariantsPhrases.txt`        |
| `DictSlot.TWVariants`           | `tw_variants`             | `TWVariants.txt`               |
| `DictSlot.TWVariantsRev`        | `tw_variants_rev`         | `TWVariantsRev.txt`            |
| `DictSlot.TWVariantsRevPhrases` | `tw_variants_rev_phrases` | `TWVariantsRevPhrases.txt`     |
| `DictSlot.HKPhrases`            | `hk_phrases`              | `HKPhrases.txt`                |
| `DictSlot.HKPhrasesRev`         | `hk_phrases_rev`          | `HKPhrasesRev.txt`             |
| `DictSlot.HKVariantsPhrases`    | `hk_variants_phrases`     | `HKVariantsPhrases.txt`        |
| `DictSlot.HKVariants`           | `hk_variants`             | `HKVariants.txt`               |
| `DictSlot.HKVariantsRev`        | `hk_variants_rev`         | `HKVariantsRev.txt`            |
| `DictSlot.HKVariantsRevPhrases` | `hk_variants_rev_phrases` | `HKVariantsRevPhrases.txt`     |
| `DictSlot.JPSCharacters`        | `jps_characters`          | `JPShinjitaiCharacters.txt`    |
| `DictSlot.JPSCharactersRev`     | `jps_characters_rev`      | `JPShinjitaiCharactersRev.txt` |
| `DictSlot.JPSPhrases`           | `jps_phrases`             | `JPShinjitaiPhrases.txt`       |

Forward regional variant phrase slots are applied before their character-level variant slots:

| Slot                         | File                    | Direction                    | Purpose                                                          |
|------------------------------|-------------------------|------------------------------|------------------------------------------------------------------|
| `DictSlot.TWVariantsPhrases` | `TWVariantsPhrases.txt` | Forward TW regional variants | Phrase-level TW variant mappings applied before `TWVariants.txt` |
| `DictSlot.HKVariantsPhrases` | `HKVariantsPhrases.txt` | Forward HK regional variants | Phrase-level HK variant mappings applied before `HKVariants.txt` |

Japanese Shinjitai slots follow the upstream OpenCC JP layout:

| Slot                        | File                           | Purpose                                               |
|-----------------------------|--------------------------------|-------------------------------------------------------|
| `DictSlot.JPSCharacters`    | `JPShinjitaiCharacters.txt`    | Japanese Shinjitai-to-Traditional Kyujitai characters |
| `DictSlot.JPSCharactersRev` | `JPShinjitaiCharactersRev.txt` | Traditional Kyujitai-to-Japanese Shinjitai characters |
| `DictSlot.JPSPhrases`       | `JPShinjitaiPhrases.txt`       | Japanese Shinjitai-to-Traditional Kyujitai phrases    |

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

dictionary = DictionaryMaxlength.from_json("opencc_purepy/dicts/dictionary_maxlength.json")

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

## DeTofu display compatibility fallback

DeTofu replaces mapped tofu-risk rare CJK extension characters with display-compatible fallback characters. It is useful
on systems, browsers, e-book readers, document viewers, or mobile platforms where some non-BMP CJK extension characters
may render as tofu boxes, missing glyphs, or empty boxes.

DeTofu is a display-compatibility pass, not normal OpenCC dictionary conversion. It does not modify phrase matching,
regional variant selection, script detection, or punctuation conversion. If you use it with converted text, apply it
after `convert(...)`.

```python
from opencc_purepy import OpenCC
from opencc_purepy.detofu import DeTofuLevel

cc = OpenCC("t2s")

text = "儼驂騑於上路，訪風景於崇阿"
converted = cc.convert(text)

display_safe = cc.detofu(converted, DeTofuLevel.ExtB)

print(display_safe)
```

String level names are also supported:

```bash
display_safe = cc.detofu(converted, "all")
```

### DeTofu levels

DeTofu levels are threshold-based:

```text
ExtB means ExtB and above
ExtC means ExtC and above
ExtD means ExtD and above
...
ExtI means ExtI only
```

Supported level names:

```text
all
ext-b / b
ext-c / c
ext-d / d
ext-e / e
ext-f / f
ext-g / g
ext-h / h
ext-i / i
```

`"all"` is equivalent to `ExtB`.

### Custom fallback file

Use `detofu_with_custom_file(...)` to add project-local fallback mappings from a UTF-8 text file:

```bash
display_safe = cc.detofu_with_custom_file(
    converted,
    "all",
    "custom_tofu.txt",
)
```

File format:

```text
tofu_char<TAB>fallback_char<TAB>extension
```

Example:

```text
𱁬	?	ExtB
```

Blank lines are ignored, and lines beginning with `#` are ignored. The extension column accepts `B` through `I` or
`ExtB` through `ExtI`. Custom file mappings override built-in mappings for the same tofu-risk character.

### Custom in-memory pairs

Use `detofu_with_custom_pairs(...)` to add direct fallback pairs in memory:

```bash
display_safe = cc.detofu_with_custom_pairs(
    converted,
    "all",
    {
        "𱁬": "?",
    },
)
```

Direct pairs do not have an extension column. They are always added to the selected map, and custom pairs override
built-in mappings for the same tofu-risk character. Only the first Unicode scalar from each key and value is used.
Empty keys or values are ignored.

### DeTofu contract

- Unknown characters are preserved unchanged.
- DeTofu never replaces unknown characters with `?`, `□`, `�`, or empty text.
- DeTofu only replaces characters that exist in the built-in or custom fallback map.
- DeTofu is intended as a final display-compatibility pass.
- For converted text, call `cc.detofu(...)` after `cc.convert(...)`.

---

## 🧩 API Reference

### Exports

- `OpenCC`
- `OpenccConfig`
- `DeTofuLevel` is available from `opencc_purepy.detofu`

### `OpenCC` class

- `OpenCC(config: Union[str, OpenccConfig] = "s2t")`  
  Create a converter with a supported config string or `OpenccConfig` enum value. Raises `ValueError` for unsupported
  configs.
- `set_config(config: Union[str, OpenccConfig]) -> None`  
  Update the active conversion config. Raises `ValueError` for unsupported configs.
- `get_config() -> str`  
  Return the current canonical config name.
- `supported_configs() -> List[str]`  
  Return all supported config names.
- `get_last_error() -> Optional[str]`  
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
  Simplified Chinese to Taiwan Traditional with phrase and variant normalization.
- `tw2sp(input: str, punctuation: bool = False) -> str`  
  Taiwan Traditional with idioms to Simplified Chinese.
- `s2hk(input: str, punctuation: bool = False) -> str`  
  Simplified Chinese to Hong Kong Traditional.
- `hk2s(input: str, punctuation: bool = False) -> str`  
  Hong Kong Traditional to Simplified Chinese.
- `s2hkp(input: str, punctuation: bool = False) -> str`  
  Simplified Chinese to Hong Kong Traditional with phrase and variant normalization.
- `hk2sp(input: str, punctuation: bool = False) -> str`  
  Hong Kong Traditional with phrases/variants to Simplified Chinese.
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

- `detofu(  
  input: Optional[str],  
  level: Union[DeTofuLevel, str] = DeTofuLevel.ExtB  
  ) -> str`

  Apply built-in DeTofu display-compatible fallback mappings.

- `detofu_with_custom_file(
  input: Optional[str],
  level: Union[DeTofuLevel, str],
  path: str
  ) -> str`

  Apply built-in DeTofu mappings plus a UTF-8 custom fallback file.

- `detofu_with_custom_pairs(
  input: Optional[str],
  level: Union[DeTofuLevel, str],
  pairs: Union[
      Mapping[str, str],
      Iterable[Tuple[str, str]]
  ]
  ) -> str`

  Apply built-in DeTofu mappings plus direct in-memory fallback pairs.

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
