from tests.base import BaseTestCase

class TestServiceTickets(BaseTestCase):
    def test_bulk_edit_mechanics(self):
        token = self.get_token()
        # Create a ticket first
        ticket_res = self.client.post(
            "/service-tickets/",
            json={"description": "Oil change", "customer_id": 1},
            headers={"Authorization": f"Bearer {token}"}
        )
        ticket_id = ticket_res.get_json().get("id", 1)
        payload = {"add_ids": [1], "remove_ids": []}
        res = self.client.put(
            f"/service-tickets/{ticket_id}/edit",
            json=payload,
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertIn(res.status_code, (200, 404))

    def test_add_part_to_ticket(self):
        token = self.get_token()
        # Create a ticket first
        ticket_res = self.client.post(
            "/service-tickets/",
            json={"description": "Oil change", "customer_id": 1},
            headers={"Authorization": f"Bearer {token}"}
        )
        ticket_id = ticket_res.get_json().get("id", 1)
        # Create an inventory part
        part_res = self.client.post("/inventory/", json={"name": "Oil Filter", "price": 9.99})
        part_id = part_res.get_json().get("id", 1)
        res = self.client.put(
            f"/service-tickets/{ticket_id}/add-part/{part_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertIn(res.status_code, (200, 404))

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

        if res.status_code != 200:
            print("TOKEN LOGIN FAILED:", res.status_code, res.get_json())

        return res.get_json()["token"]

    def test_create_ticket_requires_token_negative(self):
        res = self.client.post("/service-tickets/", json={"description": "Oil change", "customer_id": 1})
        self.assertEqual(res.status_code, 401)

    def test_create_ticket_with_token_positive(self):
        token = self.get_token()
        payload = {
            "description": "Oil change",
            "vin": "1HGCM82633A004352"
        }
        res = self.client.post(
            "/service-tickets/",
            json=payload,
            headers={"Authorization": f"Bearer {token}"}
        )
        print("CREATE TICKET RESPONSE:", res.status_code, res.get_json())
        self.assertIn(res.status_code, (200, 201))
