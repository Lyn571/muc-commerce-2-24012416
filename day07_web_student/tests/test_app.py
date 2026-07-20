import unittest

from app import app


class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SECRET_KEY="test-key")
        self.client = app.test_client()

    def login(self):
        return self.client.post(
            "/login",
            data={"username": "student", "password": "day07"},
            follow_redirects=False,
        )

    def test_correct_login_redirects_to_dashboard(self):
        response = self.login()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith("/dashboard"))

    def test_unauthenticated_dashboard_is_blocked(self):
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_authenticated_dashboard_returns_200(self):
        self.login()
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn("5,630".encode(), response.data)

    def test_api_ask_returns_data_backed_json(self):
        self.login()
        response = self.client.post("/api/ask", json={"question": "总体流失率是多少？"})
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertTrue(body["ok"])
        self.assertIn("16.8%", body["answer"])

    def test_category_filter_and_download(self):
        self.login()
        response = self.client.get("/dashboard?category=Fashion")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Fashion", response.data)
        download = self.client.get("/download?category=Fashion")
        self.assertEqual(download.status_code, 200)
        text = download.data.decode("utf-8-sig")
        self.assertIn("Fashion", text)
        self.assertNotIn("Mobile Phone", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
