"""Regression checks for jump generation in hypothetical search positions."""

import copy
from pathlib import Path
import runpy
import sys
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch


def load_game():
    # Load the original callbacks without importing Tkinter or starting a GUI.
    graphics = ModuleType("cmu_112_graphics")
    graphics.copy = copy
    graphics.runApp = lambda **kwargs: None
    source = Path(__file__).resolve().parents[1] / "mying_term_project.py"
    with patch.dict(sys.modules, {"cmu_112_graphics": graphics}):
        return runpy.run_path(str(source))


GAME = load_game()


class JumpStateTests(unittest.TestCase):
    def setUp(self):
        self.app = SimpleNamespace(
            width=600, height=800,
            getUserInput=lambda prompt: "1",
            showMessage=lambda message: None,
        )
        GAME["appStarted"](self.app)
        self.app.board = self.empty_board()
        self.state = self.empty_board()
        self.state[8][6] = 4

    @staticmethod
    def empty_board():
        return [[0] * 15 for _ in range(17)]

    def jumps(self):
        return GAME["getAllJumps"](
            self.app, 8, 6, self.state, self.app.evenMoves
        )

    def test_bridge_added_in_simulation_enables_jump(self):
        self.state[8][7] = 1
        self.assertIn((0, 2), self.jumps())

    def test_bridge_removed_in_simulation_disables_jump(self):
        self.app.board[8][7] = 1
        self.assertNotIn((0, 2), self.jumps())

    def test_legal_moves_include_simulated_jump_without_mutating_boards(self):
        self.state[8][7] = 1
        live_before = copy.deepcopy(self.app.board)
        state_before = copy.deepcopy(self.state)
        moves = GAME["getAllLegalMoves"](self.app, 8, 6, self.state)
        self.assertIn((8, 8), moves)
        self.assertEqual(self.app.board, live_before)
        self.assertEqual(self.state, state_before)

    def test_search_chooses_forward_jump_created_in_simulation(self):
        self.state = self.empty_board()
        self.state[8][6] = 4
        self.state[9][7] = 1
        result = GAME["minimax"](self.app, self.state, 1, 4)
        self.assertEqual(result[:4], [8, 6, 10, 7])


if __name__ == "__main__":
    unittest.main()
