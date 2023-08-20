import allure
import requests

from config import settings
from utils.auth import get_auth_token

BASE_URL = settings.BASE_URL


@allure.feature("Booking")
@allure.story("Validate Update with Invalid Booking ID")
def test_update_with_invalid_id():
    invalid_id = 999999
    token = get_auth_token()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={token}"
    }

    payload = {
        "firstname": "Julia",
        "lastname": "Ter",
        "totalprice": 257,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2023-12-01",
            "checkout": "2023-12-02"
        },
        "additionalneeds": "Breakfast"
    }

    with allure.step("Trying to update a booking with an invalid ID"):
        response = requests.put(f"{BASE_URL}/booking/{invalid_id}", json=payload, headers=headers)

    with allure.step("Verifying the HTTP status code"):
        assert response.status_code == 405, f"Expected status code 405 for update with invalid ID, but got {response.status_code}"

    with allure.step("Verifying the error message"):
        error_data = response.text
        expected_error = "Method Not Allowed"
        assert expected_error in error_data, f"Unexpected error message: {error_data}"
