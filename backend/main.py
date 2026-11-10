from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os

app = FastAPI(title="Akıllı Ev Enerji Tahmin API")

# Model Yükleme
MODEL_PATH = os.path.join(os.path.dirname(__file__), "energy_model.joblib")
model = joblib.load(MODEL_PATH)

# Frontend dosyalarını dışa açma
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Veri Modeli
class PredictionInput(BaseModel):
    T1: float
    RH_1: float
    T2: float
    RH_2: float
    T3: float
    RH_3: float
    T_out: float
    RH_out: float
    hour: int
    day: int
    weekday: int
    energy_previous: float
    energy_1_step_ago: float
    energy_2_step_ago: float

# EPDK Fatura Hesabı
def calculate_bill(kwh: float, low_rate=2.07, high_rate=3.63, kdv=0.10):
    if kwh <= 8.0:
        cost = kwh * low_rate
    else:
        cost = (8.0 * low_rate) + ((kwh - 8.0) * high_rate)
    return cost * (1 + kdv)

@app.get("/", response_class=HTMLResponse)
async def read_index():
    return FileResponse("frontend/index.html")

@app.post("/api/predict")
async def predict_energy(data: PredictionInput):
    try:
        input_df = pd.DataFrame([data.model_dump()])
        pred_wh = float(model.predict(input_df)[0])
        pred_kwh = pred_wh / 1000.0
        cost_tl = calculate_bill(pred_kwh)
        co2_kg = pred_kwh * 0.42

        return {
            "prediction_wh": round(pred_wh, 2),
            "cost_tl": round(cost_tl, 3),
            "co2_kg": round(co2_kg, 4)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
