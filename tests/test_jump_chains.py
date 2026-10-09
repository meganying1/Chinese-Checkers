"""Full-turn reachability and queued AI animation regressions."""

import copy
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from test_jump_state import GAME


class JumpChainTests(unittest.TestCase):
    def setUp(self):
        self.app = SimpleNamespace(
            width=600, height=800, getUserInput=lambda _: "1",
            showMessage=lambda _: None,
        )
        GAME["appStarted"](self.app)
        self.app.board = [[0] * 15 for _ in range(17)]
        self.app.balls = set()
        self.app.AIBalls = []
        for row, col, player, color in [
            (8, 6, 4, "yellow"), (9, 7, 1, "red"), (11, 8, 1, "red")
        ]:
            GAME["createBall"](self.app, row, col, player, color)

    def test_chain_reaches_two_hops_with_a_legal_path(self):
        before = copy.deepcopy(self.app.board)
        turns = dict(GAME["getAllTurnMoves"](self.app, 8, 6, before))
        self.assertEqual(turns[(12, 8)], ((10, 7), (12, 8)))
        self.assertEqual(self.app.board, before)

    def test_cycles_cannot_return_to_origin_or_duplicate_destinations(self):
        turns = GAME["getAllTurnMoves"](self.app, 8, 6, self.app.board)
        destinations = [destination for destination, path in turns]
        self.assertNotIn((8, 6), destinations)
        self.assertEqual(len(destinations), len(set(destinations)))
        for destination, path in turns:
            self.assertEqual(len(path), len(set(path)))

    def test_search_treats_chain_as_one_turn(self):
        result = GAME["minimax"](self.app, self.app.board, 1, 4)
        self.assertEqual(result[:4], [8, 6, 12, 8])

    def test_ai_animates_each_hop_before_changing_players(self):
        self.app.currentPlayer = 4
        globals_ = GAME["moveAI"].__globals__
        with patch.dict(globals_, minimax=lambda *args: [8, 6, 12, 8, 0]):
            GAME["moveAI"](self.app)
        ball = self.app.aiBall
        self.assertEqual((ball.newRow, ball.newCol), (10, 7))
        for _ in range(10):
            GAME["timerFired"](self.app)
        self.assertEqual((ball.row, ball.col), (10, 7))
        self.assertEqual((ball.newRow, ball.newCol), (12, 8))
        self.assertEqual(self.app.currentPlayer, 4)
        for _ in range(10):
            GAME["timerFired"](self.app)
        self.assertEqual((ball.row, ball.col), (12, 8))
        self.assertEqual(self.app.currentPlayer, 1)
        self.assertFalse(self.app.isJumping)
        self.assertEqual(self.app.board[8][6], 0)
        self.assertEqual(self.app.board[10][7], 0)
        self.assertEqual(self.app.board[12][8], 4)


if __name__ == "__main__":
    unittest.main()
