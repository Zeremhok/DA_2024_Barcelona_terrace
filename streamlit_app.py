import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import streamlit as st

# URL API для получения данных
url = 'https://opendata-ajuntament.barcelona.cat/data/api/action/datastore_search?resource_id=8808bc24-e14c-45a5-9c24-5e67846f087a&limit=10000'

# Запрос к API
response = requests.get(url)
data = response.json()

# Проверка, был ли запрос успешным
if data['success']:
    # Получение записей из JSON ответа
    records = data['result']['records']
    
    # Создание DataFrame из записей
    df2019_1 = pd.DataFrame(records)

# Фильтрация строк с пустыми значениями или нулевыми значениями в любом столбце
df2019_1 = df2019_1.dropna()  # Удаление строк с NaN
df2019_1 = df2019_1[(df2019_1 != 0).all(1)]  # Удаление строк с нулевыми значениями

# Выводим заголовок датасета
st.write("Dataset Head:")
st.write(df2019_1.head())

# Группировка данных по району и типу разрешения
grouped_data = df2019_1.groupby(['NOM_DISTRICTE', 'VIGENCIA']).size().reset_index(name='count')

# Вывод сгруппированных данных
st.write("Grouped Data:")
st.write(grouped_data)

# Определение цветовой палитры для каждого типа разрешения
palette = {
    'Anual': '#3498db',    # Синий
    'Temporada': '#2ecc71' # Зеленый
}

# Настройка стиля диаграммы
sns.set(style="whitegrid")

# Создание диаграммы
plt.figure(figsize=(20, 10))
chart = sns.barplot(
    x='NOM_DISTRICTE', 
    y='count', 
    hue='VIGENCIA', 
    data=grouped_data,
    palette=palette  # Указание цветовой палитры
)

# Добавление числовых подписей на барры
for p in chart.patches:
    chart.annotate(format(p.get_height(), '.0f'), 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha='center', va='center', 
                   xytext=(0, 9), 
                   textcoords='offset points')

# Настройка подписей и заголовков
plt.title('Number of terraces by blocks according to permission type')
plt.xlabel('District')
plt.xticks(rotation=90)
plt.ylabel('Count')
plt.legend(title='Type of permission')

# Отображение диаграммы в Streamlit
st.pyplot(plt)
