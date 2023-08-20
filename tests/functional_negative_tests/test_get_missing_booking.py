import allure
import requests

from config import settings

BASE_URL = settings.BASE_URL


@allure.feature("Booking")
@allure.story("Validate Retrieving a Booking with Non-Existent ID")
def test_retrieve_nonexistent_booking():
    non_existent_id = 999999

    with allure.step("Trying to retrieve a booking with a non-existent ID"):
        response = requests.get(f"{BASE_URL}/booking/{non_existent_id}")

    with allure.step("Verifying the HTTP status code"):
        assert response.status_code == 404, f"Expected status code 404 for non-existent booking, but got {response.status_code}"

    with allure.step("Verifying the error message"):
        error_data = response.text
        expected_error = "Not Found"
        assert expected_error in error_data, f"Unexpected error message: {error_data}"
