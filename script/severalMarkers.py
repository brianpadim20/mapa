import folium
import requests
import pandas as pd

def geoJSONColombia():
    # URL del GeoJSON con los límites de todos los países
    political_countries_url = (
        "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
    )

    # Realizar una solicitud GET para obtener el GeoJSON de todos los países
    response = requests.get(political_countries_url)
    data = response.json()

    # Filtrar los datos para obtener solamente la geometría de Colombia
    colombia_geometry = next(
        feature for feature in data["features"] if feature["properties"]["name"] == "Colombia"
    )

    # Coordenadas aproximadas de los extremos de Colombia
    lat_min = 0   # Latitud mínima
    lat_max = 12  # Latitud máxima
    lon_min = -79 # Longitud mínima
    lon_max = -66 # Longitud máxima

    # Calcular el centro del mapa más al norte
    lat_center = (lat_min + lat_max) / 2 - 2  # Ajusta la latitud hacia el norte
    lon_center = (lon_min + lon_max) / 2

    # Crear el mapa con los límites establecidos
    map = folium.Map(location=[lat_center, lon_center], zoom_start=6.4, min_lat=lat_min, max_lat=lat_max, min_lon=lon_min, max_lon=lon_max)
    
    # Añadir la geometría de Colombia al mapa
    folium.GeoJson(colombia_geometry, fill_opacity=0).add_to(map)
    
    # COORDENADAS
    coords = pd.DataFrame({'lang':[-74.072090, -75.5174, -74.7813, -76.5320,  -75.6182, -75.5917],
                        'lat':[4.710989, 5.0687, 10.9685, 3.4516, 6.1498, 6.1709]})
    
    for i, j in coords.iterrows():
        folium.Marker(location = [j['lat'], j['lang']]).add_to(map)
    
    #Cuando el marcador aparece solo como "circle" y no "circlemarker" se debe expresar el radio en kilómetros (se deben poner en miles)
    for i, j in coords.iterrows():
        folium.Circle(
            location = [j['lat'], j['lang']],
            radius = 20000,
            fill = True,
            color = "blue",
            fill_color = "red",
            fill_opacity = 0.25,
            tooltip = "Prueba del tooltip para Power BI" #popup es la alternativa, a este tbn se le puede poner código html
            ).add_to(map)
    
    # Guardar el mapa como un archivo HTML
    map.save("ColombiaJSONSeveralMarkers.html")

if __name__ == '__main__':
    geoJSONColombia()