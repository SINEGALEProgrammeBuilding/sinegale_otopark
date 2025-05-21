import streamlit as st
import pandas as pd
from datetime import time

def otopark_bulma():
    try:
        park_data = pd.read_json("https://api.ibb.gov.tr/ispark/park")
    except Exception as e:
        st.error(f"Veri alınamadı: {str(e)}")
        return

    st.title("🏙️ İstanbul'da Otopark Bul")

    try:
        ilce_listesi = sorted(park_data['district'].dropna().astype(str).unique().tolist())
        default_index = ilce_listesi.index("Beşiktaş") if "Beşiktaş" in ilce_listesi else 0
    except Exception as e:
        st.error(f"İlçe listesi oluşturulamadı: {str(e)}")
        return

    selected_district = st.selectbox("📍 İlçe Seçin", ilce_listesi, index=default_index)
    selected_time = st.time_input("⏰ Hangi saatte gideceksiniz?", value=time(12, 0))

    try:
        filtered_parks = park_data[
            (park_data['district'] == selected_district) &
            (park_data['isOpen'] == 1)
        ].copy()
    except KeyError as e:
        st.error(f"Filtreleme hatası: {str(e)} sütunu bulunamadı")
        return

    if not filtered_parks.empty:
        filtered_parks = filtered_parks.dropna(subset=['lat', 'lng'])
        filtered_parks['lat'] = pd.to_numeric(filtered_parks['lat'], errors='coerce')
        filtered_parks['lng'] = pd.to_numeric(filtered_parks['lng'], errors='coerce')
        filtered_parks = filtered_parks.dropna(subset=['lat', 'lng'])

        bos_kapasiteli = filtered_parks[filtered_parks['emptyCapacity'] > 0]
        dolu_otoparklar = filtered_parks[filtered_parks['emptyCapacity'] == 0]

        st.subheader(f"✅ Boş Kapasitesi Olan Otoparklar ({len(bos_kapasiteli)})")

        if not bos_kapasiteli.empty:
            try:
                st.subheader("🗺️ Konum Haritası")
                map_data = bos_kapasiteli[['lat', 'lng']].rename(columns={'lat': 'latitude', 'lng': 'longitude'})
                st.map(map_data, use_container_width=True)
            except Exception as e:
                st.error(f"Harita oluşturulamadı: {str(e)}")

        for _, park in bos_kapasiteli.iterrows():
            with st.expander(f"{park['parkName']} ({park.get('emptyCapacity', 0)} boş)", expanded=False):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.caption(f"_{park.get('parkType', 'Bilgi Yok')}_")
                with col2:
                    st.metric("Boş Kapasite", f"{park.get('emptyCapacity', 0)}",
                              help=f"Toplam: {park.get('capacity', 'Bilgi Yok')}")
                with col3:
                    st.markdown(f"**⏰ {park.get('workHours', 'Bilinmiyor')}**")

                st.markdown(f"""
                    📍 **Koordinatlar:** {park['lat']:.5f}, {park['lng']:.5f}  
                    ⏳ **Ücretsiz Süre:** {park.get('freeTime', 'Bilgi Yok')} dakika
                """)

        st.subheader(f"🚫 Dolmuş Otoparklar ({len(dolu_otoparklar)})")
        if not dolu_otoparklar.empty:
            for _, park in dolu_otoparklar.iterrows():
                with st.expander(f"~~{park['parkName']}~~ (DOLU)", expanded=False):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.caption(f"_{park.get('parkType', 'Bilgi Yok')}_")
                    with col2:
                        st.metric("Boş Kapasite", "0",
                                  delta=f"-{park.get('capacity', 0)}",
                                  delta_color="inverse")

                    st.markdown(f"""
                        ⚠️ **Durum:** Tamamen dolu  
                        ⏳ **Ücretsiz Süre:** {park.get('freeTime', 'Bilgi Yok')} dakika
                    """)
        else:
            st.info("Bu kategoride otopark bulunamadı")
    else:
        st.warning("⛔ Bu ilçede uygun otopark bulunamadı")

if __name__ == "__main__":
    otopark_bulma()