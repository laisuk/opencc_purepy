# opencc_purepy

[![PyPI version](https://img.shields.io/pypi/v/opencc-purepy)](https://pypi.org/project/opencc-purepy/)
[![License](https://img.shields.io/github/license/laisuk/opencc_pyo3)](https://github.com/laisuk/opencc_pyo3/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/personalized-badge/opencc-purepy?period=month&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/opencc-purepy)

**`opencc_purepy`** is a **pure Python implementation** of OpenCC (Open Chinese Convert), enabling conversion between different Chinese text variants such as Simplified, Traditional, Hong Kong, Taiwan, and Japanese Kanji.  
It uses dictionary-based segmentation and mapping logic inspired by [BYVoid/OpenCC](https://github.com/BYVoid/OpenCC).

---

## 🔧 Features

- ✅ Pure Python – no native dependencies
- 🔄 Supports conversion between multiple Chinese locales:
  - Simplified ↔ Traditional
  - Traditional ↔ Hong Kong / Taiwan / Japanese
- ✨ Optional punctuation style conversion
- 🧠 Automatic simplified/traditional code detection

---

## 🔁 Supported Conversion Configs

| Code     | Description                                    |
|----------|------------------------------------------------|
| `s2t`    | Simplified → Traditional                       |
| `t2s`    | Traditional → Simplified                       |
| `s2tw`   | Simplified → Traditional (Taiwan)              |
| `tw2s`   | Traditional (Taiwan) → Simplified              |
| `s2twp`  | Simplified → Traditional (Taiwan) with idioms  |
| `tw2sp`  | Traditional (Taiwan)  → Simplified with idioms |
| `s2hk`   | Simplified → Traditional (Hong Kong)           |
| `hk2s`   | Traditional (Hong Kong) → Simplified           |
| `t2tw`   | Traditional → Traditional (Taiwan)             |
| `tw2t`   | Traditional (Taiwan) → Traditional             |
| `t2twp`  | Traditional → Traditional (Taiwan) with idioms |
| `tw2tp`  | Traditional (Taiwan) → Traditional with idioms |
| `t2hk`   | Traditional → Traditional (Hong Kong)          |
| `hk2t`   | Traditional (Hong Kong) → Traditional          |
| `t2jp`   | Japanese Kyojitai → Shinjitai                  |
| `jp2t`   | Japanese Shinjitai → Kyojitai                  |

---

## 📦 Installation

```bash
pip install opencc-purepy
```

## 🚀 Usage

### 🐍 Python

```python
from opencc_purepy import OpenCC

text = "“春眠不觉晓，处处闻啼鸟。”"
opencc = OpenCC("s2t")
converted = opencc.convert(text, punctuation=True)
print(converted)  # 「春眠不覺曉，處處聞啼鳥。」
```

### 🖥 CLI

```sh
python -m opencc_purepy convert -i input.txt -o output.txt -c s2t -p
```

Or if installed as a script:

```bash
opencc-purepy convert -i input.txt -o output.txt -c s2t -p
```

## 🧩 API Reference

### Class: `OpenCC`

- `OpenCC(config: str = "s2t")`
    - `config`: Conversion configuration (see above).
- `convert(input: str, punctuation: bool = False) -> str`
    - Convert text with optional punctuation conversion.
- `zho_check(input: str) -> int`  
  - Detects the code of the input text.
      - 1 - Traditional, 
      - 2 - Simplified, 
      - 0 - others

## 🛠 Development

- Python bindings: [opencc_purepy/__init__.py](https://github.com/laisuk/opencc_purepy/blob/master/opencc_purepy/__init__.py), [opencc_purepy/opencc_purepy.pyi](https://github.com/laisuk/opencc_purepy/blob/master/opencc_purepy/opencc_purepy.pyi)
- CLI: [opencc_purepy/__main__.py](https://github.com/laisuk/opencc_purepy/blob/master/opencc_purepy/__main__.py)

## 📄 License
This project is licensed under the [MIT](https://github.com/laisuk/opencc_purepy/blob/master/LICENSE) License.

---

Powered by Pure Python and OpenCC Lexicons.