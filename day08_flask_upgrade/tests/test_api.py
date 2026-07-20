import unittest

from app import app


class Day08ApiTestCase(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SECRET_KEY="day08-test-key")
        self.client = app.test_client()

    def login(self):
        return self.client.post(
            "/login",
            data={"username": "student", "password": "day07"},
            follow_redirects=False,
        )

    def test_health_returns_200_json(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["ok"], True)

    def test_metrics_requires_login(self):
        response = self.client.get("/api/metrics")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_metrics_returns_four_serializable_cards(self):
        self.login()
        response = self.client.get("/api/metrics")
        body = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(body["ok"])
        self.assertEqual(len(body["metrics"]), 4)
        self.assertEqual(set(body["metrics"][0]), {"label", "value", "note"})

    def test_category_filter_returns_only_fashion(self):
        self.login()
        response = self.client.get("/api/categories?category=Fashion")
        body = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["category"], "Fashion")
        self.assertEqual(len(body["rows"]), 1)
        self.assertEqual(body["rows"][0]["偏好品类"], "Fashion")

    def test_empty_question_returns_unified_400_json(self):
        self.login()
        response = self.client.post("/api/ask", json={"question": ""})
        body = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(body["ok"], False)
        self.assertIn("error", body)


if __name__ == "__main__":
    unittest.main(verbosity=2)
