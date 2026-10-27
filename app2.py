import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

# SAYFA AYARLARI
st.set_page_config(
    page_title="Akıllı Ev Enerji Tüketim Simülatörü",
    page_icon="⚡",
    layout="wide"
)

# BAŞLIK ve AÇIKLAMA
st.title("⚡ Akıllı Ev Enerji Tüketim Tahmini & Karar Destek Paneli")
st.write("Sensör verilerini tekil olarak test edilebilir veya günlere bağlı sıralı simülasyon çalışıtrarak gelecek tahminlerini grafik üzerinde inceleyebilirsiniz. Ayrıca maliyet/karbon analizi ve model kıyaslaması yapabilirsiniz.")

# MODEL YÜKELEME
@st.cache_resource
def load_assets():
    model = joblib.load("energy_model.joblib")
    try:
        benchmark = pd.read_csv("models_benchmark.csv")
    except:
        benchmark = None
    return model, benchmark

try:
    model, benchmark_df = load_assets()
    st.success("Model ve sistem verileri başarıyla yüklendi!")
except Exception as e:
    st.error("Model dosyaları bulunamadı! Lütfen önce model.py dosyasını çalıştırın.")    

st.divider()

# YAN MENÜ (SİDEBAR) - TAHMİN MODU SEÇİMİ
st.sidebar.header("⚙️ Simülasyon & Birim Fiyat Ayarları")
app_mode = st.sidebar.radio("Mod Seçimi:", ["1. Anlık Tekil Tahmin", "2. Günlük/Haftalık Sıralı Simülasyon", "3. Model Karşılaştırmaları (Benchmark)"])

st.sidebar.divider()
st.sidebar.subheader("💰 Birim Fiyat ve Karbon Oranları")
kwh_price = st.sidebar.number_input("Elektrik Birim Fiyatı (TL / kWh):", value=2.50, step=0.10)
co2_rate = st.sidebar.number_input("Karbon Oranı (kg CO₂ / kWh):", value=0.42, step=0.01)


# MOD 1: ANLIK TAHMİN & MALİYET ANALİZİ
if app_mode == "1. Anlık Tekil Tahmin":
    st.subheader("📊 Tek Bir Saat İçin Sensör Verileri ve Finansal/Çevresel Etki Analizi")

    col1, col2 = st.columns(2)

    with col1:
        energy_previous = st.number_input("Şu Anki Tüketim (energy_previous - Wh)", min_value=0.0, value=50.0, step=5.0)
        energy_1_step_ago = st.number_input("1 Adım Önceki Tüketim (energy_1_step_ago - Wh)", min_value=0.0,  value=40.0, step=5.0)
        energy_2_step_ago = st.number_input("2 Adım Önceki Tüketim (energy_2_step_ago - Wh)", min_value=0.0, value=30.0, step=5.0)
        hour = st.slider("Saat (0 - 23)", min_value=0, max_value=23, value=14)
        day = st.slider("Günün Tarihi (1 - 31)", min_value=1, max_value=31, value=15)

    with col2:
        T1 = st.number_input("Mutfak Sıcaklığı (T1 - °C)", value=21.0)
        RH_1 = st.number_input("Mutfak Nemi RH_1 - %", value=47.0)
        T2 = st.number_input("Oturma Odası Sıcaklığı (T2 - °C)", value=20.0)
        RH_2 = st.number_input("Oturma Odası Nemi (RH_2 - %)", value=44.0)  
        T3 = st.number_input("Çamaşır Odası Sıcaklığı (T3 - °C)", value=22.0)
        RH_3 = st.number_input("Çamaşır Odası Nemi (RH_3 - %)", value=40.0)
        T_out = st.number_input ("Dış Hava Sıcaklığı (T_out - °C)", value=6.0)
        RH_out = st.number_input("Dış Havanın Nemi (RH_out - %)", value=92.0)
        weekday = st.selectbox("Haftanın Günü", options=[0, 1, 2, 3, 4, 5, 6,], format_func=lambda x:["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"][x])

    if st.button("🔮 Tahmin Et ve Analiz Et", type="primary"):    
        input_data =pd.DataFrame([{
            "T1": T1, "RH_1": RH_1,
            "T2": T2, "RH_2": RH_2,
            "T3": T3, "RH_3": RH_3,
            "T_out": T_out, "RH_out": RH_out,
            "hour": hour, "day": day, "weekday": weekday,
            "energy_previous": energy_previous,
            "energy_1_step_ago": energy_1_step_ago,
            "energy_2_step_ago": energy_2_step_ago}])

        pred_wh = model.predict(input_data)[0]
        pred_kwh = pred_wh / 1000.0  # Wh değerini kWh değerine dönüştürür
        cost_tl = pred_kwh * kwh_price
        co2_kg = pred_kwh * co2_rate
 
        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric(label="💡 Tahmini Enerji Tüketimi (1 Saat)", value=f"{round(pred_wh, 2)} Wh")
        m2.metric(label="💰 Tahmini Saatlik Fatura Etkisi", value=f"{round(cost_tl, 3)} TL")
        m3.metric(label="🌿 Tahmini Karbon Ayak İzi", value=f"{round(co2_kg, 4)} kg CO₂")


# MOD 2 GÜNLÜK/HAFTALIK SIRALI SİMÜLASYON

