from backend.fastapi.app import storage


def test_create_and_list_apps():
    store = storage.InMemoryAppStore()

    created = store.create_app(
        name="demo-app",
        description="demo",
        owner="alice",
    )

    assert created["name"] == "demo-app"
    assert created["owner"] == "alice"
    assert store.list_apps() == [created]
