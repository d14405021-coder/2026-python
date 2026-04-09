import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from solution.chibi_battle import ChibiBattle


class TestDataLoading(unittest.TestCase):
    """Stage 1: 資料讀取測試。"""

    def setUp(self):
        self.game = ChibiBattle()
        self.data_file = ROOT / "generals.txt"

    def test_load_generals_from_file(self):
        self.game.load_generals(self.data_file)
        self.assertEqual(len(self.game.generals), 9)
        self.assertIn("劉備", self.game.generals)
        self.assertIn("曹操", self.game.generals)

    def test_parse_general_attributes(self):
        self.game.load_generals(self.data_file)
        general = self.game.generals["關羽"]
        self.assertEqual(general.name, "關羽")
        self.assertEqual(general.atk, 28)
        self.assertEqual(general.def_, 14)
        self.assertEqual(general.spd, 85)
        self.assertEqual(general.faction, "蜀")

    def test_faction_distribution(self):
        self.game.load_generals(self.data_file)
        factions = {faction: 0 for faction in ["蜀", "吳", "魏"]}
        for general in self.game.generals.values():
            factions[general.faction] += 1
        self.assertEqual(factions["蜀"], 3)
        self.assertEqual(factions["吳"], 3)
        self.assertEqual(factions["魏"], 3)

    def test_eof_parsing(self):
        self.game.load_generals(self.data_file)
        self.assertEqual(len(self.game.generals), 9)


class TestBattleLogic(unittest.TestCase):
    """Stage 2: 戰鬥模擬與統計測試。"""

    def setUp(self):
        self.game = ChibiBattle()
        self.game.load_generals(ROOT / "generals.txt")

    def test_battle_order_by_speed(self):
        battle_order = self.game.get_battle_order()
        self.assertEqual(battle_order[0].spd, 85)
        self.assertEqual(battle_order[-1].spd, 60)

    def test_calculate_damage(self):
        damage = self.game.calculate_damage("關羽", "夏侯惇")
        self.assertEqual(damage, 28 - 14)

    def test_damage_counter_accumulation(self):
        self.game.calculate_damage("關羽", "夏侯惇")
        self.game.calculate_damage("關羽", "曹操")
        self.assertEqual(self.game.stats["damage"]["關羽"], 28)

    def test_simulate_one_wave(self):
        self.game.simulate_wave(1)
        self.assertGreater(sum(self.game.stats["damage"].values()), 0)

    def test_simulate_three_waves(self):
        self.game.simulate_battle()
        shu_wu_damage = sum(
            damage
            for general_name, damage in self.game.stats["damage"].items()
            if self.game.generals[general_name].faction in ["蜀", "吳"]
        )
        wei_damage = sum(
            damage
            for general_name, damage in self.game.stats["damage"].items()
            if self.game.generals[general_name].faction == "魏"
        )
        self.assertGreater(shu_wu_damage, wei_damage)

    def test_troop_loss_tracking(self):
        self.game.simulate_battle()
        self.assertGreater(self.game.stats["losses"]["夏侯惇"], 0)

    def test_damage_ranking_most_common(self):
        self.game.simulate_battle()
        ranking = self.game.get_damage_ranking()
        damages = [damage for _, damage in ranking]
        self.assertEqual(damages, sorted(damages, reverse=True))

    def test_faction_damage_stats(self):
        self.game.simulate_battle()
        faction_stats = self.game.get_faction_stats()
        self.assertGreater(faction_stats["蜀"], 0)
        self.assertGreater(faction_stats["吳"], 0)
        self.assertGreater(faction_stats["魏"], 0)

    def test_defeated_generals(self):
        self.game.simulate_battle()
        defeated = self.game.get_defeated_generals()
        self.assertGreater(len(defeated), 0)


class TestRefactoring(unittest.TestCase):
    """Stage 3: 重構與輸出測試。"""

    def setUp(self):
        self.game = ChibiBattle()
        self.game.load_generals(ROOT / "generals.txt")

    def test_stats_unchanged_after_refactor(self):
        self.game.simulate_battle()
        damage_before = dict(self.game.stats["damage"])
        losses_before = dict(self.game.stats["losses"])

        with io.StringIO() as buffer, redirect_stdout(buffer):
            self.game.print_battle_start()
            self.game.print_damage_report()

        self.assertEqual(dict(self.game.stats["damage"]), damage_before)
        self.assertEqual(dict(self.game.stats["losses"]), losses_before)

    def test_all_stage1_tests_still_pass(self):
        self.game.load_generals(ROOT / "generals.txt")
        self.assertEqual(len(self.game.generals), 9)

    def test_all_stage2_tests_still_pass(self):
        self.game.simulate_battle()
        ranking = self.game.get_damage_ranking()
        self.assertGreater(len(ranking), 0)
        self.assertLessEqual(len(ranking), 5)

    def test_run_full_battle_outputs_report(self):
        with io.StringIO() as buffer, redirect_stdout(buffer):
            self.game.run_full_battle()
            output = buffer.getvalue()

        self.assertIn("赤壁戰役", output)
        self.assertIn("傷害統計報告", output)
        self.assertGreater(len(output.strip()), 0)


if __name__ == "__main__":
    unittest.main()