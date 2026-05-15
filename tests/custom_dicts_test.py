# tests/custom_dicts_test.py

from pathlib import Path

from opencc_purepy import OpenCC
from opencc_purepy.dictionary_lib import DictionaryMaxlength

_TEST_DIR = Path(__file__).resolve().parent
_CUSTOM_DICT = _TEST_DIR / "_custom_st_phrases.txt"


def _write_custom_dict() -> Path:
    _CUSTOM_DICT.write_text(
        "帕兰蒂尔\t帕蘭蒂爾\n",
        encoding="utf-8",
    )
    return _CUSTOM_DICT


def _cleanup_custom_dict() -> None:
    try:
        _CUSTOM_DICT.unlink()
    except FileNotFoundError:
        pass


def test_opencc_from_dicts_appends_custom_st_phrase():
    custom_dict = _write_custom_dict()

    try:
        cc = OpenCC.from_dicts(
            config="s2t",
            appends={
                "st_phrases": custom_dict,
            },
        )

        assert cc.convert("帕兰蒂尔是一家公司") == "帕蘭蒂爾是一家公司"
    finally:
        _cleanup_custom_dict()


def test_dictionary_from_dicts_appends_late_comer_wins():
    custom_dict = _write_custom_dict()

    try:
        dictionary = DictionaryMaxlength.from_dicts(
            appends={
                "st_phrases": custom_dict,
            },
        )

        st_phrases, max_len = dictionary.st_phrases

        assert st_phrases["帕兰蒂尔"] == "帕蘭蒂爾"
        assert max_len >= len("帕兰蒂尔")
    finally:
        _cleanup_custom_dict()
