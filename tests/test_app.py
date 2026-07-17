import os
import unittest

os.environ["TESTING"] = "true"

from app import app, mydb, TimelinePost

MODELS = [TimelinePost]


class AppTestCase(unittest.TestCase):
    def setUp(self):
        mydb.bind(MODELS, bind_refs=False, bind_backrefs=False)
        if mydb.is_closed():
            mydb.connect()
        mydb.create_tables(MODELS)
        self.client = app.test_client()

    def tearDown(self):
        mydb.drop_tables(MODELS)


class TestHomePage(AppTestCase):
    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_contains_expected_text(self):
        response = self.client.get("/")
        html = response.get_data(as_text=True)

        # Page title
        self.assertIn("MLH Fellow", html)
        # My name
        self.assertIn("Adora", html)
        # Navigation links
        self.assertIn("Home", html)
        self.assertIn("Hobbies", html)
        self.assertIn("Timeline", html)


class TestTimelineApi(AppTestCase):
    def test_get_timeline_post_empty(self):
        response = self.client.get("/api/timeline_post")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIn("timeline_posts", data)
        self.assertEqual(data["timeline_posts"], [])

    def test_post_and_retrieve_timeline_post(self):
        post_response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "content": "Hello world, I'm John!",
            },
        )
        self.assertEqual(post_response.status_code, 200)

        created = post_response.get_json()
        self.assertEqual(created["name"], "John Doe")
        self.assertEqual(created["email"], "john@example.com")
        self.assertEqual(created["content"], "Hello world, I'm John!")

        get_response = self.client.get("/api/timeline_post")
        self.assertEqual(get_response.status_code, 200)

        posts = get_response.get_json()["timeline_posts"]
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]["name"], "John Doe")
        self.assertEqual(posts[0]["email"], "john@example.com")
        self.assertEqual(posts[0]["content"], "Hello world, I'm John!")


class TestTimelinePage(AppTestCase):
    def test_timeline_page_loads(self):
        response = self.client.get("/timeline")
        self.assertEqual(response.status_code, 200)

        html = response.get_data(as_text=True)
        self.assertIn("Timeline", html)
        self.assertIn("Share an update", html)
        self.assertIn("Recent posts", html)


class TestMalformedTimelinePost(AppTestCase):
    def test_missing_name_returns_400(self):
        response = self.client.post(
            "/api/timeline_post",
            data={
                "email": "john@example.com",
                "content": "Hello world, I'm John!",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid name", response.get_data(as_text=True))

    def test_empty_content_returns_400(self):
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "content": "",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid content", response.get_data(as_text=True))

    def test_invalid_email_returns_400(self):
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "not-an-email",
                "content": "Hello world, I'm John!",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid email", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
