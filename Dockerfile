FROM python:3.10-slim

WORKDIR /app

# Gerekli bağımlılıkları kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tüm proje dosyalarını kopyala
COPY . .

# Python'ın çalışma dizinini (PYTHONPATH) /app olarak tanıt
ENV PYTHONPATH=/app

EXPOSE 8080

# Sunucuyu çalıştır
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]