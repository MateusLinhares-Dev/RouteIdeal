import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.services import GoogleMaps
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def calculate_best_route(origin, destinations, vehicles):
    # Inicializa a API do GoogleMaps
    google_maps = GoogleMaps()

    # Todos os locais incluem a origem e os destinos
    all_locations = [origin] + destinations

    # Obter a matriz de distâncias completa
    distance_matrix = []
    for i in range(len(all_locations)):
        row = []
        for j in range(len(all_locations)):
            if i == j:
                row.append(0)
            else:
                row.append(
                    google_maps.get_localization(all_locations[i], [all_locations[j]])[0][0]
                )
        distance_matrix.append(row)

    # Configura os dados do problema
    data = {}
    data["distance_matrix"] = distance_matrix
    data["num_vehicles"] = vehicles
    data["depot"] = 0

    # Cria o gerenciador de índices de roteamento
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Cria o modelo de roteamento
    routing = pywrapcp.RoutingModel(manager)

    # Cria a função de custo de trânsito
    def distance_callback(from_index, to_index):
        # Converte os índices de roteamento para índices da matriz de distâncias
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define o custo do arco para a função de trânsito
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Define os parâmetros da pesquisa
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Soluciona o problema
    solution = routing.SolveWithParameters(search_parameters)

    # Retorna a solução encontrada
    if solution:
        return get_solution(manager, routing, solution, all_locations)
    else:
        return {"error": "Nenhuma solução encontrada!"}


def get_solution(manager, routing, solution, locations):
    route = []
    index = routing.Start(0)
    total_distance = 0
    while not routing.IsEnd(index):
        route.append(locations[manager.IndexToNode(index)])
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        total_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    route.append(locations[manager.IndexToNode(index)])

    distance_km = round(total_distance / 1000, 2)
    return {
        "route": [[i, rota] for i, rota in enumerate(route)],
        "total_distance": f"{distance_km} Km/h",
    }
