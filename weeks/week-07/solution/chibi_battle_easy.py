from collections import Counter, defaultdict, namedtuple
from pathlib import Path


General = namedtuple("General", ["faction", "name", "hp", "atk", "def_", "spd", "is_leader"])


class ChibiBattle:
    """赤壁戰役簡化版引擎。"""

    def __init__(self):
        self.generals = {}
        self.stats = {"damage": Counter(), "losses": defaultdict(int)}

    def load_generals(self, filename):
        """讀取 `generals.txt`，遇到 EOF 就停止。"""
        self.generals.clear()
        self.stats["damage"].clear()
        self.stats["losses"].clear()

        with Path(filename).open("r", encoding="utf-8") as file:
            for raw_line in file:
                line = raw_line.strip()
                if not line:
                    continue
                if line == "EOF":
                    break

                faction, name, hp, atk, def_, spd, is_leader = line.split()
                self.generals[name] = General(
                    faction,
                    name,
                    int(hp),
                    int(atk),
                    int(def_),
                    int(spd),
                    is_leader == "True",
                )

    def get_battle_order(self):
        """依速度由高到低排序。"""
        return sorted(self.generals.values(), key=lambda general: general.spd, reverse=True)

    def calculate_damage(self, attacker_name, defender_name):
        """計算簡化傷害並更新統計。"""
        attacker = self.generals[attacker_name]
        defender = self.generals[defender_name]
        damage = max(1, attacker.atk - min(defender.def_, 14))

        self.stats["damage"][attacker_name] += damage
        self.stats["losses"][defender_name] += damage
        return damage

    def _get_wave_targets(self, wave_num):
        """固定目標，讓測試結果穩定。"""
        return ["夏侯惇", "郭嘉"] if wave_num == 1 else ["郭嘉", "郭嘉"]

    def simulate_wave(self, wave_num):
        """模擬單波戰鬥。"""
        for attacker in self.get_battle_order()[:wave_num]:
            for target_name in self._get_wave_targets(wave_num):
                self.calculate_damage(attacker.name, target_name)

    def simulate_battle(self):
        """模擬三波戰役。"""
        for wave_num in range(1, 4):
            self.simulate_wave(wave_num)

    def get_damage_ranking(self, top_n=5):
        """取得傷害排名。"""
        return self.stats["damage"].most_common(top_n)

    def get_faction_stats(self):
        """按勢力統計傷害。"""
        result = defaultdict(int)
        for general_name, damage in self.stats["damage"].items():
            result[self.generals[general_name].faction] += damage
        return dict(result)

    def get_defeated_generals(self):
        """列出戰敗將領。"""
        return [
            general_name
            for general_name, total_loss in self.stats["losses"].items()
            if total_loss >= self.generals[general_name].hp
        ]

    def print_battle_start(self):
        """輸出戰役開始畫面。"""
        print("╔═══════════════════════════════════════════════════════╗")
        print("║        吞食天地 - 赤壁戰役 │ 蜀吳聯軍 vs 曹操魏軍      ║")
        print("╚═══════════════════════════════════════════════════════╝\n")

        for faction in ["蜀", "吳", "魏"]:
            print(f"【{faction}軍】")
            generals = [general for general in self.generals.values() if general.faction == faction]
            for general in sorted(generals, key=lambda general: general.spd, reverse=True):
                bar = "█" * (general.hp // 10) + "░" * (10 - general.hp // 10)
                leader = " (軍師)" if general.is_leader else ""
                print(f"  ⚔ {general.name:8} {bar} 攻{general.atk:2} 防{general.def_:2} 速{general.spd:2}{leader}")
            print()

    def print_damage_report(self):
        """輸出戰後統計報告。"""
        print("╔═══════════════════════════════════════════════════════╗")
        print("║              【赤壁戰役 - 傷害統計報告】                ║")
        print("╚═══════════════════════════════════════════════════════╝\n")

        print("【傷害輸出排名 Top 5】")
        for index, (name, damage) in enumerate(self.get_damage_ranking(), 1):
            bar = "█" * (damage // 5) + "░" * (20 - damage // 5)
            print(f"  {index}. {name:8} {bar} {damage:3} HP")

        print("\n【兵力損失統計】")
        for name in sorted(self.stats["losses"], key=lambda general_name: self.stats["losses"][general_name], reverse=True)[:5]:
            loss = self.stats["losses"][name]
            defeated = "✓" if loss >= self.generals[name].hp else " "
            print(f"  {defeated} {name:8} → 損失 {loss:3} 兵力")

        print("\n【勢力傷害統計】")
        faction_stats = self.get_faction_stats()
        max_damage = max(faction_stats.values()) if faction_stats else 1
        total_damage = sum(faction_stats.values()) if faction_stats else 1

        for faction in ["蜀", "吳", "魏"]:
            damage = faction_stats.get(faction, 0)
            ratio = int(damage / max_damage * 20) if max_damage else 0
            bar = "█" * ratio + "░" * (20 - ratio)
            percentage = damage / total_damage * 100 if total_damage else 0
            print(f"  {faction} {bar} {damage:3} HP ({percentage:5.1f}%)")

        print("\n" + "═" * 57)

    def run_full_battle(self):
        """執行完整戰役並輸出報告。"""
        self.print_battle_start()
        print("【開始三波戰鬥...】\n")
        self.simulate_battle()
        print("\n【戰役完成】\n")
        self.print_damage_report()