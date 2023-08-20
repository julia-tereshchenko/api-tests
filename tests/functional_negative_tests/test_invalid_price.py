import allure
import requests

from config import settings
from utils.auth import get_auth_token

BASE_URL = settings.BASE_URL


@allure.feature("Booking")
@allure.story("Test Invalid Total Price Value")
def test_invalid_total_price():
    token = get_auth_token()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={token}"
    }

    payload = {
        "firstname": "Andy",
        "lastname": "Long",
        "totalprice": -111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2023-05-01",
            "checkout": "2023-05-02"
        }
    }

    with allure.step("Trying to create a booking with invalid total price"):
        response = requests.post(f"{BASE_URL}/booking", json=payload, headers=headers)

    with allure.step("Verifying the HTTP status code"):
        assert response.status_code == 400, f"Expected status code 400 for invalid total price, but got {response.status_code}"

    with allure.step("Verifying the error message"):
        error_data = response.text
        expected_error = "invalid total price value"
        assert expected_error in error_data, f"Unexpected error message: {error_data}"
