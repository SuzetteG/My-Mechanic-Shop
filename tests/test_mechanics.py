
from tests.base import BaseTestCase

class TestMechanics(BaseTestCase):
	def test_get_mechanics(self):
		res = self.client.get("/mechanics/")
		self.assertEqual(res.status_code, 200)

	def test_get_mechanics_leaderboard(self):
		res = self.client.get("/mechanics/most-worked")
		self.assertEqual(res.status_code, 200)
