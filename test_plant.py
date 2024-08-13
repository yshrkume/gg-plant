import unittest
import requests


class PlantServiceTest(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5003"

    def test_create_plant(self):
        response = requests.post(
            f"{self.BASE_URL}/plants",
            json={
                "name": "Test Plant",
                "purchase_date": "2024-08-12",
                "light_conditions": "Indirect sunlight",
                "watering_frequency": "weekly",
                "fertilizing_frequency": "monthly",
                "notes": "This is a test plant.",
                "user_id": 1000,
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("Plant created successfully", response.json().get("message", ""))

    def test_get_plants(self):
        response = requests.get(f"{self.BASE_URL}/plants?user_id=1000")
        self.assertEqual(response.status_code, 200)

    def test_update_plant(self):
        response = requests.post(
            f"{self.BASE_URL}/plants",
            json={
                "name": "Test Plant",
                "purchase_date": "2024-08-12",
                "light_conditions": "Indirect sunlight",
                "watering_frequency": "weekly",
                "fertilizing_frequency": "monthly",
                "notes": "This is a test plant.",
                "user_id": 1000,
            },
        )
        plant_id = response.json()["plant_id"]
        response = requests.put(
            f"{self.BASE_URL}/plants/{plant_id}",
            json={
                "name": "Updated Plant",
                "purchase_date": "2024-08-12",
                "light_conditions": "Direct sunlight",
                "watering_frequency": "daily",
                "fertilizing_frequency": "weekly",
                "notes": "This is an updated plant.",
                "user_id": 1000,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Plant updated successfully", response.json().get("message", ""))

    def test_delete_plant(self):
        response = requests.post(
            f"{self.BASE_URL}/plants",
            json={
                "name": "Test Plant",
                "purchase_date": "2024-08-12",
                "light_conditions": "Indirect sunlight",
                "watering_frequency": "weekly",
                "fertilizing_frequency": "monthly",
                "notes": "This is a test plant.",
                "user_id": 1000,
            },
        )
        plant_id = response.json()["plant_id"]
        response = requests.delete(f"{self.BASE_URL}/plants/{plant_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Plant deleted successfully", response.json().get("message", ""))


if __name__ == "__main__":
    unittest.main()
