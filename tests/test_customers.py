from tests.base import BaseTestCase

class TestCustomers(BaseTestCase):
    def get_token(self):
        self.client.post("/customers/", json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@test.com",
            "phone": "5205551234",
            "password": "Pass123!",
            "address": "123 Main St, Tucson, AZ 85701",
            "dob": "2000-01-01"
        })
        res = self.client.post("/customers/login", json={"email": "jane@test.com", "password": "Pass123!"})
        return res.get_json()["token"]

    def test_get_customers_pagination(self):
        # Create multiple customers
        for i in range(7):
            payload = {
                "first_name": f"Jane{i}",
                "last_name": "Doe",
                "email": f"jane{i}@test.com",
                "phone": f"52055512{i:02d}",
                "password": "Pass123!",
                "address": f"{i} Main St, Tucson, AZ 85701",
                "dob": "2000-01-01"
            }
            self.client.post("/customers/", json=payload)
        res = self.client.get("/customers/?page=1&per_page=5")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(isinstance(data, list))
        self.assertLessEqual(len(data), 5)

    def test_get_my_tickets_requires_token(self):
        res = self.client.get("/customers/my-tickets")
        self.assertEqual(res.status_code, 401)

    def test_get_my_tickets_with_token(self):
        token = self.get_token()
        res = self.client.get("/customers/my-tickets", headers={"Authorization": f"Bearer {token}"})
        self.assertIn(res.status_code, (200, 404))

    def test_get_customers(self):
        res = self.client.get("/customers/")
        self.assertEqual(res.status_code, 200)

    def test_create_customer_positive(self):
        payload = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@test.com",
            "phone": "5205551234",
            "password": "Pass123!",
            "address": "123 Main St, Tucson, AZ 85701",
            "dob": "2000-01-01"
        }
        res = self.client.post("/customers/", json=payload)

        # helpful debug if it fails
        if res.status_code not in (200, 201):
            print("CREATE CUSTOMER FAILED:", res.status_code, res.get_json())

        self.assertIn(res.status_code, (200, 201))

    def test_create_customer_negative_missing_field(self):
        payload = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@test.com",
            "phone": "5205551234",
            # missing password
            "address": "123 Main St, Tucson, AZ 85701",
            "dob": "2000-01-01"
        }
        res = self.client.post("/customers/", json=payload)
        self.assertEqual(res.status_code, 400)
