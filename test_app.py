import unittest
import json
import threading
from http.server import HTTPServer
from unittest.mock import patch
import app

class AppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), app.AppHandler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(
            target=cls.server.serve_forever,
            daemon=True
        )
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def request(self, path):
        import urllib.request
        with urllib.request.urlopen(
            f"http://127.0.0.1:{self.port}{path}"
        ) as response:
            return response.status, response.read().decode()

    def test_homepage(self):
        status, body = self.request("/")
        self.assertEqual(status, 200)
        self.assertIn("Week 9 CI/CD Demo", body)

    def test_health_endpoint(self):
        status, body = self.request("/health")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["status"], "healthy")

if __name__ == "__main__":
    unittest.main()
