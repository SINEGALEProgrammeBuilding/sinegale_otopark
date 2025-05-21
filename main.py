import streamlit as st

from otopark_verisi import otopark_verisi
from anasayfa import anasayfa
from otopark_dagilimi import otopark_dagilimi
from otopark_bulma import otopark_bulma

st.set_page_config(page_title="İstanbul Otoparkarı Bilgi Sistemi", page_icon=":red_car:", layout="wide")

st.markdown("""
    <style>
    /* Normal buton görünümü */
    div.stButton > button {
        background-color: #003366 !important;
        color: white !important;
        transition: all 0.2s ease-in-out;
    }

    /* Tıklanma anındaki (press) durum */
    div.stButton > button:active {
        background-color: gray !important;
        color: black !important;
    }

    /* Buton dışındaki yeniden render durumlarında varsayılan renkleri korumak için override */
    div.stButton > button:focus:not(:active) {
        background-color: gray !important;
        color: white !important;
    }

    </style>
""", unsafe_allow_html=True)

if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠︎Ana Sayfa"

with st.sidebar:
    st.header("Sayfalar")
    if st.button("🏠︎Ana Sayfa"):
        st.session_state.current_page = "🏠︎Ana Sayfa"
    if st.button("🏼Veri Yapısı(Teknik Bilgiler ve Otopark Listesi)"):
        st.session_state.current_page = "🏼Veri Yapısı(Teknik Bilgiler ve Otopark Listesi)"
    if st.button("🗺️İstanbul Otopark Dağılımı"):
        st.session_state.current_page = "🗺️İstanbul Otopark Dağılımı"
    if st.button("֎Kriterlere Göre Otopark Bulma"):
        st.session_state.current_page = "֎Kriterlere Göre Otopark Bulma"

if st.session_state.current_page == "🏠︎Ana Sayfa":
    st.empty()
    anasayfa()
elif st.session_state.current_page == "🏼Veri Yapısı(Teknik Bilgiler ve Otopark Listesi)":
    st.empty()
    otopark_verisi()
elif st.session_state.current_page == "🗺️İstanbul Otopark Dağılımı":
    st.empty()
    otopark_dagilimi()
elif st.session_state.current_page == "֎Kriterlere Göre Otopark Bulma":
    st.empty()
    otopark_bulma()
else:
    anasayfa()