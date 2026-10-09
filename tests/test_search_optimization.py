"""Compare optimized search with an independent exhaustive minimax oracle."""

import copy
import random
from types import SimpleNamespace
import unittest

from test_jump_state import GAME


def exhaustive(app, state, depth, player, count):
    count[0] += 1
    if depth == 0 or GAME["AIGameOver"](app, state):
        return GAME["getValue"](app, state)
    scores = []
    for row in range(app.rows):
        for col in range(app.cols):
            if state[row][col] != player:
                continue
            for (newRow, newCol), path in GAME["getAllTurnMoves"](app, row, col, state):
                child = [line[:] for line in state]
                child[row][col] = 0
                child[newRow][newCol] = player
                scores.append(exhaustive(app, child, depth - 1,
                                         1 if player == 4 else 4, count))
    if not scores:
        return GAME["getValue"](app, state)
    return max(scores) if player == 4 else min(scores)


class SearchOptimizationTests(unittest.TestCase):
    def setUp(self):
        self.app = SimpleNamespace(
            width=600, height=800, getUserInput=lambda _: "1",
            showMessage=lambda _: None,
        )
        GAME["appStarted"](self.app)

    def test_matches_exhaustive_search_for_both_players(self):
        rng = random.Random(112)
        cells = [(row, col) for row in range(17) for col in range(15)
                 if GAME["spotOnBoard"](self.app, row, col)]
        for trial in range(6):
            state = [[0] * 15 for _ in range(17)]
            for (row, col), player in zip(rng.sample(cells, 4), [1, 1, 4, 4]):
                state[row][col] = player
            for player in (1, 4):
                with self.subTest(trial=trial, player=player):
                    expected = exhaustive(self.app, state, 3, player, [0])
                    before = copy.deepcopy(state)
                    result = GAME["minimax"](self.app, state, 3, player)
                    self.assertEqual(result[-1], expected)
                    self.assertEqual(state, before)
                    row, col, newRow, newCol = result[:4]
                    legal = dict(GAME["getAllTurnMoves"](self.app, row, col, state))
                    self.assertIn((newRow, newCol), legal)
                    child = [line[:] for line in state]
                    child[row][col], child[newRow][newCol] = 0, player
                    self.assertEqual(exhaustive(self.app, child, 2,
                                               1 if player == 4 else 4, [0]), expected)

    def test_opening_prunes_nodes_without_changing_score(self):
        count, stats = [0], {}
        expected = exhaustive(self.app, self.app.board, 3, 4, count)
        result = GAME["minimax"](self.app, self.app.board, 3, 4, searchStats=stats)
        self.assertEqual(result[-1], expected)
        self.assertLess(stats["nodes"], count[0])
        self.assertGreater(stats["cutoffs"], 0)
        self.assertGreater(stats["cacheHits"], 0)


if __name__ == "__main__":
    unittest.main()
