import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

# Load the dataset
data = pd.read_csv('sales.csv')

# Print column names to verify
print("Columns in the dataset:", data.columns)

# Convert 'Order Date' column to datetime format with dayfirst=True to handle DD/MM/YYYY format
data['Order Date'] = pd.to_datetime(data['Order Date'], dayfirst=True)

# Set 'Order Date' as index
data.set_index('Order Date', inplace=True)

# Resample data to daily sales
daily_sales = data['Sales'].resample('D').sum()

# Visualize overall statistics
plt.figure(figsize=(12, 6))
plt.plot(daily_sales, label='Daily Sales')
plt.title('Daily Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.legend()
plt.show()

# Print summary statistics
print(daily_sales.describe())


def forecast(past_sales: list[float]) -> list[float]:
    """
    Predicts the total sales for the next 3 days based on past sales data.

    Args:
        past_sales (list[float]): List of past sales data.

    Returns:
        list[float]: Predicted sales for the next 3 days.
    """
    # Fit ARIMA model
    model = ARIMA(past_sales, order=(5, 1, 0))  # Using (5, 1, 0) as a basic ARIMA model
    model_fit = model.fit()

    # Forecast next 3 days
    forecast_values = model_fit.forecast(steps=3)
    return forecast_values.tolist()

# Example usage
past_sales = daily_sales[-30:].tolist()  # Use last 30 days of data
predictions = forecast(past_sales)
print("Predicted Sales for Next 3 Days:", predictions)
