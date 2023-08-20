import time

import allure
import requests
from voluptuous import Invalid

from config import settings
from schemas.booking_schema import RetrieveBookingSchema
from utils.helpers import get_random_booking_id

BASE_URL = settings.BASE_URL


@allure.feature("Booking")
@allure.story("Retrieve a Specific Booking by ID")
def test_retrieve_random_booking_by_id():
    selected_booking_id = get_random_booking_id()

    url = f"{BASE_URL}/booking/{selected_booking_id}"

    with allure.step("Sending GET request to fetch the booking"):
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        response_time = end_time - start_time

    with allure.step("Verifying the HTTP status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Verifying the content-type is JSON"):
        assert "application/json" in response.headers["Content-Type"]

    with allure.step("Verifying the basic performance of the API"):
        assert response_time < 2, f"API took longer than 2 seconds. Actual duration: {response_time} seconds"

    with allure.step("Verifying the response payload"):
        try:
            RetrieveBookingSchema(response.json())
        except Invalid as e:
            assert False, f"Response schema validation failed: {e}"
