import os.path
import random
import folium
import numpy as np
import pandas as pd
from folium import plugins
from folium.plugins import Draw
import requests

def addPluginMiniMap():
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

    # Añadir el pluggin
    plugins.MiniMap().add_to(map)

    # Guardar el mapa como un archivo HTML
    map.save("ColombiaJSONPluggins.html")

if __name__ == '__main__':
    addPluginMiniMap()