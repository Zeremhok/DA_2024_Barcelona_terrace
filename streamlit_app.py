import streamlit as st

st.title("Barcelona terrace visualisation")
st.write(
    "Hello, DA community. This is my first project"
)
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import folium
import requests
import pandas as pd

# URL API для отримання даних
url = 'https://opendata-ajuntament.barcelona.cat/data/api/action/datastore_search?resource_id=8808bc24-e14c-45a5-9c24-5e67846f087a&limit=10000'

# Запит до API
response = requests.get(url)
data = response.json()

# Перевірка, чи запит був успішним
if data['success']:
    # Отримання записів з JSON відповіді
    records = data['result']['records']
    
    # Створення DataFrame з записів
    df2019_1 = pd.DataFrame(records)

# Чітаємо дані з датасету
data = df2019_1

# Завантажуємо дані для візуалізації мапи
gdf = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

barcelona_map = folium.Map([41.3947,2.1557], zoom_start=12.4, tiles='cartodbpositron')
folium.GeoJson(gdf).add_to(barcelona_map)

# Функція для додавання маркерів на мапу
def add_markers(map_obj, data_frame):
    for _, row in data_frame.iterrows():
        folium.Marker(
            location=[row['LATITUD'], row['LONGITUD']],  # Задаємо звідки брати геодані
            popup=row['NOM_DISTRICTE'],  
        ).add_to(map_obj)

# Додаємо маркери на мапу
add_markers(barcelona_map, df2019_1)

# Візуалізація мапи
barcelona_map