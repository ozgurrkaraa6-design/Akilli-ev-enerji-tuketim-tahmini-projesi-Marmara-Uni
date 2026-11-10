# Akilli-ev-enerji-tuketim-tahmini-projesi-Marmara-Uni

Bu proje, **Yazılım Mühendisliğine Giriş** dersi kapsamında geliştirilmiş; anlık sensör verileri, zaman/takvim değişkenleri ve geçmiş tüketim alışkanlıklarını kullanarak bir sonraki saatteki enerji ihtiyacını tahmin eden uçtan uca bir Makine Öğrenmesi (ML) ve Web uygulamasıdır. Bu proje ile gelecekte yaşanabilecek enerji kıtlığı sorununun önüne geçmeyi düşünüyoruz.

Bu proje şirketlerde, evlerde, dükkanlarda kısacası her yerde kullanılabilir.

---

## Proje Özellikleri

- **Zaman Serisi Modelleme:** Geçmiş ölçümler ('lag features') türetilerek zamansal bağımlılıkları modele aktarılır.
- **Explainable AI (Açıklanabilir YZ):** Random Forest modeli üzerinden 'Features Importance' analizi yapılarak kararları etkileyen ana faktörler (anlık tüketim vs. sıcaklık/saat) ortaya konmuştur.
- **Hiperparametre Optimizasyonu:** 'GridSearchCV' kullanılarak aşırı öğrenme (overfitting) engellenme ve test başarım skorları en iyilenmiştir.
- **Canlı Web Arayüzü:** Eğitilen model '.joblib' formatında dışa aktarılıp 'Streamlit' tabalı etkileşimli bir kullanıcı paneline dönüştürülmüştür.

---
---

## 📋 Proje Yönetimi & Kanban Tablosu

Proje geliştirme süreci Agile/Kanban prensiplerine uygun olarak yürütülmüştür.

| 📌 Yapılacaklar (To Do) | 🔄 Devam Edenler (In Progress) | ✅ Tamamlananlar (Done) |
| :--- | :--- | :--- |
| 🔲 Modelin REST API (FastAPI) olarak yayınlanması | ⏳ Canlı sensör verisi simülasyon testi | ☑️ Veri seti ön işleme ve 'lag' öznitelik türetimi |
| 🔲 Docker konteynerizasyonu | ⏳ HTML,JavaScript,CSS ile Arayüz İyileştirmesi | ☑️ Baseline model vs. Random Forest karşılaştırması |
| | | ☑️ GridSearchCV ile hiperparametre optimizasyonu |
| | | ☑️ Explainable AI (Feature Importance) analizi |
| | | ☑️ Eğitilen modelin `.joblib` olarak aktarımı |

---

## 👥 Ekip Rolleri ve Görev Dağılımı

Projenin başarıyla tamamlanmasında görev alan ekip üyeleri ve üstlendikleri sorumluluklar:

- **[Batuhan Güney  / @Bthn0]** – *Raporlama ve Değerlendirme*
  - Proje raporunun hazırlanması
  - yapılan çalışmaları değerlendirme

- **[Emirhan Bilgin  / @Twoughtt]** – *Veri Bilimcisi & Kontrolcüsü *
  - Kodlama ve Arayüz Sonucu ortaya çıkan verileri ve akışı kontrol etme.
  - Grafik uygunluk denetleme.

- **[Özgür Kara / @Gozgurrkaraa6-design]** – *Yazılım & Arayüz Geliştiricisi*
  - Kodlama ve Arayüz geliştirme.
  - Verisetini entegre etme.

- **[Umut Eldiven / @Umuteldvn]** – *Veri Analizi & Proje Yönetimi & Sunu Hazırlama *
  - Veriseti Bulma ve uygunluğunu kontrol etme.
  - Projenin Haftalık akışını kontrol etme ve yönlendirme.

## Model Başarım Metrikleri 

| Metrik | Basit Model (Baseline) | Random Forest (Optimize)|
| **MAE (Mean Absolute Error)** | ~32.1 Wh | **~14.5 Wh** |
| **RMSE (Root Mean Squared Error)** | ~64.3 Wh | **~31.2 Wh**|
| **R² Score** | - | **0.82** | 

---

## Kullanılan Teknolojiler 
- **Programlama Dili:** Python 3.10+
- **Veri Analizi & Ön İşleme:** Pandas, NumPy
- **Makine Öğrenmesi:** Scikit-Learn ('RandomForestRegressor', 'GridSearchCV')
- **Göreselleştirme:** Matplotlib, Seaborn
- **Arayüz & Yaygınlaştırma:** Streamlit, Joblib

---

## Kurulum ve Çalıştırma

### 1. Repoyu Klonlayın
```bash
git clone https://github.com/ozgurrkaraa6-design/Akilli-ev-enerj-tuketim-tahmini-projesi-Marmara-Uni.git
cd Akilli-ev-enerji-tuketim-tahmini-projesi-Marmara-Uni
```
