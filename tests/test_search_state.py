"""Search stays independent of live interaction flags; hints remain actionable."""

import copy
from types import SimpleNamespace
import unittest

from test_jump_state import GAME


class SearchStateTests(unittest.TestCase):
    def setUp(self):
        self.app = SimpleNamespace(
            width=600, height=800, getUserInput=lambda _: "1",
            showMessage=lambda _: None,
        )
        GAME["appStarted"](self.app)
        self.app.board = [[0] * 15 for _ in range(17)]
        self.app.balls = set()

    def test_search_ignores_live_jump_and_game_over_flags(self):
        self.app.board[8][6] = 4
        self.app.board[9][7] = 1
        expected = GAME["minimax"](self.app, self.app.board, 1, 4)
        self.app.isJumping = True
        self.app.gameOver = True
        self.assertEqual(GAME["minimax"](self.app, self.app.board, 1, 4), expected)

    def test_mid_jump_hint_selects_same_piece_and_next_hop(self):
        self.app.board[8][6] = 1
        self.app.board[7][6] = 4
        self.app.board[5][5] = 4
        self.app.selection = (8, 6)
        self.app.isJumping = True
        before = copy.deepcopy(self.app.board)
        GAME["givePlayerHint"](self.app)
        self.assertTrue(self.app.givingHint)
        self.assertEqual(self.app.hintBall, (8, 6))
        self.assertEqual(self.app.hintLocation, (6, 5))
        self.assertFalse(self.app.hintEndTurn)
        self.assertEqual(self.app.board, before)

    def test_mid_jump_hint_can_recommend_ending_turn(self):
        self.app.board[8][6] = 1
        self.app.selection = (8, 6)
        self.app.isJumping = True
        GAME["givePlayerHint"](self.app)
        self.assertTrue(self.app.givingHint)
        self.assertTrue(self.app.hintEndTurn)
        self.assertEqual(self.app.hintLocation, (8, 6))

    def test_no_move_returns_finite_score_and_no_hint(self):
        result = GAME["minimax"](self.app, self.app.board, 3, 4)
        self.assertEqual(result[:4], [-1] * 4)
        self.assertEqual(result[-1], GAME["getValue"](self.app, self.app.board))
        GAME["givePlayerHint"](self.app)
        self.assertFalse(self.app.givingHint)

    def test_turn_change_clears_jump_restriction(self):
        self.app.isJumping = True
        self.app.selection = (8, 6)
        GAME["changePlayer"](self.app)
        self.assertFalse(self.app.isJumping)
        self.assertEqual(self.app.selection, (-1, -1))

    def test_clicking_hint_during_jump_preserves_the_turn(self):
        self.app.board[8][6] = 1
        self.app.board[7][6] = 4
        self.app.board[5][5] = 4
        self.app.selection = (8, 6)
        self.app.isJumping = True
        event = SimpleNamespace(x=self.app.width * 5 / 6, y=self.app.height / 12)
        GAME["mousePressed"](self.app, event)
        self.assertTrue(self.app.givingHint)
        self.assertTrue(self.app.isJumping)
        self.assertEqual(self.app.currentPlayer, 1)
        self.assertEqual(self.app.selection, (8, 6))

    def test_restart_button_works_after_game_over(self):
        self.app.gameOver = True
        event = SimpleNamespace(x=self.app.width / 2,
                                y=self.app.height * 14 / 15)
        GAME["mousePressed"](self.app, event)
        self.assertFalse(self.app.gameOver)
        self.assertEqual(len(self.app.balls), 20)


if __name__ == "__main__":
    unittest.main()
