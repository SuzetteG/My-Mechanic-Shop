from tests.base import BaseTestCase

class TestAuth(BaseTestCase):

    def test_login_negative_no_user(self):
        res = self.client.post("/customers/login", json={"email": "nope@test.com", "password": "bad"})
        self.assertIn(res.status_code, (400, 401))

    def test_login_positive(self):
        # Create customer first using REQUIRED fields
        self.client.post("/customers/", json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@test.com",
            "phone": "5205551234",
            "password": "Pass123!",
            "address": "123 Main St, Tucson, AZ 85701",
            "dob": "2000-01-01"
        })

        # Then login
        res = self.client.post("/customers/login", json={"email": "jane@test.com", "password": "Pass123!"})

        if res.status_code != 200:
            print("LOGIN FAILED:", res.status_code, res.get_json())

        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("token", data)
