import requests
import os

SHEETY_USER = os.environ["SHEETY_USER"]
SHEETY_HEADER = os.environ["SHEETY_HEADER"]
SHEETY_DESTINATION_ENDPOINT = f"https://api.sheety.co/{SHEETY_USER}/flightsDeals/destinations"
headers = {"Authorization": SHEETY_HEADER}

# Class responsible for talking to Shetty API (Google Sheets)
class DataManager:
    def __init__(self):
        self.destination_data = {}
        self.get_destination_data()

    def get_destination_data(self):
        response = requests.get(url=SHEETY_DESTINATION_ENDPOINT, headers=headers)
        data = response.json()
        self.destination_data = data["destinations"]

    def update_city_codes(self):
        for item in self.destination_data:
            city_inputs = {
                "destination": {
                    "iataCode": item["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_DESTINATION_ENDPOINT}/{item['id']}",
                                    json=city_inputs, headers=headers)
