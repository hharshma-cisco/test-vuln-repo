from app.web import make_app


def test_make_app():
    app = make_app()
    with app.test_client() as client:
        resp = client.get("/")
        assert resp.status_code == 200
        assert b"ok" in resp.data
