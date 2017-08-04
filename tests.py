import unittest

from party import app
from model import db, example_data, connect_to_db


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        """Do before tests."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Test to show homepage is correct."""

        result = self.client.get("/")
        self.assertIn("board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):
        """Test to show we see the RSVP form, but NOT the party details."""

        result = self.client.get("/")
        self.assertIn("Please RSVP", result.data)
        self.assertNotIn("Party Details", result.data)

    def test_rsvp(self):
        """Test to show that when RSVP, party details are shown, but not the RSVP form"""
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)

        self.assertIn("Party Details", result.data)
        self.assertNotIn("Please RSVP", result.data)


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = "key"

        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = 1

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_games(self):
        """Test that the games page displays the game from example_data()."""

        result = self.client.get("/games")
        self.assertIn("Splendor", result.data)
        self.assertIn("Card based where you try to accumulate", result.data)




if __name__ == "__main__":
    unittest.main()
