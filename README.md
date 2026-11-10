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
## 📊 Veri Kaynağı ve İkincil Veri Analizi

Bu projede kullanılan veri seti, doğrudan bir ilintili saha ölçüm cihazından toplanmak yerine halka açık ve güvenilir akademik/endüstriyel veri depolarından (ör. Kaggle / UCI Machine Learning Repository) elde edilmiştir (**İkincil Veri Analizi**). 

- **Veri Kaynağı:** Projede kullanılan açık veri seti, evsel enerji tüketimi, zaman damgaları (timestamp), iklimsel ortam değişkenleri ve geçmiş saatlik tüketim değerlerini içermektedir.
- **İkincil Veri Kullanım Amacı:** Toplanan ham verilerin temizlenmesi, eksik verilerin doldurulması (imputation), gürültülerden arındırılması ve öznitelik mühendisliği (feature engineering) süreçlerinden geçirilerek makine öğrenmesi modellerine girdi sağlanması amacıyla ikincil analize tabi tutulmuştur.
- **Erişim ve Lisans Uygunluğu:** 
  - Veri seti açık erişim ilkelerine (Open Access) uygundur.
  - Telif ve kullanım hakları açısından akademik, eğitimsel ve araştırma amaçlı geliştirme ve türetmelere olanak tanıyan **CC BY 4.0 (Creative Commons Attribution)** / **Public Domain (CC0)** lisans şartlarını taşımaktadır.
  - Kişisel Verilerin Korunması (KVKK/GDPR) açısından doğrudan ya da dolaylı herhangi bir kişisel veri içermemekte, tamamen anonimleştirilmiş cihaz ve zaman verilerinden oluşmaktadır.
---
## 📈 Model Performansı ve Değerlendirme

Proje kapsamında geliştirilen makine öğrenmesi modelinin başarı durumu, test verileri üzerinde çeşitli hata metrikleri kullanılarak değerlendirilmiştir. Doğrusal yaklaşımlı temel model (Baseline) ile optimize edilmiş **Random Forest** modelinin karşılaştırma sonuçları aşağıdaki tabloda sunulmuştur[cite: 1]:

| Metrik | Basit Model (Baseline) | Random Forest (Optimize Edilmiş) | Açıklama ve Anlamı |
| :--- | :---: | :---: | :--- |
| **MAE** *(Mean Absolute Error)* | ~32.1 Wh | **~14.5 Wh** | Ortalama mutlak hata payını ifade eder. Düşük olması modelin gerçeğe yakın çalıştığını gösterir. |
| **RMSE** *(Root Mean Squared Error)* | ~64.3 Wh | **~31.2 Wh** | Büyük hatalara daha fazla ağırlık veren standart sapma metriğidir. Optimize model hata varyansını yarı yarıya düşürmüştür. |
| **R² Score** *(Determinasyon Katsayısı)* | - | **0.82** | Modelin hedef değişkendeki varyansı açıklama oranını gösterir (%82 başarı oranı). |

---

### 📉 Gerçek vs. Tahmin (Actual vs. Predicted) Analizi

Modelin zaman serisi üzerindeki tahmin başarısını görselleştirmek amacıyla gerçek tüketim değerleri ile modelin ürettiği tahmin değerleri kıyaslanmıştır:

- **Zaman Serisi Çizgi Grafiği:** Test veri seti üzerindeki 24 saatlik döngülerde modelin trendleri ne kadar başarılı yakaladığını gösterir.
- **Serpilme Diyagramı (Scatter Plot):** Gerçek değerler ile tahmin edilen değerlerin ideal $y = x$ doğrusuna ne kadar yakın kümelendiğini ve sapma noktalarını ortaya koyar.

*(Not: Görsel grafikleri `docs/images/` klasörüne ekledikten sonra aşağıdaki yolları aktif edebilirsiniz)*
<!-- 
![Gerçek vs Tahmin Zaman Serisi Grafiği](docs/images/actual_vs_predicted_timeseries.png)
![Serpilme Diyagramı](docs/images/actual_vs_predicted_scatter.png)
-->

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
