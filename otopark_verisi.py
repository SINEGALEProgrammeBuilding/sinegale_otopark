import streamlit as st
import pandas as pd
import numpy as np

def otopark_verisi():

    path = pd.read_json("https://api.ibb.gov.tr/ispark/park")

    st.title("İstanbul Otoparkları Tam Listesi")

    path = path.rename(columns={
        'parkID': 'Otopark Numarası',
        'parkName': 'Otopark Adı',
        'lat': 'enlem',
        'lng': 'boylam',
        'capacity': 'Kapasite',
        'emptyCapacity': 'Boş Kapasite',
        'workHours': 'Çalışma Saatleri',
        'parkType': 'Otopark Çeşidi',
        'freeTime': 'Ücretsiz Süre',
        'district': 'İlçe',
        'isOpen': 'Açık/Kapalı'
    })

    path['Açık/Kapalı'] = np.where(
        path['Açık/Kapalı'] == 1,
        'Açık🟢',
        'Kapalı🔴'
    )

    path['Boş Kapasite'] = np.where(
        path['Boş Kapasite'] == 0,
        'Dolu🛑',
        path['Boş Kapasite'].astype(str) + '🟩'
    )

    path['Ücretsiz Süre'] = np.where(
        path['Ücretsiz Süre'] == 0,
        'Yok❌',
        path['Ücretsiz Süre'].astype(str) + '✅'
    )

    st.write(path)

    with st.expander("Kullanılan Kütüphaneler"):
        coll1, coll2, coll3, coll4, coll5 = st.columns(5)
        with coll1:
            st.image("img.png", caption='streamlit', width=100)
        with coll2:
            st.image("img_1.png", caption='pandas', width=100)
        with coll3:
            st.image("img_2.png", caption='numpy',width=100)
        with coll4:
            st.image("img_3.png", caption='sqlite3',width=100)
        with coll5:
            st.image("img_4.png", caption="python datetime",width=100)