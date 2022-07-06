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

        #extract the location points from the previous directions function

        for leg in results[0]["legs"]:
            leg_start_loc = leg["start_location"]
            marker_points.append(f'{leg_start_loc["lat"]},{leg_start_loc["lng"]}')
            for step in leg["steps"]:
                end_loc = step["end_location"]
                waypoints.append(f'{end_loc["lat"]},{end_loc["lng"]}')
        last_stop = results[0]["legs"][-1]["end_location"]
        marker_points.append(f'{last_stop["lat"]},{last_stop["lng"]}')
                
        markers = [ "color:blue|size:mid|label:" + chr(65+i) + "|" 
                + r for i, r in enumerate(marker_points)]
        result_map = self.client.static_map(
                        center = waypoints[0],
                        scale=2, 
                        zoom=13,
                        size=[640, 640], 
                        format="jpg", 
                        maptype="roadmap",
                        markers=markers,
                        path="color:0x0000ff|weight:2|" + "|".join(waypoints))

        return result_map


if __name__ == '__main__':
    addresses = ['Externato+Bastos+Silva+RJ',  # depot
                    'Rua Mutuapira, 191, RJ',
                    'Rua Jaime Bittencourt, 336, RJ'
                    'Rua Espedicionário Evilásio Rocha Assis, 85, RJ',
                    'R. João Antônio Leandro, 3473, RJ',
                    'R. Expedicionario Manuel E De Sousa, 414 - Fazenda dos Mineiros, São Gonçalo,',
                    'R. Heitor Rodrigues, 91 - Itaúna',
                    'R. Laura Amélia de Souza, 239, Sao Goncalo',
                    'R. Liborina Silva, 372 - Itaúna',
                    'Estr. da Sapucaia, 694, Sao Goncalo',
                    'R. Santo André, 92-242 - Itaúna',
                    'R. Lopes de Moura, 38 - Nova Cidade',
                    'R. Ives Ribeiro, 110 - Nova Cidade',
                    'R. Petrópolis, 700 - Trindade',
                    'R. Petrópolis, 1189 - Trindade',
                    'Av. José Manna Júnior, 606, Sao Goncalo',
                    'R. Ilhéus, 147 - Trindade',
                    'R. Cuiabá, 661 - Trindade',
                    'R. Itaperuna, 358 - Trindade',
                    'R. Londrina, 104 - Trindade',
                    'Avenida Trindade, 536 - Trindade',
                    'R. Recife, 1609 - Trindade',
                    'R. Uberlândia, 459 - Trindade',
                    'R. Albino de Almeida, 85 - Trindade',
                    'R. Barbacena, 17 - Trindade',
                    'R. Rio de Janeiro, 751-639 - Trindade',
                    'R. Itaocara, 82 - Trindade',
                    'R. Guadalajara, 148-230 - Trindade',
                    'R. Peleuzio Araújo, 59 - Mutua',
                    'R. Manuel Pinheiro, 148 - São Miguel',
                    'R. Peleuzio Araújo, 88 - Mutua',
                ]

    mapsAPI = MapsAPI(os.getenv('API_KEY'))


    address_chunks = [addresses[x:x+10] for x in range(0, len(addresses), 10)]
    distances = []
    routes = []

    for address_chunk in address_chunks:
        distances += mapsAPI.distance_matrix(address_chunk)
        routes += mapsAPI.directions(address_chunk[0], address_chunk[-1], address_chunk[1:-1])

    with open('driving_route_map.jpg', 'wb') as img:
        for chunk in mapsAPI.plot_directions(routes):
            img.write(chunk)

    routingGA = RoutingGA(popSize=50, qtyLocations=len(distances) - 1, qtyRoutes=5,
                        maxGenerations=100, selectionK=3, mutationRate=0.05, distances=distances)
    lib = GALib(routingGA=routingGA,
                libPath=os.getenv('LIB_PATH'))

    lib.run()
