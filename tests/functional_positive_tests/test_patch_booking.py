import allure
import requests

from config import settings
from utils.auth import get_auth_token
from utils.helpers import get_random_booking_id

BASE_URL = settings.BASE_URL


@allure.feature("Booking")
@allure.story("Partial Update of a specific booking by ID")
def test_partial_update_booking():
    token = get_auth_token()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={token}"
    }

    selected_booking_id = get_random_booking_id()

    response = requests.get(f"{BASE_URL}/booking/{selected_booking_id}")
    response.raise_for_status()
    original_data = response.json()

    with allure.step("Partial updating the selected booking"):
        partial_data = {
            "firstname": "UpdatedFirstName"
        }

        response = requests.patch(f"{BASE_URL}/booking/{selected_booking_id}", json=partial_data, headers=headers)
        response.raise_for_status()

    with allure.step("Verifying the booking was partially updated"):
        response = requests.get(f"{BASE_URL}/booking/{selected_booking_id}")
        response.raise_for_status()
        fetched_data = response.json()

        assert fetched_data["firstname"] == partial_data["firstname"], "First name was not updated correctly"

        for key in original_data.keys():
            if key != "firstname":
                assert fetched_data[key] == original_data[key], f"{key} should not have changed but did."

    with allure.step("Verifying the HTTP status code for PATCH operation"):
        assert response.status_code == 200, f"Expected status code 200 for PATCH operation, but got {response.status_code}"

    with allure.step("Verifying the content-type"):
        assert response.headers["Content-Type"] == "application/json; charset=utf-8"

    with allure.step("Verifying the payload size limit"):
        assert len(response.content) < 10000, "Payload size is greater than the expected limit"

    with allure.step("Verifying the basic performance of the API"):
        response_time = response.elapsed.total_seconds()
        assert response_time < 2, f"API took longer than 2 seconds. Actual duration: {response_time} seconds"
