import unittest

from backend.fastapi.app.storage import InMemoryAppStore


class InMemoryAppStoreTests(unittest.TestCase):
    def test_create_and_list_apps(self):
        store = InMemoryAppStore()

        created = store.create_app(name="demo-app", description="demo", owner="alice")

        self.assertEqual(created["name"], "demo-app")
        self.assertEqual(created["owner"], "alice")
        self.assertEqual(store.list_apps(), [created])


if __name__ == "__main__":
    unittest.main()
