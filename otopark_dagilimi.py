import streamlit as st
import pandas as pd
import requests


def otopark_dagilimi():
    st.title("İstanbul Otopark Dağılım Haritası")

    try:
        url = "https://api.ibb.gov.tr/ispark/park"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        df = pd.DataFrame(data)

        required_columns = ['lat', 'lng', 'parkName', 'capacity', 'emptyCapacity']
        if not all(col in df.columns for col in required_columns):
            missing = [col for col in required_columns if col not in df.columns]
            raise KeyError(f"Eksik sütun(lar): {missing}")

        df = df.rename(columns={'lng': 'lon'})
        df = df.dropna(subset=['lat', 'lon'])
        df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
        df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
        df = df.dropna(subset=['lat', 'lon'])

        if df.empty:
            st.warning("Gösterilecek veri bulunamadı")
            return

        st.subheader("Belediye'ye Bağlı Otoparklar")
        st.map(df[['lat', 'lon']].assign(
            lat=df['lat'].astype(float),
            lon=df['lon'].astype(float)
        ), zoom=10)


    except requests.exceptions.RequestException as e:
        st.error(f"API bağlantı hatası: {str(e)}")
        st.info("Demo veri ile devam ediliyor...")
        demo_data = pd.DataFrame({
            'lat': [41.0082, 41.0223, 41.0542],
            'lon': [28.9784, 29.0134, 29.0032],
            'parkName': ["Demo Otopark 1", "Demo Otopark 2", "Demo Otopark 3"],
            'capacity': [100, 150, 200],
            'emptyCapacity': [20, 0, 50]
        })
        st.map(demo_data)

    except Exception as e:
        st.error(f"Beklenmeyen hata: {str(e)}")