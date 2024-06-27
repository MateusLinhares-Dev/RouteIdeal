import requests


class GoogleApi:

    def __init__(self):
        self.__Google_url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
        self.__api = "AIzaSyD9cjiwDeuVyv71k2T4H0_crfUMVPTfy8Q"

    def get_distance(self, origins, destinations):
        address_str = ""
        for i in range(len(destinations)):
            address_str += destinations[i] + "|"

        url = (
            self.__Google_url
            + "origins="
            + origins
            + "&destinations="
            + address_str
            + "&key="
            + self.__api
        )
        response = requests.get(url)

        return response.json()
