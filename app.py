from flask import Flask, render_template, request, redirect, url_for
from tomtom_geocoding import get_coordinates
from tomtom_routing import get_route
from map_visualize import plot_route
import os
import folium

app = Flask(__name__)

# Global history and index
route_history = []
current_index = -1

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/route', methods=['POST'])
def route():
    global current_index, route_history

    locations = []
    for i in range(1, 5):
        location = request.form.get(f'location{i}')
        if location:
            coords = get_coordinates(location)
            if coords:
                locations.append(coords)
            else:
                return f"❌ Could not geocode: {location}"

    if len(locations) < 2:
        return "⚠️ Please enter at least two valid locations."

    print("🔵 Getting route from TomTom API...")
    summary, route_points = get_route(locations)

    if route_points:
        plot_route(route_points)
        if os.path.exists("static/route_map.html"):
            print("✅ Map saved successfully.")
        
        distance = round(summary['lengthInMeters'] / 1000, 2)
        duration = round(summary['travelTimeInSeconds'] / 60, 2)

        # Add new route to history and update index
        route_history.append({
            'distance': distance,
            'duration': duration
        })
        current_index = len(route_history) - 1

        return render_template('maps.html', distance=distance, duration=duration,
                               has_prev=current_index > 0,
                               has_next=current_index < len(route_history) - 1)
    
    return "❌ Failed to fetch route."

@app.route('/next')
def next_route():
    global current_index
    if current_index < len(route_history) - 1:
        current_index += 1

    data = route_history[current_index]
    return render_template('maps.html',
                           distance=data['distance'],
                           duration=data['duration'],
                           has_prev=current_index > 0,
                           has_next=current_index < len(route_history) - 1)

@app.route('/prev')
def prev_route():
    global current_index
    if current_index > 0:
        current_index -= 1

    data = route_history[current_index]
    return render_template('maps.html',
                           distance=data['distance'],
                           duration=data['duration'],
                           has_prev=current_index > 0,
                           has_next=current_index < len(route_history) - 1)

if __name__ == '__main__':
    app.run(debug=True, port=5050)
