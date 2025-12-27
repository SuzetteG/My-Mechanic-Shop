from tests.base import BaseTestCase

class TestInventory(BaseTestCase):

    def test_get_inventory(self):
        res = self.client.get("/inventory/")
        self.assertEqual(res.status_code, 200)

        data = res.get_json()
        # could be [] initially
        self.assertTrue(isinstance(data, list))

    def test_create_inventory_positive(self):
        payload = {"name": "Oil Filter", "price": 9.99, "quantity": 10}
        res = self.client.post("/inventory/", json=payload)

        if res.status_code not in (200, 201):
            print("CREATE INVENTORY FAILED:", res.status_code, res.get_json())

        self.assertIn(res.status_code, (200, 201))

        data = res.get_json()
        # If your API returns created object
        if isinstance(data, dict):
            self.assertIn("name", data)

    def test_create_inventory_negative_missing_field(self):
        payload = {"name": "Oil Filter", "quantity": 10}  # missing price
        res = self.client.post("/inventory/", json=payload)
        self.assertEqual(res.status_code, 400)

    def test_update_inventory_positive(self):
        # create first
        create = self.client.post("/inventory/", json={"name": "Oil Filter", "price": 9.99, "quantity": 10})
        self.assertIn(create.status_code, (200, 201))
        created = create.get_json()
        item_id = created.get("id") if isinstance(created, dict) else None

        # if your API returns ID differently, print and adjust
        if not item_id:
            print("CREATE INVENTORY RESPONSE (no id found):", created)
            self.fail("Inventory create did not return an id field")

        res = self.client.put(f"/inventory/{item_id}", json={"name": "Oil Filter XL", "price": 12.50, "quantity": 5})

        if res.status_code != 200:
            print("UPDATE INVENTORY FAILED:", res.status_code, res.get_json())

        self.assertEqual(res.status_code, 200)

    def test_delete_inventory_positive(self):
        create = self.client.post("/inventory/", json={"name": "Oil Filter", "price": 9.99, "quantity": 10})
        self.assertIn(create.status_code, (200, 201))
        created = create.get_json()
        item_id = created.get("id") if isinstance(created, dict) else None

        if not item_id:
            print("CREATE INVENTORY RESPONSE (no id found):", created)
            self.fail("Inventory create did not return an id field")

        res = self.client.delete(f"/inventory/{item_id}")

        if res.status_code != 200:
            print("DELETE INVENTORY FAILED:", res.status_code, res.get_json())

        self.assertEqual(res.status_code, 200)
