"""井字棋游戏单元测试"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tic_tac_toe import Board, Game, Player


class TestBoard:
    """棋盘核心逻辑测试"""

    def test_init_board_empty(self):
        board = Board()
        assert board.is_empty(0, 0)
        assert board.is_empty(2, 2)

    def test_place_marker(self):
        board = Board()
        assert board.place_marker(1, 1, "X")
        assert not board.is_empty(1, 1)
        assert board._grid[1][1] == "X"

    def test_cannot_place_on_occupied(self):
        board = Board()
        board.place_marker(0, 0, "X")
        assert not board.place_marker(0, 0, "O")

    def test_check_winner_row(self):
        board = Board()
        board.place_marker(0, 0, "X")
        board.place_marker(0, 1, "X")
        board.place_marker(0, 2, "X")
        assert board.check_winner() == "X"

    def test_check_winner_col(self):
        board = Board()
        board.place_marker(0, 0, "O")
        board.place_marker(1, 0, "O")
        board.place_marker(2, 0, "O")
        assert board.check_winner() == "O"

    def test_check_winner_diag(self):
        board = Board()
        board.place_marker(0, 0, "X")
        board.place_marker(1, 1, "X")
        board.place_marker(2, 2, "X")
        assert board.check_winner() == "X"

    def test_check_winner_anti_diag(self):
        board = Board()
        board.place_marker(0, 2, "O")
        board.place_marker(1, 1, "O")
        board.place_marker(2, 0, "O")
        assert board.check_winner() == "O"

    def test_no_winner(self):
        board = Board()
        board.place_marker(0, 0, "X")
        board.place_marker(1, 1, "O")
        assert board.check_winner() is None

    def test_is_full(self):
        board = Board()
        for r in range(3):
            for c in range(3):
                board._grid[r][c] = "X"
        assert board.is_full()

    def test_is_not_full(self):
        board = Board()
        assert not board.is_full()

    def test_get_empty_cells(self):
        board = Board()
        board.place_marker(0, 0, "X")
        cells = board.get_empty_cells()
        assert len(cells) == 8
        assert (0, 0) not in cells


class TestGame:
    """游戏逻辑测试"""

    def test_game_init(self):
        game = Game("A", "B")
        assert game.current_player.name == "A"
        assert game.current_player.marker == "X"
        assert not game.game_over

    def test_switch_player(self):
        game = Game("A", "B")
        assert game.current_player.name == "A"
        game.switch_player()
        assert game.current_player.name == "B"
        game.switch_player()
        assert game.current_player.name == "A"

    def test_make_move(self):
        game = Game("A", "B")
        assert game.make_move(0, 0)
        assert not game.board.is_empty(0, 0)

    def test_invalid_move(self):
        game = Game("A", "B")
        game.make_move(0, 0)
        assert not game.make_move(0, 0)

    def test_winner_detected(self):
        game = Game("A", "B")
        game.make_move(0, 0)  # A: X at (0,0)
        game.switch_player()
        game.make_move(1, 0)  # B: O at (1,0)
        game.switch_player()
        game.make_move(0, 1)  # A: X at (0,1)
        game.switch_player()
        game.make_move(1, 1)  # B: O at (1,1)
        game.switch_player()
        game.make_move(0, 2)  # A: X at (0,2) → wins
        assert game.game_over
        assert game.winner.name == "A"

    def test_undo_move(self):
        game = Game("A", "B")
        game.make_move(0, 0)
        assert not game.board.is_empty(0, 0)
        assert game.undo_move()
        assert game.board.is_empty(0, 0)

    def test_draw(self):
        """模拟平局：双方填满棋盘无人获胜"""
        game = Game("A", "B")
        # 手动构造平局棋盘（无任何三连）
        # X O X
        # O O X
        # X X O
        board_state = [
            ["X", "O", "X"],
            ["O", "O", "X"],
            ["X", "X", "O"],
        ]
        game.board._grid = board_state
        game.game_over = True
        game.winner = None
        assert game.is_game_over()
        assert game.winner is None
