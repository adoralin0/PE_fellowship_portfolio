import os
import unittest

os.environ["TESTING"] = "true"

from peewee import SqliteDatabase

from app import TimelinePost

MODELS = [TimelinePost]

test_db = SqliteDatabase(":memory:")


class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_timeline_post(self):
        first_post = TimelinePost.create(
            name="John Doe", email="john@example.com", content="Hello world, I'm John!"
        )
        second_post = TimelinePost.create(
            name="Jane Doe", email="jane@example.com", content="Hello world, I'm Jane!"
        )

        posts = list(TimelinePost.select().order_by(TimelinePost.id))

        self.assertEqual(len(posts), 2)

        self.assertEqual(posts[0].name, "John Doe")
        self.assertEqual(posts[1].name, "Jane Doe")

        self.assertEqual(posts[0].email, "john@example.com")
        self.assertEqual(posts[1].email, "jane@example.com")

        self.assertEqual(posts[0].content, "Hello world, I'm John!")
        self.assertEqual(posts[1].content, "Hello world, I'm Jane!")


if __name__ == "__main__":
    unittest.main()
