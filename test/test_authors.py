from models import Role


def test_authors_list_public(client):
    r = client.get("/api/authors")
    assert r.status_code == 200


def test_create_author_requires_admin(client, normal_user):
    # user ile login
    token = client.post('/api/auth/login', json={
        "email": "normal@gmail.com",
        "password": "normal123"
    }).json()['access_token']

    r = client.post(
        '/api/authors',
        json={"name": "Test Author"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert r.status_code == 403
