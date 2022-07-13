import googlemaps
import itertools
import pickle
import numpy as np

from datetime import datetime as dt
from data.addresses import addresses

class Destination:
    def __init__(self, address: str, distance: int) -> None:
        self.address = address
        self.distance = distance


class MapsAPI:
    def __init__(self, key: str) -> None:
        self.key = key
        self.client = googlemaps.Client(key)

    def distance_matrix(self, source, destination, calculateTime = False):
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

        metric = 'duration' if calculateTime else 'distance'

        for row in response['rows']:
            distances.append([x[metric]['value'] for x in row['elements']])

        return distances

    def split_distance_request(self, chunks: list, shouldCache = True, calculateTime = False):
        distances = {}
        for address_chunk in chunks:
            for source, destinations in address_chunk.items():
                result = self.distance_matrix(source, destinations)

                if source not in distances:
                    distances[source] = []

                distances[source] += result

        if shouldCache:
            with open('cache/distance_matrix', 'wb') as file:
                pickle.dump(distances, file)

        return distances

    def get_from_cache():
        with open('cache/distance_matrix', 'rb') as f:
            return pickle.load(f)

    def join_distance_matrix(chunks: 'dict[str, list[str]]'):
        distances = []
        for chunk in chunks.values():
            fullChunk = []
            for chunkPart in chunk:
                fullChunk += chunkPart
            
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

        sym_distances = np.zeros((n,n), dtype=np.int32) # Initialize nxn matrix
        triu = np.triu_indices(n) # Find upper right indices of a triangular nxn matrix
        tril = np.tril_indices(n, -1) # Find lower left indices of a triangular nxn matrix
        sym_distances[triu] = flattened # Assign list values to upper right matrix
        sym_distances[tril] = sym_distances.T[tril] # Make the matrix symmetric

        return sym_distances

    def save_to_image(self, routes, filename):
        with open(f'images/{filename}.jpg', 'wb') as img:
            for chunk in self.plot_directions(routes):
                img.write(chunk)

    def split_directions_request(self, locations, maxLen = 26):
        locations = locations[:] + [locations[0]]
        chunks = [locations[x-1:x+maxLen] for x in range(1, len(locations), maxLen)]
        
        responses = []
        for chunk in chunks:
            responses.append(self.directions(chunk[-1], chunk[0], chunk[1: -1]))

        full_directions = responses[0]

        for response in responses:
            full_directions[0]['legs'] += [x for x in response[0]['legs']]

        return full_directions
            

    def directions(self, destination, source, waypoints: 'list[str]'):
        return self.client.directions(
            source,
            destination,
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
            zoom=14,
            size=[640, 640],
            format="jpg",
            maptype="roadmap",
            markers=markers,
            style={"feature": "poi|visibility:off"},
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