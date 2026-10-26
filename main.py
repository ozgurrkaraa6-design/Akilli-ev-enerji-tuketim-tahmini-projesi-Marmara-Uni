import pandas as pd 
import matplotlib.pyplot as plt

df = pd.read_csv("data/energydata_complete.csv")

# tarih bilgisini zamana dönüştürür
df["date"] = pd.to_datetime(df["date"])

# veri seti hakkında bilgi
print("Veri boyutu:", df.shape)
print("\nSütunlar:")
print(df.columns.tolist())

print("\nEksik değerler:")
print(df.isnull().sum())

# enerji tüketiminin istatistikleri
print("\nEnerji tüketimi:")
print(df["Appliances"].describe())

# günlük ortalama enerji tüketimi
df["gun"] = df["date"].dt.date
gunluk = df.groupby("gun")["Appliances"].mean()

gunluk.plot(figsize=(10, 5))
plt.title("Günlük ortalama enerji tüketimi")
plt.xlabel("Gun")
plt.ylabel("Ortalama tüketim (Wh)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
