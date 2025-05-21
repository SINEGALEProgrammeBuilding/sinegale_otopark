import streamlit as st


def anasayfa():
    st.title("İstanbul Otopark Bilgi Sistemine Hoş Geldiniz!")
    st.subheader(":red[Bu Uygulama ile Yapabilecekleriniz]")
    st.write("""
    ####
    -Konumunuza en yakın otoparkları bulabilirsiniz

    -Seçtiğiniz otoparkın kapalı olup olmadığını öğrenebilirsiniz

    -Seçtiğiniz kritelerdeki otoparkların konumunu harita üzerinden inceleyabilirsiniz
    """)