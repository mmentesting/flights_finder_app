from datetime import date, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

ORIGIN_CITY_CODE = "TLV"
TOMORROW = (date.today() + timedelta(days=1)).strftime("%d/%m/%Y")
SIX_MONTHS = (date.today() + timedelta(days=180)).strftime("%d/%m/%Y")

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

if data_manager.destination_data[0]["iataCode"] == "":
    for item in data_manager.destination_data:
        item["iataCode"] = flight_search.get_destination_code(item["city"])
    data_manager.update_city_codes()

for item in data_manager.destination_data:
    flight = flight_search.search_flights(ORIGIN_CITY_CODE, item["iataCode"], TOMORROW, SIX_MONTHS)
    try:
        if flight.price <= item["lowestPrice"]:
            message = f"Subject:Low Price Flight Alert!\n\n" \
                      f"Only ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}!\n" \
                      f"Flight dates from {flight.departure_date} to {flight.return_date}."
            notification_manager.send_mail(message)
    except AttributeError:
        continue
