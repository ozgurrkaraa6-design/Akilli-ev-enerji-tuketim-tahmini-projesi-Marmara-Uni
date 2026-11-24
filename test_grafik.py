import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

# 1. Kayıt klasörünü otomatik oluştur
os.makedirs("docs/images", exist_ok=True)

# 2. Veri setini yükle (Önce yerelde arar, bulamazsa UCI kaynağından otomatik çeker)
local_paths = ["data/energydata_complete.csv", "energydata_complete.csv"]
csv_source = next((p for p in local_paths if os.path.exists(p)), 
                  "https://archive.ics.uci.edu/ml/machine-learning-databases/00374/energydata_complete.csv")

df = pd.read_csv(csv_source)

# 3. Öznitelik Mühendisliği (Takvim ve Lag Değişkenleri)
df['date'] = pd.to_datetime(df['date'])
df['hour'] = df['date'].dt.hour
df['day'] = df['date'].dt.day
df['weekday'] = df['date'].dt.weekday

df['energy_previous'] = df['Appliances'].shift(1)
df['energy_1_step_ago'] = df['Appliances'].shift(2)
df['energy_2_step_ago'] = df['Appliances'].shift(3)
df.dropna(inplace=True)

features = ['T1', 'RH_1', 'T2', 'RH_2', 'T3', 'RH_3', 'T_out', 'RH_out',
            'hour', 'day', 'weekday', 'energy_previous', 'energy_1_step_ago', 'energy_2_step_ago']

X = df[features]
y = df['Appliances']

# Zaman serisi sırasını korumak için shuffle=False kullanıyoruz
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
test_dates = df.loc[y_test.index, 'date']

# 4. Random Forest Modelini Eğit ve Tahmin Üret
model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

# ---------------------------------------------------------
# GRAFİK 1: 24 Saatlik Zaman Serisi Çizgi Grafiği (144 adım = 24 saat)
# ---------------------------------------------------------
plt.figure(figsize=(10, 5))
saat_etiketleri = test_dates.iloc[:144].dt.strftime('%H:%M')

plt.plot(range(144), y_test.iloc[:144].values, label="Gerçek Değerler (Actual)", color="#0f2942", linewidth=2)
plt.plot(range(144), y_pred[:144], label="Tahmin Edilen (Predicted)", color="#e67e22", linestyle="--", linewidth=2)

plt.xticks(ticks=range(0, 144, 18), labels=saat_etiketleri.iloc[::18])
plt.title("24 Saatlik Akıllı Ev Enerji Tüketim Tahmini (Gerçek vs. Tahmin)", fontsize=13, fontweight="bold")
plt.xlabel("Zaman (Saat)", fontsize=11)
plt.ylabel("Enerji Tüketimi (Wh)", fontsize=11)
plt.legend(frameon=True, facecolor="white", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("docs/images/actual_vs_predicted_timeseries.png", dpi=300)
plt.show()

# ---------------------------------------------------------
# GRAFİK 2: Serpilme Diyagramı (Scatter Plot)
# ---------------------------------------------------------
plt.figure(figsize=(7, 6))
plt.scatter(y_test, y_pred, alpha=0.35, color="#0284c7", edgecolors="none", label="Tahmin Noktaları")

max_val = max(y_test.max(), y_pred.max())
plt.plot([0, max_val], [0, max_val], color="#dc2626", linestyle="--", linewidth=2, label="İdeal y = x Doğrusu")

plt.title(f"Gerçek vs. Tahmin Edilen Değerler (R² = {r2:.2f} | MAE = {mae:.1f} Wh)", fontsize=12, fontweight="bold")
plt.xlabel("Gerçek Tüketim (Wh)", fontsize=11)
plt.ylabel("Tahmin Edilen Tüketim (Wh)", fontsize=11)
plt.legend(frameon=True, facecolor="white", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("docs/images/actual_vs_predicted_scatter.png", dpi=300)
plt.show()

print("Grafikler başarıyla 'docs/images/' klasörüne kaydedildi!")