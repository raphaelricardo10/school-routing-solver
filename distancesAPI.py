import googlemaps
import os

from routingGA import RoutingGA
from GALib import GALib
from dotenv import load_dotenv
from datetime import datetime as dt

load_dotenv()

class MapsAPI:
    def __init__(self, key: str) -> None:
        self.key = key
        self.client = googlemaps.Client(key)

    def distance_matrix(self, addresses):
        response = self.client.distance_matrix(
                    addresses,
                    addresses,
                    mode="driving",
                    language="pt-BR",
                    avoid="tolls",
                    units="metric",
                    departure_time=dt.now(),
                    traffic_model="optimistic",
        )

        distances = []

        for row in response['rows']:
            distances.append([x['distance']['value'] for x in row['elements']])
        return distances


if __name__ == '__main__':
    addresses = ['Externato+Bastos+Silva+RJ',  # depot
                    'Rua+Mutuapira+191+RJ',
                    'Rua+Joao+Laborde+183+RJ',
                    'Rua+Jaime+Bitencourt+336+RJ',
                ]

    mapsAPI = MapsAPI(os.getenv('API_KEY'))

    distances = mapsAPI.distance_matrix(addresses)

    print(distances)

    routingGA = RoutingGA(popSize=200, qtyLocations=15, qtyRoutes=5,
                        maxGenerations=100, selectionK=3, mutationRate=0.65, distances=distances)
    lib = GALib(routingGA=routingGA,
                libPath=os.getenv('LIB_PATH'))

    lib.run()
