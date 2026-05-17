# tests/custom_dicts_test.py

from pathlib import Path
import shutil

from opencc_purepy import OpenCC, DictSlot
from opencc_purepy.dictionary_lib import DictionaryMaxlength

_TEST_DIR = Path(__file__).resolve().parent
_CUSTOM_DICT = _TEST_DIR / "_custom_st_phrases.txt"
_CUSTOM_OVERRIDE_DICT = _TEST_DIR / "_override_st_phrases.txt"
_CUSTOM_PUNCT_DICT = _TEST_DIR / "_custom_st_punctuations.txt"


def _write_custom_dict() -> Path:
    _CUSTOM_DICT.write_text(
        "帕兰蒂尔\t柏蘭蒂爾\n",
        encoding="utf-8",
    )
    return _CUSTOM_DICT


def _cleanup_custom_dict() -> None:
    for path in (_CUSTOM_DICT, _CUSTOM_OVERRIDE_DICT, _CUSTOM_PUNCT_DICT):
        try:
            path.unlink()
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

        assert cc.convert("帕兰蒂尔是一家公司") == "柏蘭蒂爾是一家公司"
    finally:
        _cleanup_custom_dict()


def test_dictionary_from_dicts_appends_late_comer_wins():
    custom_dict = _write_custom_dict()

    try:
        dictionary = DictionaryMaxlength.from_dicts(
            appends={
                DictSlot.ST_PHRASES: custom_dict,
            },
        )

        st_phrases, max_len = dictionary.st_phrases

        assert st_phrases["帕兰蒂尔"] == "柏蘭蒂爾"
        assert max_len >= len("帕兰蒂尔")
    finally:
        _cleanup_custom_dict()


def test_opencc_from_dicts_append_late_comer_wins_existing_key():
    _CUSTOM_DICT.write_text(
        "汉字\t測字\n",
        encoding="utf-8",
    )

    try:
        cc = OpenCC.from_dicts(
            config="s2t",
            appends={
                DictSlot.ST_PHRASES: _CUSTOM_DICT,
            },
        )

        assert cc.convert("汉字转换") == "測字轉換"
    finally:
        _cleanup_custom_dict()


def test_opencc_from_dicts_override_replaces_entire_slot():
    _CUSTOM_OVERRIDE_DICT.write_text(
        "帕兰蒂尔\t柏蘭蒂爾\n",
        encoding="utf-8",
    )

    try:
        cc = OpenCC.from_dicts(
            config="s2t",
            overrides={
                DictSlot.ST_PHRASES: _CUSTOM_OVERRIDE_DICT,
            },
        )

        st_phrases, _max_len = cc.dictionary.st_phrases
        assert st_phrases == {"帕兰蒂尔": "柏蘭蒂爾"}
        assert cc.convert("帕兰蒂尔") == "柏蘭蒂爾"
        assert cc.convert("汉字") == "漢字"
    finally:
        _cleanup_custom_dict()


def test_dictslot_punctuation_append_is_used_by_punctuation_conversion():
    _CUSTOM_PUNCT_DICT.write_text(
        "！\t‼\n",
        encoding="utf-8",
    )

    try:
        cc = OpenCC.from_dicts(
            config="s2t",
            appends={
                DictSlot.ST_PUNCTUATIONS: _CUSTOM_PUNCT_DICT,
            },
        )

        assert cc.convert("“汉字”！", punctuation=True) == "「漢字」‼"
    finally:
        _cleanup_custom_dict()


def test_dictslot_punctuation_enum_members_exist():
    assert DictSlot.ST_PUNCTUATIONS.value == "st_punctuations"
    assert DictSlot.TS_PUNCTUATIONS.value == "ts_punctuations"


def test_legacy_custom_dict_dir_without_punctuation_files_loads():
    legacy_dir = _TEST_DIR / "_legacy_dicts_without_punctuation"
    if legacy_dir.exists():
        shutil.rmtree(legacy_dir)
    legacy_dir.mkdir()

    old_required_files = [
        "STCharacters.txt",
        "STPhrases.txt",
        "TSCharacters.txt",
        "TSPhrases.txt",
        "TWPhrases.txt",
        "TWPhrasesRev.txt",
        "TWVariants.txt",
        "TWVariantsRev.txt",
        "TWVariantsRevPhrases.txt",
        "HKVariants.txt",
        "HKVariantsRev.txt",
        "HKVariantsRevPhrases.txt",
        "JPShinjitaiCharacters.txt",
        "JPShinjitaiPhrases.txt",
        "JPVariants.txt",
        "JPVariantsRev.txt",
    ]

    try:
        for filename in old_required_files:
            (legacy_dir / filename).write_text("", encoding="utf-8")
        (legacy_dir / "STCharacters.txt").write_text("汉\t漢\n", encoding="utf-8")
        (legacy_dir / "TSCharacters.txt").write_text("漢\t汉\n", encoding="utf-8")

        dictionary = DictionaryMaxlength.from_dicts(base_dir=legacy_dir)

        assert dictionary.st_characters == ({"汉": "漢"}, 1)
        assert dictionary.st_punctuations == ({}, 0)
        assert dictionary.ts_punctuations == ({}, 0)
    finally:
        shutil.rmtree(legacy_dir)
