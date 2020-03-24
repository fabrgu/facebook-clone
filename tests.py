import unittest

from views import app

class FacebookCloneTests(unittest.TestCase):
    """ Tests for facebook clone site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index_route(self):
        result = self.client.get("/")
        self.assertIn(b'<h3>Sign up</h3>', result.data)


if __name__ == "__main__":
    unittest.main()