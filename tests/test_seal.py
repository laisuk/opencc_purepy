import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from opencc_purepy import DictSlot, OpenCC, OpenccConfig
from opencc_purepy.dictionary_lib import DictionaryMaxlength
from opencc_purepy.union_cache import UnionKey


class TestSeal(unittest.TestCase):
    def test_builtin_conversion_and_dispatch(self):
        cc = OpenCC()
        seal = "\U0003ef7a\U0003fbb5"
        cases = [("s2seal", "汉字", seal), ("t2seal", "漢字", seal),
                 ("seal2s", seal, "汉字"), ("seal2t", seal, "漢字")]
        for config, source, expected in cases:
            with self.subTest(config=config):
                self.assertEqual(getattr(cc, config)(source), expected)
                self.assertEqual(cc.get_config(), "s2t")
                converter = OpenCC(OpenccConfig.parse(config.upper()))
                self.assertEqual(converter.convert(source), expected)
                self.assertEqual(getattr(cc, config)(""), "")
                self.assertEqual(getattr(cc, config)("ABC🙂"), "ABC🙂")

    def test_punctuation(self):
        cc = OpenCC()
        seal = cc.t2seal("漢")
        for config, source in [("s2seal", "汉"), ("t2seal", "漢")]:
            self.assertEqual(getattr(cc, config)("“" + source + "”", True), "「" + seal + "」")
        self.assertEqual(cc.seal2s("「" + seal + "」", True), "“汉”")
        self.assertEqual(cc.seal2t("“" + seal + "”", True), "「漢」")

    def test_txt_and_packaged_slots_match(self):
        raw = DictionaryMaxlength.from_dicts()
        packaged = DictionaryMaxlength.from_json()
        for slot in [DictSlot.SealCharacters, DictSlot.SealCharactersRev,
                     DictSlot.SealVariants, DictSlot.SealVariantsRev]:
            self.assertTrue(getattr(packaged, slot.value)[0])
            self.assertEqual(getattr(raw, slot.value), getattr(packaged, slot.value))

    def test_round_order_customization_and_cache(self):
        dictionary = DictionaryMaxlength()
        dictionary.st_characters = ({"s": "t"}, 1)
        dictionary.seal_variants = ({"t": "v"}, 1)
        dictionary.seal_characters_rev = ({"v": "𽀀"}, 1)
        dictionary.seal_characters = ({"𽀀": "v"}, 1)
        dictionary.seal_variants_rev = ({"v": "t"}, 1)
        dictionary.ts_characters = ({"t": "s"}, 1)
        cc = OpenCC(dictionary=dictionary)
        self.assertEqual(cc.s2seal("s"), "𽀀")
        self.assertEqual(cc.t2seal("t"), "𽀀")
        self.assertEqual(cc.seal2s("𽀀"), "s")
        self.assertEqual(cc.seal2t("𽀀"), "t")
        self.assertIs(cc._get_dict_refs("s2seal"), cc._get_dict_refs("s2seal"))
        self.assertIs(cc._get_dict_refs("s2seal").round_2,
                      cc.union_cache.get_union(UnionKey.SealVariantsOnly))
        self.assertIsNone(cc._get_dict_refs("t2seal").round_3)
        self.assertIsNotNone(cc._get_dict_refs("t2seal_punct").round_3)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "custom.txt"
            path.write_text("v\tX\n", encoding="utf-8")
            dictionary.with_custom_dict_files(overrides={DictSlot.SealCharactersRev: path})
            self.assertEqual(OpenCC(dictionary=dictionary).s2seal("s"), "X")

    def test_cli_accepts_seal_config(self):
        result = subprocess.run([sys.executable, "-B", "-m", "opencc_purepy", "convert", "--help"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        for config in ("s2seal", "t2seal", "seal2s", "seal2t"):
            self.assertIn(config, result.stdout)
