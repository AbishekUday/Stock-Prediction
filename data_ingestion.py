import os
import requests
import pandas as pd

# API settings
API_KEY = "4G2EKXPPVZMP1NOW"
SYMBOL = "TATAMOTORS.BSE"  # Example stock symbol

# Fetch data
url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}&outputsize=full"
response = requests.get(url)
data = response.json()["Time Series (Daily)"]

# Prepare DataFrame
df = pd.DataFrame.from_dict(data, orient="index").astype(float)

# Ensure directory exists
output_dir = "data_ingestion"
os.makedirs(output_dir, exist_ok=True)

# Save CSV
csv_file = os.path.join(output_dir, "stock_data.csv")
df.to_csv(csv_file, index=True)
print("Data saved successfully!")

