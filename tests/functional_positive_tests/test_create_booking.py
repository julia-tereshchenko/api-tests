import allure
import requests
from voluptuous import Invalid

from config import settings
from schemas.booking_schema import CreateBookingSchema


BASE_URL = settings.BASE_URL


@allure.feature("Booking")
@allure.story("Validate Creation of Booking")
def test_validate_creation_of_booking():
    url = f"{BASE_URL}/booking"
    headers = {"Content-Type": "application/json"}
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

    response = requests.post(url, json=payload, headers=headers)

    with allure.step("Verifying the HTTP status code"):
        assert response.status_code == 200, f"Expected 200 but got {response.status_code}"

    with allure.step("Verifying the Request and Response payload"):
        assert response.json()["booking"] == payload, "Payload data does not match"

    with allure.step("Verifying the content-Type"):
        assert response.headers["Content-Type"] == "application/json; charset=utf-8"

    with allure.step("Verifying the payload size limit"):
        assert len(response.content) < 5 * 1024, "Payload size exceeds limit"

    with allure.step("Verifying the response schema"):
        try:
            CreateBookingSchema(response.json())
        except Invalid as e:
            assert False, f"Response schema validation failed: {e}"
