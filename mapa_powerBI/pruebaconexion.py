import pandas as pd
import pyodbc

def map_data():
    # Detalles de conexión
    server = 'grupoafincloud.database.windows.net'
    database = 'InfoAfin_BI'
    username = 'InfoAfinReadUser'
    password = 'GrupoBI$*2023'
    driver = 'SQL Server Native Client 11.0'
    
    # Cadena de conexión
    conn_str = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    # Conectarse a SQL
    conn = pyodbc.connect(conn_str)
    
    # Ejecutar una consulta SQL para obtener los datos
    query = "SELECT Latitud, Longitud FROM Dim.Clientes"
    df = pd.read_sql(query, conn)

    # Test
    print (df)
    
    # Cerrar la conexión a la base de datos
    conn.close()

map_data()