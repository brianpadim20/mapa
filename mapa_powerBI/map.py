import folium
import pandas as pd
import pyodbc
import requests

def map_data(lat_col, lon_col):
    # Detalles de conexión
    server = 'grupoafincloud.database.windows.net'
    database = 'InfoAfin_BI'
    username = 'InfoAfinReadUser'
    password = 'GrupoBI$*2023'
    driver = 'SQL Server Native Client 11.0'
    
    # Cadena de conexión
    conn_str = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    # Conectarse a Azure
    conn = pyodbc.connect(conn_str)

    # URL de GeoJSON para marcar la frontera de colombia
    political_countries_url = (
        "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
    )

    # Solicitud GET para obtener el GeoJSON de todos los países
    response = requests.get(political_countries_url)
    data = response.json()

    colombia_geometry = next(
        feature for feature in data["features"] if feature["properties"]["name"] == "Colombia"
    )
    
    # Ejecutar una consulta SQL para obtener los datos
    query = "SELECT Latitud, Longitud FROM Dim.Clientes"
    df = pd.read_sql(query, conn)

    # Test
    # print (df)
    
    # Cerrar la conexión a la base de datos
    conn.close()

    # Filtrar valores NaN en latitud y longitud
    df = df.dropna(subset=[lat_col,lon_col])

    # # Coordenadas aproximadas de los extremos de Colombia
    lat_min = 0   # Latitud mínima
    lat_max = 12  # Latitud máxima
    lon_min = -79 # Longitud mínima
    lon_max = -66 # Longitud máxima

    # # Calcular el centro del mapa más al norte
    lat_center = (lat_min + lat_max) / 2 - 2  # Ajusta la latitud hacia el norte
    lon_center = (lon_min + lon_max) / 2

    # # Crear el mapa con los límites establecidos
    map = folium.Map(location=[lat_center, lon_center], zoom_start=6.4, min_lat=lat_min, max_lat=lat_max, min_lon=lon_min, max_lon=lon_max)

    # Añadir la geometría de Colombia al mapa
    folium.GeoJson(colombia_geometry, fill_opacity=0).add_to(map)
    
    # Añadir los marcadores al mapa
    for index, row in df.iterrows():
        lat, lon = row[lat_col], row[lon_col]
        info = f"<p>{', '.join([f'{col}: {row[col]}' for col in df.columns])}</p>"
        folium.Marker(location=[lat, lon], tooltip=info).add_to(map)
    
    # Guardar el mapa como un archivo HTML
    map.save("index.html")
    
    # Retornar el mapa como un objeto HTML
    # return map._repr_html_()

if __name__ == '__main__':
    # Llama a la función map_data con los nombres de las columnas de latitud y longitud
    map_data('Latitud', 'Longitud')


# ----------------------------------------------------------------------------------------------------------

# import folium
# import pandas as pd
# import pyodbc
# import requests

# def map_data(lat_col, lon_col):
#     # Detalles de conexión
#     server = 'grupoafincloud.database.windows.net'
#     database = 'InfoAfin_BI'
#     username = 'InfoAfinReadUser'
#     password = 'GrupoBI$*2023'
#     driver = 'SQL Server Native Client 11.0'
    
#     # Cadena de conexión
#     conn_str = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

#     # Conectarse a Azure
#     conn = pyodbc.connect(conn_str)

#     # URL de GeoJSON para marcar la frontera de colombia
#     political_countries_url = (
#         "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
#     )

#     # Solicitud GET para obtener el GeoJSON de todos los países
#     response = requests.get(political_countries_url)
#     data = response.json()

#     colombia_geometry = next(
#         feature for feature in data["features"] if feature["properties"]["name"] == "Colombia"
#     )

#     # Conectarse a SQL
#     conn = pyodbc.connect(conn_str)
    
#     # Ejecutar una consulta SQL para obtener los datos
#     query = "SELECT Latitud, Longitud FROM Dim.Clientes"
#     df = pd.read_sql(query, conn)

#     # Test
#     # print (df)
    
#     # Cerrar la conexión a la base de datos
#     conn.close()

#     # Filtrar valores NaN en latitud y longitud
#     df = df.dropna(subset=[lat_col,lon_col])

#     # # Coordenadas aproximadas de los extremos de Colombia
#     lat_min = 0   # Latitud mínima
#     lat_max = 12  # Latitud máxima
#     lon_min = -79 # Longitud mínima
#     lon_max = -66 # Longitud máxima

#     # # Calcular el centro del mapa más al norte
#     lat_center = (lat_min + lat_max) / 2 - 2  # Ajusta la latitud hacia el norte
#     lon_center = (lon_min + lon_max) / 2

#     # # Crear el mapa con los límites establecidos
#     map = folium.Map(location=[lat_center, lon_center], zoom_start=6.4, min_lat=lat_min, max_lat=lat_max, min_lon=lon_min, max_lon=lon_max)

#     # Añadimos la geometría de Colombia al mapa
#     folium.GeoJson(colombia_geometry, fill_opacity=0).add_to(map)
    
#     # # Añadir los marcadores al mapa
#     for index, row in df.iterrows():
#         lat, lon = row[lat_col], row[lon_col]
#         info = f"<p>{', '.join([f'{col}: {row[col]}' for col in df.columns])}</p>"
#         folium.Marker(location=[lat, lon], tooltip=info).add_to(map)
    
#     # # Guardar el mapa como un archivo HTML
#     map.save("mapa_desde_sql.html")

# if __name__ == '__main__':
#     # Llama a la función map_data con los nombres de las columnas de latitud y longitud
#     map_data('Latitud', 'Longitud')