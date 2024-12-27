import pandas as pd
from statsmodels.tsa.arima.model import ARIMA  # type: ignore
import joblib

# Load the dataset
df = pd.read_csv(r"D:\Stock_prediction\TATAMOTORS.csv", parse_dates=True, index_col='Date')

# Ensure columns are correctly formatted
df.columns = df.columns.str.strip()

# Fit the ARIMA model
model = ARIMA(df['close'], order=(5, 1, 5))
model_fit = model.fit()

# Save the fitted model
joblib.dump(model_fit, 'arima_model_tata.pkl')
print("Model saved successfully!")