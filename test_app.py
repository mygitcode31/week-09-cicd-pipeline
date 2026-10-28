"""Unit tests for the Engineering the Empire timeline app."""
import json
import unittest

from app import APP_VERSION, MILESTONES, render_timeline, route_response


class TimelineAppTests(unittest.TestCase):
    def test_homepage_returns_html(self):
        status, content_type, body = route_response("/")
        self.assertEqual(status, 200)
        self.assertIn("text/html", content_type)
        self.assertIn("Engineering the Empire", body)
        self.assertIn("The chapters that", body)

    def test_health_returns_json(self):
        status, content_type, body = route_response("/health")
        self.assertEqual(status, 200)
        self.assertIn("application/json", content_type)
        payload = json.loads(body)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["version"], APP_VERSION)

    def test_timeline_contains_milestones(self):
        page = render_timeline()
        self.assertGreaterEqual(len(MILESTONES), 6)
        self.assertIn("Mechanical Engineering", page)
        self.assertIn("Python", page)
        self.assertIn("Product Design Engineer", page)

    def test_unknown_path_returns_404(self):
        status, content_type, body = route_response("/does-not-exist")
        self.assertEqual(status, 404)
        self.assertEqual(body, "Not found")


if __name__ == "__main__":
    unittest.main(verbosity=2)
