"""Validate hex geometry, assignment costs, and strategic score behavior."""

import itertools
import random
from types import SimpleNamespace
import unittest

from test_jump_state import GAME


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.app = SimpleNamespace(
            width=600, height=800, getUserInput=lambda _: "1",
            showMessage=lambda _: None,
        )
        GAME["appStarted"](self.app)

    def empty_board(self):
        return [[0] * 15 for _ in range(17)]

    def test_every_neighbor_is_one_hex_step_away(self):
        for row in range(17):
            for col in range(15):
                if not GAME["spotOnBoard"](self.app, row, col):
                    continue
                directions = self.app.oddMoves if row % 2 else self.app.evenMoves
                for dr, dc in directions:
                    self.assertEqual(GAME["hexDistance"](
                        (row, col), (row + dr, col + dc)), 1)

    def test_assignment_agrees_with_brute_force_on_small_matrices(self):
        rng = random.Random(112)
        for n, m in [(1, 3), (2, 3), (3, 3), (4, 4)]:
            for _ in range(20):
                costs = [[rng.randrange(12) for _ in range(m)] for _ in range(n)]
                expected = min(sum(costs[i][j] for i, j in enumerate(columns))
                               for columns in itertools.permutations(range(m), n))
                self.assertEqual(GAME["minimumAssignmentCost"](costs), expected)

    def test_assignment_cannot_reuse_the_same_target(self):
        self.assertEqual(GAME["minimumAssignmentCost"]([[0, 5], [0, 5]]), 5)

    def test_terminal_scores_dominate_nonterminal_positions(self):
        opening = GAME["getValue"](self.app, self.app.board)
        aiWin, humanWin = self.empty_board(), self.empty_board()
        for row, col in self.app.redSpots:
            aiWin[row][col] = 4
        for row, col in self.app.yellowSpots:
            humanWin[row][col] = 1
        self.assertEqual(GAME["getValue"](self.app, aiWin), GAME["WIN_SCORE"])
        self.assertEqual(GAME["getValue"](self.app, humanWin), -GAME["WIN_SCORE"])
        self.assertLess(abs(opening), GAME["WIN_SCORE"])

    def test_columns_matter_even_at_the_same_row(self):
        central, edge = self.empty_board(), self.empty_board()
        central[12][6] = 4
        edge[12][0] = 4
        self.assertGreater(GAME["getValue"](self.app, central),
                           GAME["getValue"](self.app, edge))


if __name__ == "__main__":
    unittest.main()
