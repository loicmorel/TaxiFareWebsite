import streamlit as st
import requests
import datetime
import pandas as pd
import numpy as np

# BACK_LOCAL_URL = "http://localhost:8000"
BACK_PROD_URL = "https://tfpredictionimageamd64-c7z3tydiqq-df.a.run.app"

MAPBOX_TOKEN = 'pk.eyJ1Ijoia3Jva3JvYiIsImEiOiJja2YzcmcyNDkwNXVpMnRtZGwxb2MzNWtvIn0.69leM_6Roh26Ju7Lqb2pwQ'
MAPBOX_URL = f"https://api.mapbox.com/geocoding/v5/mapbox.places"

def print_error(str):
    st.markdown(f'<h1 style="color:#FF0000;font-size:16px;">\
            {str}</h1>',
            unsafe_allow_html=True)

def print_debug(str):
    st.markdown(f'<h3 style="color:#D3D3D3;font-size:12px;">\
            {datetime.datetime.now()}-[debug]:{str}</h3>',
            unsafe_allow_html=True)

st.markdown("""## Taxi Fare Predictor - Loic
##### Inpute below information, then click on submit...
""")

pu_address = st.text_input("Put your pickup address")

do_address = st.text_input("Put your dropoff address")

passenger_num = st.slider("Passenger Count", 1, 8, 2)

date = st.date_input(
     "When is is your trip ?",
     datetime.date.today())

time = st.time_input("What time is your trip ?", datetime.datetime.now())

if st.button('Submit...'):

    # datetime conversion
    pickup_datetime = f'{date.strftime("%Y-%m-%d")} {time.strftime("%H:%M:%S")}'
    print(pickup_datetime)

    # pu_address conversion to coordonates
    if pu_address:
        query_mapbox = f"{MAPBOX_URL}/{pu_address}_nyc.json?types=address&access_token={MAPBOX_TOKEN}"
        print(query_mapbox)
        response = requests.get(query_mapbox)
        if response.status_code != 200:
            print_error("Error accessing MapBox API...")
            pickup_longitude = pickup_latitude = 0
        else:
            pickup_longitude = response.json().get('features')[0].get('geometry').get('coordinates')[0]
            pickup_latitude = response.json().get('features')[0].get('geometry').get('coordinates')[1]
            print_debug(f'pickup_longitude: {pickup_longitude}')
            print_debug(f'pickup_latitude: {pickup_latitude}')
    else:
        print_error("Pickup address need to be filled")
        pickup_longitude = pickup_latitude = 0

    # do_address conversion to coordonates
    if do_address:
        query_mapbox = f"{MAPBOX_URL}/{do_address}_nyc.json?types=address&access_token={MAPBOX_TOKEN}"
        print(query_mapbox)
        response = requests.get(query_mapbox)
        if response.status_code != 200:
            print_error("Error accessing MapBox API...")
            dropoff_longitude = dropoff_latitude = 0
        else:
            dropoff_longitude = response.json().get('features')[0].get('geometry').get('coordinates')[0]
            dropoff_latitude = response.json().get('features')[0].get('geometry').get('coordinates')[1]
            print_debug(f'dropoff_longitude: {dropoff_longitude}')
            print_debug(f'dropoff_latitude: {dropoff_latitude}')
    else:
        print_error("Dropoff address need to be filled")
        dropoff_longitude = dropoff_latitude = 0

    back_params = dict(
        pickup_datetime=pickup_datetime,
        pickup_longitude=pickup_longitude,
        pickup_latitude=pickup_latitude,
        dropoff_longitude=dropoff_longitude,
        dropoff_latitude=dropoff_latitude,
        passenger_count=passenger_num
    )

    # params_filled = pu_address and do_address and passenger_num and date and time
    params_filled = pickup_longitude and pickup_latitude and dropoff_longitude \
        and dropoff_latitude and date and time

    if params_filled:
        # add a map
        # df = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=['lat', 'lon'])
        # print(df)
        map_df = pd.DataFrame([[pickup_latitude, pickup_longitude],
                               [dropoff_latitude, dropoff_longitude]],
                              columns=['lat', 'lon'])
        st.map(map_df)

        # collect prediction from back office
        pred = requests.get(f"{BACK_PROD_URL}/predict", params=back_params).json().get('fare', 'prediction error...')
        pred = round(pred, 2)
        st.markdown(f'<h1 style="color:#000080;font-size:16px;">\
        NYC Taxi fare prediction: ${pred}</h1>',
        unsafe_allow_html=True)
    else:
        print_error("Missing informations to access the BackEnd API...")
