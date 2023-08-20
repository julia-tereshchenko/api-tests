import allure
import requests

from config import settings

BASE_URL = settings.BASE_URL


@allure.feature("Booking")
@allure.story("Create Booking with Missing Required Fields")
def test_create_booking_missing_fields():
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    booking_data = {
        "firstname": "James",
        "totalprice": 123,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2023-01-01",
            "checkout": "2023-01-10"
        },
        "additionalneeds": "Breakfast"
    }

    with allure.step("Attempt to create a booking with missing required fields"):
        response = requests.post(f"{BASE_URL}/booking", json=booking_data, headers=headers)

        assert response.status_code != 200, "API allowed creation of booking with missing required fields."

    with allure.step("Verifying the content-type"):
        assert response.headers["Content-Type"] == "text/plain; charset=utf-8"

    with allure.step("Verifying the Request and Response payload"):
        error_text = response.text
        assert "Internal Server Error" in error_text, f"Unexpected error message: {error_text}"

    with allure.step("Verifying the payload size limit"):
        assert len(response.content) < 10000, "Payload size is greater than the expected limit."

    with allure.step("Verifying the basic performance of the API"):
        response_time = response.elapsed.total_seconds()
        assert response_time < 2, f"API took longer than 2 seconds. Actual duration: {response_time} seconds"
