from voluptuous import Schema, Match, PREVENT_EXTRA

CreateBookingSchema = Schema(
    {
        "bookingid": int,
        "booking": {
            "firstname": str,
            "lastname": str,
            "totalprice": int,
            "depositpaid": bool,
            "bookingdates": {
                "checkin": Match(r'^\d{4}-\d{2}-\d{2}$'),
                "checkout": Match(r'^\d{4}-\d{2}-\d{2}$')
            },
        "additionalneeds": str,
        }
    },
    extra=PREVENT_EXTRA,
    required=True
)


RetrieveBookingSchema = Schema(
    {
        "firstname": str,
        "lastname": str,
        "totalprice": int,
        "depositpaid": bool,
        "bookingdates": {
            "checkin": Match(r'^\d{4}-\d{2}-\d{2}$'),
            "checkout": Match(r'^\d{4}-\d{2}-\d{2}$')
        },
        "additionalneeds": str
    },
    extra=PREVENT_EXTRA,
    required=True
)
