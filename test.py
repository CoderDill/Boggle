from unittest import TestCase

from werkzeug.wrappers import response
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self) -> None:
        self.client = app.test_client()
        app.config["TESTING"] = True
        return super().setUp()

    def tearDown(self) -> None:
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

    def checkGuess(self):
        """"""