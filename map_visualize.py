import folium
from tomtom_geocoding import reverse_geocode

def plot_route(points, filename="static/route_map.html"):
    print("🔸 Creating map with start and end markers only...")
    m = folium.Map(location=points[0], zoom_start=6)

    # Only geocode and mark the start point
    start_lat, start_lon = points[0]
    start_label = reverse_geocode(start_lat, start_lon)
    folium.Marker(
        location=(start_lat, start_lon),
        popup=f"Start: {start_label}",
        icon=folium.Icon(color='green')
    ).add_to(m)

    # Only geocode and mark the end point
    end_lat, end_lon = points[-1]
    end_label = reverse_geocode(end_lat, end_lon)
    folium.Marker(
        location=(end_lat, end_lon),
        popup=f"End: {end_label}",
        icon=folium.Icon(color='red')
    ).add_to(m)

    print("🔹 Adding polyline...")
    folium.PolyLine(points, color="blue", weight=4).add_to(m)

    print("🔸 Saving map...")
    m.save(filename)
    print(f"✅ Map saved successfully at {filename}")
