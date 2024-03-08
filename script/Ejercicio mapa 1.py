import folium

def displayWebMapTiles():
    map = folium.Map()
    map.save("foliumTutorial.html")

def displayWebMapName():
    map = folium.Map(tiles="Stamen Terrain",attr="Map tiles by Stamen Design")
    map.save("foliumTutorial.html")


def displayGeoLocation():
    map = folium.Map (location = (49.25, -123.12))#, tiles="cartodb positron", attr="Map tiles by Stamen Design")
    map.save("foliumTutorial.html")

def mostrarColombia():
    # Coordenadas aproximadas de los extremos de Colombia
    lat_min = 0   # Latitud mínima
    lat_max = 12  # Latitud máxima
    lon_min = -79 # Longitud mínima
    lon_max = -66 # Longitud máxima

    # Calculamos el centro del mapa más al norte
    lat_center = (lat_min + lat_max) / 2 - 2  # Ajustamos la latitud hacia el norte
    lon_center = (lon_min + lon_max) / 2

    # Creamos el mapa con los límites establecidos
    map = folium.Map(location=[lat_center, lon_center],zoom_start=6.4, min_lat=lat_min, max_lat=lat_max, min_lon=lon_min, max_lon=lon_max)
    map.save("colombia_map.html")

if __name__ == '__main__':
    #displayWebMapTiles()
    displayWebMapName()
    # mostrarColombia()