elif app_mode == "2. Günlük/Haftalık Sıralı Simülasyon":
    st.subheader("📅 Günlere Bağlı Sıralı Simülasyon ve Toplam Maliyet Tahmini")

    col1, col2, col3 = st.columns(3)
    with col1:
        num_days = st.slider("Simüle Edilicek Gün Sayısı:", min_value=1, max_value=7, value=3)
    with col2:
        base_temp = st.number_input("Ortalama İç Sıcaklık (°C):", value=21.0)
    with col3:
        initial_energy = st.number_input("Başlangıç Tüketim (Wh):", value=50.0)

    if st.button("🚀 Simülasyonu Çalıştır", type="primary"):
        total_hours = num_days * 24
        predictions_list = []
        timestamps = []

        # BAŞLANGIÇ LAG DEĞERLERİ
        e_prev = initial_energy
        e_1_ago = initial_energy * 0.9
        e_2_ago = initial_energy * 0.8

        # GÜN VE SAAT BAZINDA DÖNGÜ İLE ARDIŞIK TAHMİN
        for h in range (total_hours):
            current_day = (h // 24) + 1
            current_hour = h % 24
            current_weekday = (h // 24) % 7

            # SAATLİK VE GÜNLÜK BASİT BİR SICAKLIK DALGALAMASI SİMÜLE EDİYORUZ
            temp_var = np.sin(h / 24 * 2 * np.pi) * 2

            input_data = pd.DataFrame([{
                "T1": base_temp + temp_var, "RH_1": 45.0,
                "T2": base_temp - 1.0 + temp_var, "RH_2": 42.0,
                "T3": base_temp + 1.0, "RH_3": 40.0,
                "T_out": base_temp - 10.0 + temp_var, "RH_out": 85.0,
                "hour": current_hour,
                "day": current_day,
                "weekday": current_weekday,
                "energy_previous": e_prev,
                "energy_1_step_ago": e_1_ago,
                "energy_2_step_ago": e_2_ago
            }])

            # MODELİ ÇALIŞTIR
            pred = model.predict(input_data)[0]

            predictions_list.append(pred)
            timestamps.append(f"Gün {current_day} - {current_hour:02d}:00")

            # BİR SONRAKİ SAAT İÇİN LAG (GEÇMİŞ) DEĞERLERİNİ GÜNCELLE (OTOREGRESİF KAYDIRMA)
            e_2_ago = e_1_ago
            e_1_ago = e_prev
            e_prev = pred

        # SONUÇLARI DATAFRAME'E DÖNÜŞTÜR
        results_df = pd.DataFrame({
            "Zaman": timestamps,
            "Tahmini Tüketim (Wh)": predictions_list    
        })

        # HESAPLAMALAR
        total_wh = sum(predictions_list)
        total_kwh = total_wh / 1000.0
        total_cost = total_kwh * kwh_price
        total_co2 = total_kwh * co2_rate

        st.divider()
        
        # ZAMAN SERİSİ GRAFİĞİ GÖSTERİMİ
        st.subheader("📈 Zaman Serisi Tahmin Grafiği")

        fig, ax = plt.subplots(figsize=(14, 5))
        ax.plot(results_df["Tahmini Tüketim (Wh)"], color="#1f77b4", linewidth=2, marker='o', markersize=3, label="Tahmini Tüketim (Wh)")
        ax.set_title(f"{num_days} Günlük Saatlik Enerji Tüketim Tahmin Eğrisi", fontsize=14, fontweight='bold')
        ax.set_xlabel("Zaman (Saat Sıralı)", fontsize=11)
        ax.set_ylabel("Enerji (Wh)", fontsize=11)
        ax.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig)

        # GÜN GEÇİŞLERİNE DİKEy ÇİZGİLER EKLE
        for day_mark in range (1, num_days):
            ax.axvline(x=day_mark * 24, color='red', linestyle=':', alpha=0.7, label="Gün Değişimi" if day_mark==1 else"")

        st.pyplot(fig)

        # FİNANSAL ÖZET METRİKLER
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Toplam Tüketim", f"{round(total_kwh, 2)} kWh")
        c2.metric("Toplam Tahmini Fatura", f"{round(total_cost, 2)} TL")
        c3.metric("Toplam Karbon Salınımı", f"{round(total_co2, 2)}kg CO₂")
        c4.metric("Zirve (Peak) Tüketim", f"{round(max(predictions_list), 2)} Wh")

# MODEL KARŞILAŞTIRMALARI (BENCHMARK)

else:
    st.subheader("🏆 Makine Öğrenmesi Algoritmalarının Karşılaştırılması (Model Benchmark)")
    st.write("Farklı regresyon algoritmalarının test veri seti üzerindeki performans skorları aşağıda listelenmiştir.")

    if benchmark_df is not None:
        st.dataframe(benchmark_df, use_container_width=True)

        # KARŞILAŞTIRMA GRAFİĞİ
        st.subheader("📊 MAE (Hata Oranı) Kıyaslama Grafiği")
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        colors = ['#ff9999', '#66b3ff', '#99ff99']
        ax2.bar(benchmark_df["Model"], benchmark_df["MAE (Wh)"], color=colors)
        ax2.set_label("MAE - Ortalama Mutlak Hata (Wh) [Düşük Olan İyidir]")
        ax2.set_title("Modellerin Hata Oranı Kıyaslaması")
        st.pyplot(fig2)

        st.info("💡 **Sonuç:** Random FOrest modeli en düşük MAE skoru ve en yüksek R² başarısını gösterdiği için nihai tahmin motoru olarak seçilmiştir.") 
      
    else:
       st.warning("Benchmark verisi bulunamadı! Lütfen model.py dosyasını çalıştırıp benchmark verilerini oluşturun.")

    
        