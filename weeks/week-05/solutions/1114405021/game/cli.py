"""命令列啟動入口（簡化版）。"""

from .game import BigTwoGame


def run_cli() -> None:
    """啟動簡化 CLI，示範如何初始化遊戲。"""
    game = BigTwoGame()
    game.setup()
    print("Big Two CLI 已啟動（簡化模式）")
    print(f"玩家數量: {len(game.players)}")


if __name__ == "__main__":
    run_cli()
