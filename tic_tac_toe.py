#!/usr/bin/env python3
"""
井字棋游戏 - 完整实现
支持双人对战模式
"""

import copy
from typing import Optional, Tuple, List


class Board:
    """棋盘类，管理棋盘状态"""

    EMPTY = " "
    PLAYER_X = "X"
    PLAYER_O = "O"
    BOARD_SIZE = 3

    def __init__(self):
        """初始化3x3空棋盘"""
        self._grid = [[self.EMPTY for _ in range(self.BOARD_SIZE)]
                      for _ in range(self.BOARD_SIZE)]

    def is_empty(self, row: int, col: int) -> bool:
        """检查指定位置是否为空"""
        return self._grid[row][col] == self.EMPTY

    def place_marker(self, row: int, col: int, marker: str) -> bool:
        """在指定位置放置棋子，成功返回True"""
        if not self._is_valid_position(row, col):
            return False
        if not self.is_empty(row, col):
            return False
        self._grid[row][col] = marker
        return True

    def remove_marker(self, row: int, col: int) -> bool:
        """移除指定位置的棋子，成功返回True"""
        if not self._is_valid_position(row, col):
            return False
        self._grid[row][col] = self.EMPTY
        return True

    def _is_valid_position(self, row: int, col: int) -> bool:
        """检查坐标是否在棋盘范围内"""
        return 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE

    def check_winner(self) -> Optional[str]:
        """检查是否有获胜者，返回获胜棋子标记或None"""
        # 检查行
        for row in range(self.BOARD_SIZE):
            if self._check_line(self._grid[row]):
                return self._grid[row][0]

        # 检查列
        for col in range(self.BOARD_SIZE):
            line = [self._grid[row][col] for row in range(self.BOARD_SIZE)]
            if self._check_line(line):
                return line[0]

        # 检查对角线
        line1 = [self._grid[i][i] for i in range(self.BOARD_SIZE)]
        if self._check_line(line1):
            return line1[0]

        line2 = [self._grid[i][self.BOARD_SIZE - 1 - i] for i in range(self.BOARD_SIZE)]
        if self._check_line(line2):
            return line2[0]

        return None

    def _check_line(self, line: List[str]) -> bool:
        """检查一条线是否被同一玩家占据"""
        return (line[0] != self.EMPTY and
                all(marker == line[0] for marker in line))

    def is_full(self) -> bool:
        """检查棋盘是否已满"""
        return all(self._grid[row][col] != self.EMPTY
                   for row in range(self.BOARD_SIZE)
                   for col in range(self.BOARD_SIZE))

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """获取所有空位坐标列表"""
        return [(row, col)
                for row in range(self.BOARD_SIZE)
                for col in range(self.BOARD_SIZE)
                if self._grid[row][col] == self.EMPTY]

    def save_state(self) -> dict:
        """保存棋盘状态（只保存棋盘相关状态）"""
        return {
            'grid': copy.deepcopy(self._grid),
            'board_size': self.BOARD_SIZE
        }

    def load_state(self, state: dict):
        """加载棋盘状态"""
        self._grid = state['grid']

    def display(self):
        """显示棋盘"""
        print("\n   0   1   2")
        for row in range(self.BOARD_SIZE):
            print(f"{row}  ", end="")
            for col in range(self.BOARD_SIZE):
                print(f"{self._grid[row][col]}", end="")
                if col < self.BOARD_SIZE - 1:
                    print(" | ", end="")
            print()
            if row < self.BOARD_SIZE - 1:
                print("  ---+---+---")


class MoveHistory:
    """移动历史记录类"""

    def __init__(self):
        self._history = []

    def add_move(self, row: int, col: int, marker: str):
        """记录一步移动"""
        self._history.append({
            'row': row,
            'col': col,
            'marker': marker
        })

    def undo_last_move(self) -> Optional[dict]:
        """撤销上一步移动，返回被撤销的移动信息"""
        if not self._history:
            return None
        return self._history.pop()

    def get_last_move(self) -> Optional[dict]:
        """获取上一步移动信息（不移除）"""
        if not self._history:
            return None
        return self._history[-1]

    def clear(self):
        """清空历史"""
        self._history.clear()

    def is_empty(self) -> bool:
        """检查历史是否为空"""
        return len(self._history) == 0

    def get_all_moves(self) -> List[dict]:
        """获取所有历史记录（为保存游戏状态提供接口）"""
        return [move.copy() for move in self._history]


class Player:
    """玩家类"""

    def __init__(self, name: str, marker: str):
        self.name = name
        self.marker = marker


