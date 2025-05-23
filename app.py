# 必要なライブラリをインポート
import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import pydeck as pdk  # ← これを追加！

# アプリのタイトルを表示
st.title("🚕 Taxi Fare Prediction App")

# アプリの説明を表示
st.markdown("""
Enter your ride details (date, time, location, passenger count)
and get a fare estimate using Le Wagon's prediction API.
""")

# セッションステート初期化（履歴のため）
if "fare_history" not in st.session_state:
    st.session_state.fare_history = []

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

        st.session_state.fare_history.append({
            "datetime": pickup_datetime,
            "fare": prediction
        })

    except Exception as e:
        st.error(f"Failed to get prediction: {e}")


#st.map(pickup_coords, zoom=12)
#st.caption("📍 Pickup Location")

#st.map(dropoff_coords, zoom=12)
#st.caption("🏁 Dropoff Location")

    # グラフ表示
if st.session_state.fare_history:
    df_history = pd.DataFrame(st.session_state.fare_history)
    st.line_chart(df_history.set_index("datetime"))
    st.caption("📊 Fare Prediction History")

# 🗺️ ルート線を描画するマップ表示（pickup → dropoff）

# 緯度・経度をルートとして1本の線に
# Pickup & Dropoffのマーカー用データ
points_df = pd.DataFrame([
    {"lat": pickup_latitude, "lon": pickup_longitude},
    {"lat": dropoff_latitude, "lon": dropoff_longitude}
])

points_layer = pdk.Layer(
    "ScatterplotLayer",
    data=points_df,
    get_position='[lon, lat]',
    get_color='[0, 200, 255]',
    get_radius=100,
)


view_state = pdk.ViewState(
    latitude=(pickup_latitude + dropoff_latitude)/2,
    longitude=(pickup_longitude + dropoff_longitude)/2,
    zoom=12
)

# ラベル用データ
labels_df = pd.DataFrame([
    {"lat": pickup_latitude, "lon": pickup_longitude, "label": "Pickup"},
    {"lat": dropoff_latitude, "lon": dropoff_longitude, "label": "Dropoff"}
])

text_layer = pdk.Layer(
    "TextLayer",
    data=labels_df,
    get_position='[lon, lat]',
    get_text="label",
    get_color=[255, 255, 255],
    get_size=16,
    get_alignment_baseline="'bottom'"
)

st.pydeck_chart(pdk.Deck(
    layers=[points_layer,text_layer],
    initial_view_state=view_state
))
st.caption("📍 Pickup & Dropoff Points")
