import allure
import requests

from config import settings
from utils.auth import get_auth_token

BASE_URL = settings.BASE_URL


@allure.feature("Booking")
@allure.story("Test Booking Dates Boundary")
def test_booking_dates_boundary():
    token = get_auth_token()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={token}"
    }

    payload = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2023-05-01",
            "checkout": "2023-04-30"
        }
    }

    with allure.step("Trying to create a booking with checkout date before checkin date"):
        response = requests.post(f"{BASE_URL}/booking", json=payload, headers=headers)

    with allure.step("Verifying the HTTP status code"):
        assert response.status_code == 400, f"Expected status code 400 for invalid booking dates, but got {response.status_code}"

    with allure.step("Verifying the error message"):
        error_data = response.text
        expected_error = "checkout date is before checkin"
        assert expected_error in error_data, f"Unexpected error message: {error_data}"
