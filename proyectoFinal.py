from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# API key for Google Maps Distance Matrix API
GOOGLE_MAPS_API_KEY = "AIzaSyDytpSLPygjIvXWahgD6BABOeMx6VUTQqU"

def get_distance(city1, city2):
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={city1}&destinations={city2}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        if data['status'] == 'OK' and 'rows' in data and len(data['rows']) > 0:
            elements = data['rows'][0]['elements']
            if len(elements) > 0 and 'distance' in elements[0] and 'value' in elements[0]['distance']:
                return elements[0]['distance']['value'] / 1000  # Distance in kilometers
    return float('inf')

def hill_climbing(start, destination):
    current_city = start
    route = [current_city]
    total_distance = 0

    while current_city != destination:
        min_distance = float('inf')
        next_city = None

        # Explore neighbors (other cities)
        for city in [c for c in [destination, 'Guadalajara', 'Monterrey', 'Puebla', 'Ciudad de México'] if c != current_city]:
            distance = get_distance(current_city, city)
            if distance < min_distance:
                min_distance = distance
                next_city = city

        if next_city:
            route.append(next_city)
            total_distance += min_distance
            current_city = next_city
        else:
            break

    return route, total_distance

@app.route('/')
def index():
    return render_template('indexx.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    start = request.form['start']
    destination = request.form['destination']
    optimal_route, total_distance = hill_climbing(start, destination)
    return render_template('indexx.html', route=' -> '.join(optimal_route), distance=total_distance)

if __name__ == '__main__':
    app.run(debug=True)
