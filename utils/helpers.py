import requests
from random import choice
from config import settings

def get_random_booking_id():
    response = requests.get(f"{settings.BASE_URL}/booking")
    response.raise_for_status()
    booking_ids = [booking["bookingid"] for booking in response.json()]
    return choice(booking_ids)
