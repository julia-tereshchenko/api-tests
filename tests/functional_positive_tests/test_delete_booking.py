import allure
import requests

from config import settings
from utils.auth import get_auth_token
from utils.helpers import get_random_booking_id

BASE_URL = settings.BASE_URL


@allure.feature("Booking")
@allure.story("Delete a specific booking by ID")
def test_validate_booking_deletion():
    token = get_auth_token()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={token}"
    }

    selected_booking_id = get_random_booking_id()

    with allure.step("Deleting the selected booking"):
        response = requests.delete(f"{BASE_URL}/booking/{selected_booking_id}", headers=headers)
        response.raise_for_status()

    with allure.step("Verifying the HTTP status code for delete operation"):
        assert response.status_code == 201, f"Expected status code 201 for DELETE operation, but got {response.status_code}"

    with allure.step("Verifying the booking was deleted"):
        response = requests.get(f"{BASE_URL}/booking/{selected_booking_id}")
        assert response.status_code == 404, "Booking was not deleted or still accessible."

    with allure.step("Verifying the basic performance of the API"):
        response_time = response.elapsed.total_seconds()
        assert response_time < 2, f"API took longer than 2 seconds. Actual duration: {response_time} seconds"
