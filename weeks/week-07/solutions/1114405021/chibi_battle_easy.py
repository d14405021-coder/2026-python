from collections import namedtuple, Counter, defaultdict

General = namedtuple('General', ['faction', 'name', 'hp', 'atk', 'def_', 'spd', 'is_leader'])

class ChibiBattleEasy:
    def __init__(self):
        self.generals = {}
        self.stats = {'damage': Counter(), 'losses': defaultdict(int)}
    
    def load_generals(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line == 'EOF' or not line: break
                parts = line.split()
                if len(parts) == 7:
                    self.generals[parts[1]] = General(
                        parts[0], parts[1], int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5]), parts[6] == 'True'
                    )
    
    def simulate_battle(self):
        shu = [g for g in self.generals.values() if g.faction == '蜀']
        wei = [g for g in self.generals.values() if g.faction == '魏']
        for _ in range(3): # 三波
            for i, attacker in enumerate(shu):
                if i < len(wei):
                    dmg = max(1, attacker.atk - wei[i].def_)
                    self.stats['damage'][attacker.name] += dmg
                    self.stats['losses'][wei[i].name] += dmg
