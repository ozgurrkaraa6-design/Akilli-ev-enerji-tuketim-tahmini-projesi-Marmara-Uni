import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.model_selection import GridSearchCV


# veriyi yükle
df = pd.read_csv("data/energydata_complete.csv")
df["date"] = pd.to_datetime(df["date"])

# tarih özelliklerini çıkar
df["hour"] = df["date"].dt.hour
df["day"] = df["date"].dt.day
df["weekday"] = df["date"].dt.dayofweek


# önceki ölçümlerdeki enerji tüketimi
df["energy_previous"] = df["Appliances"]
df["energy_1_step_ago"] = df["Appliances"].shift(1)
df["energy_2_step_ago"] = df["Appliances"].shift(2)
df["target"] = df["Appliances"].shift(-1)

# gelecekte bilinmeyen hedefi ve son satırı çıkar
df = df.dropna(subset=["target", "energy_previous", "energy_1_step_ago", "energy_2_step_ago",])

# model girdileri
features = [
    "T1", "RH_1",
    "T2", "RH_2",
    "T3", "RH_3",
    "T_out", "RH_out",
    "hour", "day", "weekday",
    "energy_previous",    
    "energy_1_step_ago",
    "energy_2_step_ago"
    ]

x = df[features]
y = df["target"]

# veriyi zamana göre ayır
split = int(len(df) * 0.8)

x_train = x.iloc[:split]
x_test = x.iloc[split:]
y_train = y.iloc[:split]
y_test = y.iloc[split:]


# modeli eğit
model = RandomForestRegressor(
    n_estimators=200,
    random_state=10,
    n_jobs=-1
)



model.fit(x_train, y_train)

# tahmin yap 
predictions = model.predict(x_test)

# basit tahmin: sonraki tüketim mevcut tüketime eşit
baseline_predictions = x_test["energy_previous"]

baseline_mae =mean_absolute_error(
    y_test, baseline_predictions
)

baseline_rmse =np.sqrt(
    mean_squared_error(y_test, baseline_predictions) 
)

print(f"Basit Model MAE :{round(baseline_mae, 3)} Wh")
print(f"Basit Model RMSE : {round(baseline_rmse, 3)} Wh")
print("_" * 40)

# sonuçları değerlendir
mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

print("Model başarıyla eğitildi!")
print(f"Model MAE : {round(mae, 3)} Wh")
print(f"Model RMSE : {round(rmse, 3)} Wh")
print(f"Model R² : {round(r2, 3)}")

# gerçek ve tahmin edilen değerleri karşılaştır
comparison = pd.DataFrame({
    "Gercek": y_test.iloc[:200].values,
    "Tahmin": predictions[:200]
})

print("\nİlk 25 tahmin:")
print(comparison.head(25))

plt.figure(figsize=(12, 5))
comparison.plot(ax=plt.gca(), alpha=0.8)
plt.title("Gercek ve Tahmin Edilen Enerji Tüketimi")
plt.xlabel("Olcum")
plt.ylabel("Enerji (Wh)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

# adım 1 : öznitelik  önem düzeyi
# 1. önem skorlarını modelden al ve sıfırla

importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

# 2. dataframe olarak düzenle

feature_importance_df = pd.DataFrame({
    'Özellik': [features[i]for i in indices],
    'Önem Skoru': importances[indices]
})

print("\n---Özellik Önem Düzeyleri---")
print(feature_importance_df.to_string(index=False))

# 3. grafil ile görselleştirme

plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df['Özellik'][::-1], feature_importance_df['Önem Skoru'][::-1], color='skyblue')
plt.xlabel('Önem Skoru (Importance Score)')
plt.ylabel('Girdi Özellikleri (Features)')
plt.title('Random Forest Modeli -   Girdi Özelliklerinin Tahmine Etkisi')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

print("\n--- Hiperparametre Optimisazyonu Başlatılıyor... ---")

# denenecek parametre kombinasyonlarını tanımla
param_grid = {
    'n_estimators': [100, 200],       # oluşturulucak ağaç sayısı
    'max_depth': [10, 20, None],     # ağaçların maksimim derinliği
    'min_samples_split': [2, 5],     # bir düğümün dallanması için gereken min örnek
    'min_samples_leaf': [1, 2]       # bir yaprakta bulunması gereken min örnek
}

# temel modeli ve GridSearchCV nesnesini oluşturur
rf_base = RandomForestRegressor(random_state=10, n_jobs=-1)

# zaman serisi yapısına zarar vermemek için cv=3 tutuyoruz ( negative mean squared error ile optimizasyın)
grid_search = GridSearchCV(
    estimator=rf_base,
    param_grid=param_grid,
    cv=3,
    scoring='neg_mean_squared_error',
    n_jobs=-1,
    verbose=1
)

# eğitimi başlat ( en iyi kombinasyonu bulur)
grid_search.fit(x_train, y_train)

# en iyi parametreleri ve en iyi modeli al
best_params = grid_search.best_params_
best_model = grid_search.best_estimator_

print("\nBulunan En İyi Parametreler:")
print(best_params)

# optimized (En iyilenmiş) model ile tahmin yap
opt_predictions = best_model.predict(x_test)

opt_mae = mean_absolute_error(y_test, opt_predictions)
opt_rmse = np.sqrt(mean_squared_error(y_test, opt_predictions))
opt_r2 = r2_score(y_test, opt_predictions)

print("\n--- Optimize Edilmiş Random Forest Model Sonuçları---")
print(f"Eski Model MAE: {round(mae, 3)} Wh --> Yeni Model MAE: {round(opt_mae, 3)} Wh")
print(f"Eski Model RMSE: {round(rmse, 3)} Wh --> Yeni Model RMSE: {round(opt_rmse, 3)} Wh")
print(f"Eski Model R² : {round(r2, 3)}  --> Yeni Model R² : {round(opt_r2, 3)}") 

# modeli kaydetme
import joblib 

# en iyi modeli ve özzellikleri kaydediyoruz
joblib.dump(best_model, "energy_model.joblib")
print("\n[BİLGİ] Model 'energy_model.joblib' olarak başarıyla kaydedildi!")