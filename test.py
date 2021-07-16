from unittest import TestCase
from werkzeug.wrappers import response
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self) -> None:
        """Before Every Test"""
        self.client = app.test_client()
        app.config["TESTING"] = True
        return super().setUp()

    def tearDown(self) -> None:
        """After Every Test"""
        return super().tearDown()

    def boggleHome(self):
        """Check page load and session data"""

        with self.client:
            response = self.client.get("/")
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('num_of_plays'))
            self.assertIn(b"<form", response.data)
            self.assertIn(b'<b class="score"', response.data)
            self.assertIn(b'<b class="timer"', response.data)

    def checkGuessNotOnBoard(self):
        """Check Guess is NOT on board"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [
                    ['U', 'F', 'P', 'D', 'A'],
                    ['A', 'X', 'N', 'X', 'L'],
                    ['A', 'B', 'F', 'A', 'U'],
                    ['N', 'T', 'N', 'M', 'S'],
                    ['O', 'R', 'L', 'W', 'L']]
        self.client.get('/')
        response = self.client.get('/enter-guess?guess=thunder')
        self.assertEqual(response.json['result'], 'not-on-board')

    def checkGuessNotEnglish(self):
        """Check Guess"""

        self.client.get('/')
        response = self.client.get('/enter-guess?guess=elskhdie')
        self.assertEqual(response.json['result'], 'not-word')

    def checkGuessOk(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [
                    ['U', 'F', 'P', 'D', 'A'],
                    ['A', 'X', 'N', 'X', 'L'],
                    ['A', 'B', 'F', 'A', 'U'],
                    ['N', 'T', 'N', 'M', 'S'],
                    ['O', 'R', 'L', 'W', 'L']]
        response = self.client.get("/enter-guess?guess=no")
        self.assertEqual(response.json['result'], 'ok')
