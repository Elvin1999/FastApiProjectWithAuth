from models import Role

def test_authors_list(client):
    r=client.get('/api/authors')
    assert r.status_code == 200

def test_create_author_requires_admin(client,normal_user):
    #user login
    token=client.post('/api/auth/login',json={
        'email':'user@gmail.com',"password":"user123"
    }).json()['access_token']

    r=client.post('/api/authors',json={"name":"Mark Twen"},
                  headers={'Authorization':f'Bearer {token}'})

    assert r.status_code == 201