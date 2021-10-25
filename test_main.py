from fastapi.testclient import TestClient
import json

from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health-check")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

def test_add_key():
    # Flush all contents
    client.delete("/store/flush")
    # Add new key

    # Read test json data from file
    f = open('test_data.json',)
    test_payload = json.load(f)
    
    response = client.post(
        "/store",
        json = test_payload,
    )
    assert response.status_code == 200

def test_get_all():
    response = client.get("/store/all")
    assert response.status_code == 200
   

def test_get_key():
    response = client.get("/store?key=name")
    assert response.status_code == 200
    response = response.json()
    assert response["key"] == "name" and response["value"] == "foo"

def test_get_key_absent():
    response = client.get("/store?key=abc")
    assert response.status_code == 404
    assert response.json() == { "detail": "No data found!"}

def test_update():
    payload = {
                "name": "bar", 
                "age": "20", 
                "description": "The Bar Barters"
            }
    response = client.put(
        "/store",
        json = payload,
    )
    assert response.status_code == 200
    response = response.json()
    assert json.loads(response["cache"]["name"]) == "bar"

def test_delete_key():
    response = client.delete("/store?key=name")
    assert response.status_code == 200
    
def test_flush_all():
    response = client.delete("/store/flush")
    assert response.status_code == 200
    assert response.json() == {
                                "message": "Cache cleared",
                                "cache": {}
                                }
   