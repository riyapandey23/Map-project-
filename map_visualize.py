import folium
import os
from tomtom_geocoding import reverse_geocode

def plot_route(points, filename="route_map.html"):
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

    # Ensure we save into the package's static folder so Flask can serve it
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    os.makedirs(static_dir, exist_ok=True)
    out_path = os.path.join(static_dir, filename)

    print("🔸 Saving map to static folder...")
    m.save(out_path)
    print(f"✅ Map saved successfully at {out_path}")
