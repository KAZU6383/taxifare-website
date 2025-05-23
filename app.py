# 必要なライブラリをインポート
import streamlit as st
import requests
from datetime import datetime

# アプリのタイトルを表示
st.title("🚕 Taxi Fare Prediction App")

# アプリの説明を表示
st.markdown("""
Enter your ride details (date, time, location, passenger count)
and get a fare estimate using Le Wagon's prediction API.
""")

# 乗車日と時間の入力
pickup_date = st.date_input("Pickup Date")
pickup_time = st.time_input("Pickup Time")
pickup_datetime = f"{pickup_date} {pickup_time}"

# 出発地点の緯度・経度
pickup_longitude = st.number_input("Pickup Longitude", value=-73.950655)
pickup_latitude = st.number_input("Pickup Latitude", value=40.783282)

# 到着地点の緯度・経度
dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.984365)
dropoff_latitude = st.number_input("Dropoff Latitude", value=40.769802)

# 乗車人数
passenger_count = st.slider("Number of Passengers", 1, 8, 1)

# 使用するAPIのエンドポイント
url = "https://taxifare.lewagon.ai/predict"
st.markdown("Note: Using Le Wagon's demo API endpoint.")

# ボタンでAPIを呼び出し
if st.button("Predict Fare"):
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        #st.json(response.json())

        prediction = response.json()["fare"]
        st.success(f"Estimated Fare: ${prediction:.2f}")
    except Exception as e:
        st.error(f"Failed to get prediction: {e}")
