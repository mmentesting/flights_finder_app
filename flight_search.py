import requests
from flight_data import FlightData
import os

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
TEQUILA_HEADER = os.environ["TEQUILA_HEADER"]

# Class responsible for talking to Tequila Kiwi API (Flight Search)
class FlightSearch:
    def get_destination_code(self, city):
        headers = {"apikey": TEQUILA_HEADER}
        location_params = {
            "term": city,
            "location_types": "city"
        }
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/locations/query", params=location_params, headers=headers)
        data = response.json()
        city_code = data["locations"][0]["code"]
        return city_code

    def search_flights(self, origin_city, destination_city, tomorrow, six_months):
        headers = {"apikey": TEQUILA_HEADER}
        search_params = {
            "fly_from": origin_city,
            "fly_to": destination_city,
            "date_from": tomorrow,
            "date_to": six_months,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD"
        }
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", params=search_params, headers=headers)
        try:
            data = response.json()["data"][0]
        except IndexError:
            # print(f"No flights found for {destination_city}")
            return None
        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            departure_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0])
        return flight_data
