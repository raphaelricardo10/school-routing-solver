import googlemaps
import os
import itertools
import pickle
import numpy as np

from routingGA import RoutingGA
from GALib import GALib
from dotenv import load_dotenv
from datetime import datetime as dt
from data import addresses

load_dotenv()

class Destination:
    def __init__(self, address: str, distance: int) -> None:
        self.address = address
        self.distance = distance


class MapsAPI:
    def __init__(self, key: str) -> None:
        self.key = key
        self.client = googlemaps.Client(key)

    def distance_matrix(self, source, destination):
        response = self.client.distance_matrix(
            source,
            destination,
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

    def split_distance_request(chunks: list, shouldCache = True):
        distances = {}
        for address_chunk in address_chunks:
            for source, destinations in address_chunk.items():
                result = mapsAPI.distance_matrix(source, destinations)

                if source not in distances:
                    distances[source] = []

                distances[source] += result

        if shouldCache:
            with open('distanceData.txt', 'wb') as file:
                pickle.dump(distances, file)

        return distances

    def get_from_cache():
        with open('distanceData.txt', 'rb') as f:
            return pickle.load(f)

    def join_distance_matrix(chunks: 'dict[str, list[str]]'):
        distances = []
        for chunk in chunks.values():
            fullChunk = []
            for chunkPart in chunk:
                fullChunk += chunkPart[0]
            
            fullChunk.insert(0, 0)
            distances.append(fullChunk)

        distances.append([0])

        return distances

    def flatten_distance_matrix(distances: 'dict[str, list[str]]'):
        flattened_distances = []
        for x in distances:
            flattened_distances += x

        return flattened_distances

    def convert_to_symmetric(distances: 'list[list[int]]'):
        distances = MapsAPI.join_distance_matrix(distances)
        n = len(distances)

        flattened = MapsAPI.flatten_distance_matrix(distances)

        sym_distances = np.zeros((n,n)) # Initialize nxn matrix
        triu = np.triu_indices(n) # Find upper right indices of a triangular nxn matrix
        tril = np.tril_indices(n, -1) # Find lower left indices of a triangular nxn matrix
        sym_distances[triu] = flattened # Assign list values to upper right matrix
        sym_distances[tril] = sym_distances.T[tril] # Make the matrix symmetric

        return sym_distances

    def save_to_image(routes):
        with open('driving_route_map.jpg', 'wb') as img:
            for chunk in mapsAPI.plot_directions(routes):
                img.write(chunk)

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

    def split_in_chunks(data: list, chunkSize):
        combinations = [x for x in itertools.combinations(addresses, 2)]
        count = 0
        chunks = []
        chunk = {}
        chunks.append(chunk)

        for element in combinations:
            if count >= chunkSize:
                chunk = {}
                chunks.append(chunk)
                count = 0

            if(element[0]) not in chunk:
                chunk[element[0]] = []
                count += 1

            chunk[element[0]].append(element[1])
            count += 1

        return chunks


if __name__ == '__main__':
    mapsAPI = MapsAPI(os.getenv('API_KEY'))

    address_chunks = MapsAPI.split_in_chunks(addresses, 25)
    distances = MapsAPI.split_distance_request(address_chunks) if os.getenv('GET_DISTANCES', False) else MapsAPI.get_from_cache()
    distances = MapsAPI.convert_to_symmetric(distances)

    routingGA = RoutingGA(popSize=50, qtyLocations=len(distances) - 1, qtyRoutes=5,
                          maxGenerations=100, selectionK=3, mutationRate=0.05, distances=distances)
    lib = GALib(routingGA=routingGA,
                libPath=os.getenv('LIB_PATH'))

    lib.run()
