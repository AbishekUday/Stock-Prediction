from fastapi import FastAPI, UploadFile, File
import pandas as pd
import joblib
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta

# Load the pre-trained model
model = joblib.load("arima_model_tata.pkl")

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Stock Price Prediction API!"}

# Upload endpoint
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), days: int = 30):
    try:
        # Read uploaded file
        df = pd.read_csv(file.file, parse_dates=['Date'], index_col='Date')
        df.columns = df.columns.str.strip()
        df = df.sort_index()

        # Train a new ARIMA model based on the uploaded dataset
        new_model = ARIMA(df['close'], order=(5, 1, 5))
        new_model_fit = new_model.fit()

        # Forecast future stock prices
        forecast = new_model_fit.forecast(steps=days)
        start_date = df.index[-1] + timedelta(days=1)
        future_dates = pd.date_range(start_date, periods=days, freq='B')

        # Prepare predictions
        predictions = [
            {"date": date.strftime("%Y-%m-%d"), "predicted_close": round(price, 2)}
            for date, price in zip(future_dates, forecast)
        ]

        return {"predictions": predictions}

    except Exception as e:
        return {"error": str(e)}

