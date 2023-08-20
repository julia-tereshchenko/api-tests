import allure
import requests

from config import settings
from schemas.booking_schema import RetrieveBookingSchema
from utils.auth import get_auth_token
from utils.helpers import get_random_booking_id

BASE_URL = settings.BASE_URL


@allure.feature("Booking")
@allure.story("Update a specific booking by ID")
def test_validate_booking_update():
    token = get_auth_token()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={token}"
    }

    selected_booking_id = get_random_booking_id()

    with allure.step("Updating the selected booking"):
        updated_data = {
            "firstname": "Julie",
            "lastname": "Ellis",
            "totalprice": 458,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2023-12-01",
                "checkout": "2023-12-31"
            },
            "additionalneeds": "Breakfast"
        }

        response = requests.put(f"{BASE_URL}/booking/{selected_booking_id}", json=updated_data, headers=headers)
        response.raise_for_status()

    with allure.step("Verifying the booking was updated correctly"):
        response = requests.get(f"{BASE_URL}/booking/{selected_booking_id}")
        response.raise_for_status()
        fetched_data = response.json()

        assert fetched_data["firstname"] == updated_data["firstname"], "First name was not updated correctly"
        assert fetched_data["lastname"] == updated_data["lastname"], "Last name was not updated correctly"
        assert fetched_data["totalprice"] == updated_data["totalprice"], "Total price was not updated correctly"

    with allure.step("Verifying the HTTP status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Verifying the content-type"):
        assert response.headers["Content-Type"] == "application/json; charset=utf-8"

    with allure.step("Verifying the Request and Response payload"):
        RetrieveBookingSchema(fetched_data)

    with allure.step("Verifying the payload size limit"):
        assert len(response.content) < 10000, "Payload size is greater than the expected limit"

    with allure.step("Verifying the basic performance of the API"):
        response_time = response.elapsed.total_seconds()
        assert response_time < 2, f"API took longer than 2 seconds. Actual duration: {response_time} seconds"
