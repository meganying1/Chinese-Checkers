"""Check destination triangles and agreement between gameplay and AI wins."""

from types import SimpleNamespace
import unittest

from test_jump_state import GAME


class WinConditionTests(unittest.TestCase):
    def setUp(self):
        self.app = SimpleNamespace(
            width=600, height=800,
            getUserInput=lambda prompt: "6",
            showMessage=lambda message: None,
        )
        GAME["appStarted"](self.app)

    def place_yellow(self, spots):
        yellow = [ball for ball in self.app.balls if ball.player == 4]
        for ball, (row, col) in zip(yellow, sorted(spots)):
            ball.row, ball.col = row, col
        # Keep the simulated board aligned with these yellow positions.
        self.app.board = [[0] * self.app.cols for _ in range(self.app.rows)]
        for ball in yellow:
            self.app.board[ball.row][ball.col] = ball.player

    def test_yellow_wins_in_opposite_red_triangle(self):
        self.place_yellow(self.app.redSpots)
        self.assertTrue(GAME["AIOpponentWins"](self.app, self.app.board))
        self.assertTrue(GAME["yellowWins"](self.app))
        self.assertEqual(self.app.winner, 4)

    def test_yellow_does_not_win_in_blue_triangle(self):
        self.place_yellow(self.app.blueSpots)
        self.assertFalse(GAME["AIOpponentWins"](self.app, self.app.board))
        self.assertFalse(GAME["yellowWins"](self.app))
        self.assertIsNone(self.app.winner)

    def test_yellow_needs_all_ten_pieces_in_target(self):
        spots = self.app.redSpots - {(16, 6)} | {(8, 6)}
        self.place_yellow(spots)
        self.assertFalse(GAME["yellowWins"](self.app))
        self.assertIsNone(self.app.winner)

    def test_game_over_recognizes_yellow_win(self):
        self.place_yellow(self.app.redSpots)
        self.assertTrue(GAME["gameIsOver"](self.app))
        self.assertEqual(self.app.winner, 4)
        self.assertEqual(self.app.currentPlayer, -1)


if __name__ == "__main__":
    unittest.main()
