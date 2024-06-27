import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from repository.repository import GoogleApi


class GoogleMaps:

    def __init__(self):
        self.repository_google = GoogleApi()

    def get_localization(self, origin, destinations):
        origin = str(origin).replace(" ", "+")
        destinations = [str(dest).replace(" ", "+") for dest in destinations]

        max_elements = 100
        num_addresses = len(destinations)
        max_rows = max_elements

        q, r = divmod(num_addresses, max_rows)

        dest_addresses = destinations
        distance_matrix = []
        # Send q requests, returning max_rows rows per request.
        for i in range(q):
            response = self.repository_google.get_distance(origin, dest_addresses)
            distance_matrix += self.build_distance_matrix(response)

        if r > 0:
            response = self.repository_google.get_distance(origin, dest_addresses)
            distance_matrix += self.build_distance_matrix(response)
        return distance_matrix

    def build_distance_matrix(self, response):
        distance_matrix = []
        for row in response["rows"]:
            row_list = [
                row["elements"][j]["distance"]["value"]
                for j in range(len(row["elements"]))
            ]
            distance_matrix.append(row_list)
        return distance_matrix
