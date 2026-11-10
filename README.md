# Akilli-ev-enerji-tuketim-tahmini-projesi-Marmara-Uni

Bu proje, **Yazılım Mühendisliğine Giriş** dersi kapsamında geliştirilmiş; anlık sensör verileri, zaman/takvim değişkenleri ve geçmiş tüketim alışkanlıklarını kullanarak bir sonraki saatteki enerji ihtiyacını tahmin eden uçtan uca bir Makine Öğrenmesi (ML) ve Web uygulamasıdır[cite: 1]. Bu proje ile gelecekte yaşanabilecek enerji kıtlığı sorununun önüne geçmeyi düşünüyoruz[cite: 1].

Bu proje şirketlerde, evlerde, dükkanlarda kısacası her yerde kullanılabilir[cite: 1].

---

## Proje Özellikleri

- **Zaman Serisi Modelleme:** Geçmiş ölçümler ('lag features') türetilerek zamansal bağımlılıkları modele aktarılır[cite: 1].
- **Explainable AI (Açıklanabilir YZ):** Random Forest modeli üzerinden 'Features Importance' analizi yapılarak kararları etkileyen ana faktörler (anlık tüketim vs. sıcaklık/saat) ortaya konmuştur[cite: 1].
- **Hiperparametre Optimizasyonu:** 'GridSearchCV' kullanılarak aşırı öğrenme (overfitting) engellenme ve test başarım skorları en iyilenmiştir[cite: 1].
- **Canlı Web Arayüzü:** Eğitilen model '.joblib' formatında dışa aktarılıp 'Streamlit' tabalı etkileşimli bir kullanıcı paneline dönüştürülmüştür[cite: 1].

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

Proje kapsamında geliştirilen farklı makine öğrenmesi modellerinin test verileri üzerindeki başarı durumları aşağıda karşılaştırılmalı olarak sunulmuştur:

| Model | MAE (Wh) | RMSE (Wh) | $R^2$ Skoru |
| :--- | :---: | :---: | :---: |
| **Linear Regression** | 29.71 | 60.82 | 0.554 |
| **Decision Tree** | 74.52 | 152.56 | -1.808 |
| **Random Forest (Optimize)** | **45.39** | **75.48** | **0.313** |

---

### 📉 Gerçek vs. Tahmin (Actual vs. Predicted) Analizi

Modelin zaman serisi üzerindeki tahmin başarısını görselleştirmek amacıyla gerçek tüketim değerleri ile modelin ürettiği tahmin değerleri kıyaslanmıştır:

- **Zaman Serisi Çizgi Grafiği:** Test veri seti üzerindeki döngülerde modelin trendleri ne kadar başarılı yakaladığını gösterir.
- **Serpilme Diyagramı (Scatter Plot):** Gerçek değerler ile tahmin edilen değerlerin dağılımını ve sapma noktalarını ortaya koyar.

*(Not: Görsel grafikleri `docs/images/` klasörüne ekledikten sonra aşağıdaki yolları aktif edebilirsiniz)*
<!-- 
![Gerçek vs Tahmin Zaman Serisi Grafiği](docs/images/actual_vs_predicted_timeseries.png)
![Serpilme Diyagramı](docs/images/actual_vs_predicted_scatter.png)
-->

---

## 📋 Proje Yönetimi & Kanban Tablosu

Proje geliştirme süreci Agile/Kanban prensiplerine uygun olarak yürütülmüştür[cite: 1].

| 📌 Yapılacaklar (To Do) | 🔄 Devam Edenler (In Progress) | ✅ Tamamlananlar (Done) |
| :--- | :--- | :--- |
| 🔲 Modelin REST API (FastAPI) olarak yayınlanması | ⏳ Canlı sensör verisi simülasyon testi | ☑️ Veri seti ön işleme ve 'lag' öznitelik türetimi[cite: 1] |
| 🔲 Docker konteynerizasyonu | ⏳ HTML,JavaScript,CSS ile Arayüz İyileştirmesi | ☑️ Baseline model vs. Random Forest karşılaştırması[cite: 1] |
| | | ☑️ GridSearchCV ile hiperparametre optimizasyonu[cite: 1] |
| | | ☑️ Explainable AI (Feature Importance) analizi[cite: 1] |
| | | ☑️ Eğitilen modelin `.joblib` olarak aktarımı[cite: 1] |

---

## 👥 Ekip Rolleri ve Görev Dağılımı

Projenin başarıyla tamamlanmasında görev alan ekip üyeleri ve üstlendikleri sorumluluklar[cite: 1]:

- **[Batuhan Güney  / @Bthn0]** – *Raporlama ve Değerlendirme*[cite: 1]
