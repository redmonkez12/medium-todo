import json


def test_create_user(client):
    data = {
        "first_name":"Tomas",
        "last_name":"Svojanovsky",
        "email":"tomas.svojanovsky11@gmail.com",
        "birthdate": "1991-08-09",
        "password": "123456789"
    }
    response = client.post("/api/v1/auth/users",json.dumps(data))
    print(response.json())
    assert response.status_code == 201
    assert response.json() == False
