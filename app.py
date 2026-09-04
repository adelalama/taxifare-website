import streamlit as st
import requests
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Taxi Fare Predictor", page_icon="🚖", layout="centered")

'''
## Detalles del viaje:
'''

col1, col2 = st.columns(2)

with col1:
    pickup_date = st.date_input('Fecha del Viaje', datetime.now().date())
    pickup_time = st.time_input('Hora del Viaje', datetime.now().time())
    passenger_count = st.number_input('Numero de Pasajeros', min_value = 1, max_value = 8, value = 1)

with col2:
    pickup_longitude = st.number_input('Longitud de origen', value = -73.985428, format = '%.6f')
    pickup_latitude = st.number_input('Latitud de origen', value = 40.748817, format= '%.6f')
    dropoff_longitude = st.number_input('Longitud de destino', value = -73.780968,  format = '%.6f')
    dropoff_latitude = st.number_input('Latitud de destino', value = 40.641766, format = '%.6f')

pickup_datetime = f'{pickup_date} {pickup_time}'

map_data = pd.DataFrame({
    'latitude': [pickup_latitude, dropoff_latitude],
    'longitude': [pickup_longitude, dropoff_longitude],
    'Tipo': ['Origen', 'Destino']
})

st.map(map_data)

if st.button('Calcular precio'):

    url = 'https://taxifare.lewagon.ai/predict'
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }
    with st.spinner('Calculando el mejor precio...'):
        try:
            response = requests.get(url, params = params)
            result = response.json()
            prediction = result.get('fare', result.get('prediction'))
            st.success(f'Tarifa estimada: ${prediction}')
        except Exception as e:
            st.error(f'Sucedio el siguiente error: {e}')
