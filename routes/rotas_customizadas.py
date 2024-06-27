from flask import Blueprint, request, jsonify
from route_maps.route_optimizer import calculate_best_route

get_best_route = Blueprint('get_best_route', __name__)

@get_best_route.route('/routes', methods=['POST'])
def get_route():
    data = request.get_json()
    start = data.get('start')
    destinations = data.get('destinations')
    vehicles = data.get('vehicles')

    if not start or not destinations or not vehicles:
        return jsonify({'error': 'Invalid input data'}), 400

    best_route = calculate_best_route(start, destinations, vehicles)
    return jsonify({'best_route': best_route}), 200
