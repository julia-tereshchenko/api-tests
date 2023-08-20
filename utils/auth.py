import requests
from config import settings

def get_auth_token():
    response = requests.post(f"{settings.BASE_URL}/auth", json={"username": "admin", "password": "password123"})
    if response.status_code == 200:
        return response.json().get("token")
    else:
        raise ValueError("Failed to get auth token.")

