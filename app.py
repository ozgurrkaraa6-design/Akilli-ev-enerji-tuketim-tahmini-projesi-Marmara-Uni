import streamlit as st
import pandas as pd
import numpy as np
import joblib

# sayfa ayarları
st.set_page_config(
    page_title="Akıllı Ev Enerji Tüketim Tahmini",
    page_icon="⚡",
    layout="centered"
)

# başlık ve açıklama
st.title("⚡ Akıllı Ev Enerji Tüketim Tahmin Paneli")
st.write("Anlık sensör verileri ve geçmiş tüketim alışkanlıklarını kullanarak gelecek saatteki enerji ihtiyacını tahmin edin.")

# model yükleme
@st.cache_resource
def load_model():
    return joblib.load("energy_model.joblib")

try:
    model = load_model()
    st.success("Model başarıyla yüklendi")
except Exception as e:
    st.error("Model dosyası ('energy_model.joblib') bulunamadı! Lütfen önce model.py dosyasını çalıştırın.")

st.divider()

# kullanıcı girdi formu 
st.subheader("📊 Sensör ve Zaman Verilerini Giriniz")

col1, col2 = st.columns(2)

with col1:
    energy_previous = st.number_input("Şu Anki Tüketim (energy_previous - Wh)", min_value=0.0, value=50.0, step=5.0)
    energy_1_step_ago = st.number_input("1 Adım Önceki Tüketim (energy_1_step_ago - Wh)", min_value=0.0, value=40.0, step=5.0)
    energy_2_step_ago = st.number_input("2 Adım Önceki Tüketim (energy_2_step_ago - Wh)", min_value=0.0, value=30.0, step=5.0)
    hour = st.slider("Saat (0 - 23)", min_value=0, max_value=23, value=14)
    day = st.slider("Günün Tarihi (1 - 31)", min_value=1, max_value=31, value=15)

with col2:
    T1 = st.number_input("Mutfak Sıcaklığı (T1 - °C)", value=21.0)
    RH_1 = st.number_input("Mutfak Nemi (RH_1 - %)", value=47.0)    
    T2 = st.number_input("Oturma Odası Sıcaklığı (T2 - °C)", value=20.0)
    RH_2 = st.number_input("Oturma Odası Nemi (RH_2 - °C)", value=44.0)
    T3 = st.number_input("Çamaşır Odası Sıcaklığı (T3 - °C)", value=22.0)
    RH_3 = st.number_input("Çamaşır Odası Nemi (RH_3 - °C)", value=40.0)
    T_out = st.number_input("Dış Hava Sıcaklığı (T_out - °C)", value=6.0)
    RH_out = st.number_input("Dış Hava Nemi (RH_out - °C)", value=92.0)
    weekday = st.selectbox("Haftanın Günleri", options=[0, 1, 2, 3, 4, 5, 6], format_func=lambda x:["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"][x])


# tahmin butonu
if st.button("🔮 Gelecek Saat Enerji Tüketimini Tahmin Et", type="primary"):
    # girdileri dataframe formatına getir
    input_data = pd.DataFrame([{
        "T1": T1, "RH_1": RH_1,
        "T2": T2, "RH_2": RH_2,
        "T3": T3, "RH_3": RH_3,
        "T_out": T_out, "RH_out": RH_out,
        "hour": hour, "day": day, "weekday": weekday,
        "energy_previous": energy_previous,
        "energy_1_step_ago": energy_1_step_ago,
        "energy_2_step_ago": energy_2_step_ago
    }])

    # tahmin yap
    prediction = model.predict(input_data)[0]

    st.divider()
    st.metric(label="💡 Tahmin Edilen Enerji Tüketimi (1 Saat Sonra)", value=f"{round(prediction, 2)} Wh")
    