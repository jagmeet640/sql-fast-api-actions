import requests
import pytest

@pytest.fixture(scope="session")
def base_url():
    return "http://127.0.0.1:8000/students/"

def test_get_students():
    response = requests.get("http://127.0.0.1:8000/students_read/").json()
    assert len(response) > 1


def test_create_student():
    # Send a POST request to create a student
    response = requests.post("http://127.0.0.1:8000/students/", json={"name": "test", "age": 21, "marks": 95, "rollId":22})
    print(response.json())
    assert response.status_code == 200

def test_update_student():
    response = requests.put("http://127.0.0.1:8000/students_update/", json={"name": "aman", "age": 25, "marks": 100, "rollId": 22})
    print(response.json())
    assert response.status_code == 200

def test_delete_student():
    response = requests.delete("http://127.0.0.1:8000/students/22")
    assert response.status_code == 200