class Game:
    """游戏主类，管理游戏流程"""

    def __init__(self, player1_name: str = "玩家1", player2_name: str = "玩家2"):
        self.board = Board()
        self.history = MoveHistory()
        self.player1 = Player(player1_name, Board.PLAYER_X)
        self.player2 = Player(player2_name, Board.PLAYER_O)
        self.current_player = self.player1
        self.game_over = False
        self.winner = None

    def switch_player(self):
        """切换当前玩家"""
        self.current_player = (self.player2
                              if self.current_player == self.player1
                              else self.player1)

    def make_move(self, row: int, col: int) -> bool:
        """执行一步移动，成功返回True"""
        if self.game_over:
            print("游戏已结束，无法继续下棋")
            return False

        if not self.board.place_marker(row, col, self.current_player.marker):
            return False

        self.history.add_move(row, col, self.current_player.marker)

        # 检查游戏状态
        winner = self.board.check_winner()
        if winner:
            self.game_over = True
            self.winner = (self.player1 if winner == self.player1.marker
                          else self.player2)
        elif self.board.is_full():
            self.game_over = True
            self.winner = None  # 平局

        return True

    def undo_move(self) -> bool:
        """撤销上一步移动，成功返回True"""
        if self.history.is_empty():
            print("没有可以撤销的步骤")
            return False

        if self.game_over:
            self.game_over = False
            self.winner = None

        last_move = self.history.undo_last_move()
        self.board.remove_marker(last_move['row'], last_move['col'])

        # 切换回上一步的玩家
        self.switch_player()

        return True

    def is_game_over(self) -> bool:
        """检查游戏是否结束"""
        return self.game_over

    def get_current_player(self) -> Player:
        """获取当前玩家"""
        return self.current_player

    def display_status(self):
        """显示当前游戏状态"""
        print(f"\n当前玩家: {self.current_player.name} ({self.current_player.marker})")
        self.board.display()
        if self.game_over:
            if self.winner:
                print(f"\n🎉 {self.winner.name} 获胜！")
            else:
                print("\n🤝 平局！")

    def save_game_state(self) -> dict:
        """保存完整的游戏状态"""
        return {
            'board': self.board.save_state(),
            'current_player_name': self.current_player.name,
            'current_player_marker': self.current_player.marker,
            'game_over': self.game_over,
            'winner_name': self.winner.name if self.winner else None,
            'history': self.history.get_all_moves()  # 通过公有方法获取历史
        }


class DisplayManager:
    """显示管理类"""

    @staticmethod
    def show_welcome():
        """显示欢迎信息"""
        print("=" * 40)
        print("         井字棋游戏")
        print("=" * 40)
        print("游戏规则：")
        print("- 两名玩家轮流在3x3棋盘上落子")
        print("- 先连成一条线（横、竖、斜）者获胜")
        print("- 棋盘满无人获胜则为平局")
        print()

    @staticmethod
    def show_commands():
        """显示可用命令"""
        print("游戏命令：")
        print("  row col  - 在(row, col)位置落子（如: 1 2）")
        print("  undo     - 撤销上一步")
        print("  quit     - 退出游戏")
        print()

    @staticmethod
    def show_game_info(game: Game):
        """显示游戏信息"""
        print(f"玩家 {game.player1.name} ({game.player1.marker}) vs "
              f"玩家 {game.player2.name} ({game.player2.marker})")

    @staticmethod
    def show_error(message: str):
        """显示错误信息"""
        print(f"❌ 错误: {message}")

    @staticmethod
    def show_success(message: str):
        """显示成功信息"""
        print(f"✅ {message}")


class GameController:
    """游戏控制器，处理用户输入和游戏流程"""

    def __init__(self):
        self.display = DisplayManager()
        self.game: Optional[Game] = None

    def start_game(self):
        """开始新的游戏"""
        self.display.show_welcome()

        # 获取玩家名字
        player1_name = input("请输入玩家1的名字（X）: ").strip() or "玩家1"
        player2_name = input("请输入玩家2的名字（O）: ").strip() or "玩家2"

        self.game = Game(player1_name, player2_name)
        self.display.show_game_info(self.game)
        self.display.show_commands()

        self._game_loop()

    def _game_loop(self):
        """游戏主循环"""
        while not self.game.is_game_over():
            self.game.display_status()

            command = input(f"\n{self.game.get_current_player().name} 请输入: ").strip()

            if command.lower() == 'quit':
                print("游戏结束")
                return
            elif command.lower() == 'undo':
                if self.game.undo_move():
                    self.display.show_success("已撤销上一步")
                continue

            # 解析坐标
            try:
                parts = command.split()
                if len(parts) != 2:
                    self.display.show_error("请输入两个数字，如: 1 2")
                    continue

                row, col = int(parts[0]), int(parts[1])

                # 验证坐标范围
                if not (0 <= row < Board.BOARD_SIZE and 0 <= col < Board.BOARD_SIZE):
                    self.display.show_error(f"坐标必须在0-{Board.BOARD_SIZE-1}之间")
                    continue

                # 执行移动
                if self.game.make_move(row, col):
                    if not self.game.is_game_over():
                        self.game.switch_player()
                else:
                    self.display.show_error("该位置已有棋子，请重新选择")

            except ValueError:
                self.display.show_error("请输入有效的数字坐标")
            except Exception as e:
                self.display.show_error(f"发生错误: {e}")

        # 游戏结束显示结果
        self.game.display_status()

    def play_again(self) -> bool:
        """询问是否再玩一局"""
        while True:
            choice = input("\n是否再玩一局？(y/n): ").strip().lower()
            if choice == 'y':
                return True
            elif choice == 'n':
                return False
            else:
                print("请输入 y 或 n")


def main():
    """主函数"""
    controller = GameController()

    while True:
        controller.start_game()
        if not controller.play_again():
            print("\n感谢游玩！再见！")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n游戏被中断")
    except Exception as e:
        print(f"\n程序发生未预期错误: {e}")
