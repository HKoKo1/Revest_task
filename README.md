Daily Sales Forecasting using ARIMA
This repository implements data analysis and daily sales forecasting using the ARIMA model in Python. Sales data is loaded from a CSV file, transformed into an appropriate format, and then forecasting is done using past sales data to predict the next 3 days of sales.

Key Features:

1-Data Loading: Loads sales data from a CSV file containing columns like "Order Date" and "Sales".

2-Data Transformation: Converts the "Order Date" column to a datetime format and sets it as the index.

3-Resampling: Resamples the data to get daily sales totals.

4-Visualization: Plots daily sales over time using the matplotlib library.

5-ARIMA Forecasting: Uses an ARIMA model (with the default (5, 1, 0) parameters) to predict sales for the next 3 days based on past daily sales data.

Requirements:
1) pandas
2) matplotlib
3) statsmodels
4) numpy
