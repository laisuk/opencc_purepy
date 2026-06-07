import unittest
import json
import os
from opencc_purepy.core import OpenCC, OpenccConfig
from opencc_purepy.dictionary_lib import DictionaryMaxlength
from opencc_purepy.union_cache import UnionKey
from opencc_purepy.__main__ import _config_arg, _format_arg


class TestOpenCC(unittest.TestCase):

    def setUp(self):
        self.converter = OpenCC("s2t")

    def test_s2t_conversion(self):
        simplified = "汉字转换测试：意大利的罗马城不是一天里就能建成的"
        result = self.converter.s2t(simplified)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "漢字轉換測試：意大利的羅馬城不是一天裡就能建成的")  # Expect some output

    def test_t2s_conversion(self):
        traditional = "漢字轉換測試：意大利的羅馬城不是一天裡就能建成的"
        self.converter.config = "t2s"
        result = self.converter.convert(traditional)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "汉字转换测试：意大利的罗马城不是一天里就能建成的")

    def test_s2twp_conversion(self):
        simplified = "汉字转换测试：意大利的罗马城不是一天里就能建成的"
        result = self.converter.s2twp(simplified)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "漢字轉換測試：義大利的羅馬城不是一天裡就能建成的")  # Expect some output

    def test_s2twp_applies_taiwan_phrase_and_variant_normalization(self):
        self.assertEqual(self.converter.s2twp("软件为"), "軟體為")
        self.assertEqual(self.converter.s2twp("软件众"), "軟體眾")

    def test_s2twp_uses_two_round_plan(self):
        refs = self.converter._get_dict_refs("s2twp")

        self.assertIsNotNone(refs.round_2)
        self.assertIsNone(refs.round_3)

    def test_tw2sp_conversion(self):
        traditional = "漢字轉換測試：義大利的羅馬城不是一天裡就能建成的"
        self.converter.config = "tw2sp"
        result = self.converter.convert(traditional)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "汉字转换测试：意大利的罗马城不是一天里就能建成的")

    def test_invalid_config(self):
        with self.assertRaises(ValueError):
            OpenCC("bad_config")

    def test_config_parse_normalizes_supported_names(self):
        self.assertEqual(OpenccConfig.parse(" S2T "), OpenccConfig.S2T)

    def test_cli_config_arg_normalizes_supported_names(self):
        self.assertEqual(_config_arg("s2TW"), "s2tw")
        self.assertEqual(_config_arg("S2t"), "s2t")

    def test_cli_format_arg_normalizes_supported_names(self):
        self.assertEqual(_format_arg("DOCX"), "docx")

    def test_convert_with_punctuation(self):
        simplified = "“汉字转换测试”"
        result = self.converter.s2t(simplified, punctuation=True)
        self.assertEqual(result, "「漢字轉換測試」")

    def test_t2s_convert_with_punctuation(self):
        traditional = "「漢字轉換測試」"
        result = OpenCC("t2s").convert(traditional, punctuation=True)
        self.assertEqual(result, "“汉字转换测试”")

    def test_punctuation_applies_to_variant_configs(self):
        converter = OpenCC("t2tw")
        result = converter.convert("“軟體”", punctuation=True)
        self.assertIn("「", result)
        self.assertIn("」", result)

    def test_segment_replace_matches_direct_conversion_for_short_punctuated_text(self):
        refs = self.converter._get_dict_refs("s2t")
        slots, cap = refs._normalize()[0]
        text = "汉字转换测试，意大利的罗马城不是一天里就能建成的。" * 20
        expected = OpenCC.convert_segment(text, slots, cap)

        result = self.converter.segment_replace(text, slots, cap)
        self.assertEqual(expected, result)

    def test_backward_compatible_old_json_without_punctuation_slots(self):
        old_json = {
            "st_characters": [{"汉": "漢"}, 1],
            "st_phrases": [{"汉字": "漢字"}, 2],
            "ts_characters": [{"漢": "汉"}, 1],
            "ts_phrases": [{"漢字": "汉字"}, 2],
        }

        from tempfile import NamedTemporaryFile

        with NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
            json.dump(old_json, handle, ensure_ascii=False)
            path = handle.name

        try:
            dictionary = DictionaryMaxlength.from_json(path)
        finally:
            os.unlink(path)
        self.assertEqual(dictionary.st_punctuations, ({}, 0))
        self.assertEqual(dictionary.ts_punctuations, ({}, 0))

    def test_union_cache_warm_path_reuses_indexed_union(self):
        cc = OpenCC("s2t")
        first = cc.convert("汉字转换测试")
        union = cc.union_cache.get_union(UnionKey.S2T)
        second = cc.convert("汉字转换测试")

        self.assertEqual(first, "漢字轉換測試")
        self.assertEqual(second, first)
        self.assertTrue(union.indexed)

    def test_zho_check(self):
        mixed = "這是一個測試test123"  # Should be treated as Traditional
        result = self.converter.zho_check(mixed)
        self.assertEqual(result, 1)  # Assert this is detected as Traditional


if __name__ == "__main__":
    unittest.main()
