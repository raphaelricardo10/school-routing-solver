import googlemaps
import os

from routingGA import RoutingGA
from GALib import GALib
from dotenv import load_dotenv
from datetime import datetime as dt
from data import addresses

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

    def directions(self, destination, source, waypoints: 'list[str]'):
        return self.client.directions(
            destination,
            source,
            mode="driving",
            avoid=["highways", "tolls", "ferries"],
            waypoints=waypoints,
            units="metric",
            language="pt-BR",
            region="BR",
        )

    def plot_directions(self, results):
        marker_points = []
        waypoints = []

        # extract the location points from the previous directions function

        for leg in results[0]["legs"]:
            leg_start_loc = leg["start_location"]
            marker_points.append(
                f'{leg_start_loc["lat"]},{leg_start_loc["lng"]}')
            for step in leg["steps"]:
                end_loc = step["end_location"]
                waypoints.append(f'{end_loc["lat"]},{end_loc["lng"]}')
        last_stop = results[0]["legs"][-1]["end_location"]
        marker_points.append(f'{last_stop["lat"]},{last_stop["lng"]}')

        markers = ["color:blue|size:mid|label:" + chr(65+i) + "|"
                   + r for i, r in enumerate(marker_points)]
        result_map = self.client.static_map(
            center=waypoints[0],
            scale=2,
            zoom=13,
            size=[640, 640],
            format="jpg",
            maptype="roadmap",
            markers=markers,
            path="color:0x0000ff|weight:2|" + "|".join(waypoints))

        return result_map


if __name__ == '__main__':
    mapsAPI = MapsAPI(os.getenv('API_KEY'))

    address_chunks = [addresses[x:x+10] for x in range(0, len(addresses), 10)]
    distances = []
    routes = []

    for address_chunk in address_chunks:
        distances += mapsAPI.distance_matrix(address_chunk)
        routes += mapsAPI.directions(address_chunk[0],
                                     address_chunk[-1], address_chunk[1:-1])

    with open('driving_route_map.jpg', 'wb') as img:
        for chunk in mapsAPI.plot_directions(routes):
            img.write(chunk)

    routingGA = RoutingGA(popSize=50, qtyLocations=len(distances) - 1, qtyRoutes=5,
                          maxGenerations=100, selectionK=3, mutationRate=0.05, distances=distances)
    lib = GALib(routingGA=routingGA,
                libPath=os.getenv('LIB_PATH'))

    lib.run()
