import warnings

warnings.filterwarnings("ignore")

import os
import time
import random
import pandas as pd
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MaxAbsScaler, StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

from darts.datasets import TrafficDataset, AirPassengersDataset, AustralianTourismDataset
from ucimlrepo import fetch_ucirepo 

# ## Air dataset
# - https://www.opendatanetwork.com/dataset/datahub.transportation.gov/xgub-n9bw
carrier_raw = pd.read_csv("carrier_passengers.csv")
carrier_df = carrier_raw[carrier_raw['Year'] == 2023].sort_values(by = 'data_dte').reset_index(drop = True)
carrier_df = carrier_df.drop(columns=["data_dte", "usg_apt_id", "usg_wac", "fg_apt_id", "fg_wac", "airlineid", "type", "Scheduled", "Charter"])

# ### Numeric encoding
columns_to_encode = ['usg_apt', 'fg_apt', 'carrier']
temp_df = carrier_df.copy()
temp_df = temp_df[columns_to_encode]

model_df = carrier_df.copy()

## Construct encoders
le_usg_apt = LabelEncoder()
le_fg_apt = LabelEncoder()
le_carrier = LabelEncoder()

## Encode the data
model_df['usg_apt_encoded'] = le_usg_apt.fit_transform(model_df['usg_apt'])
model_df['fg_apt_encoded'] = le_fg_apt.fit_transform(model_df['fg_apt'])
model_df['carrier_encoded'] = le_carrier.fit_transform(model_df['carrier'])
model_df = model_df.drop(columns=['usg_apt', 'fg_apt', 'carrier']).rename(columns = {0:"Month", 1:"carriergroup", 2:"Total"})


# ### Fit the model on average passenger per month
## , 'carriergroup', 'usg_apt_encoded', 'fg_apt_encoded', 'carrier_encoded'
scaler = StandardScaler()
X = model_df[['Month']].drop_duplicates().reset_index(drop = True)
X['Year'] = 2023
model_df['Avg'] = model_df.groupby(by = 'Month')['Total'].transform("mean")
y = model_df[['Avg']].drop_duplicates().reset_index(drop = True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train = scaler.fit_transform(X_train)
X_test = scaler.fit_transform(X_test)
y_train = scaler.fit_transform(y_train)
y_test = pd.DataFrame(scaler.fit_transform(y_test))

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test).flatten()
results_df = pd.DataFrame(y_pred).reset_index(drop = True)
results_df = pd.concat([y_test, results_df], axis = 1).rename(columns = {0:"Predicted", "Total": "Actual"})

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

# ### Forecast future data
from datetime import datetime, timedelta
from darts import TimeSeries
from src.forecasting_engine import get_data, write_forecast
import pandas as pd

## Timestamp ('%Y-%m-%dT%H:%M:%S'), node_id, noise (binary = loud or not), count
## Data to be collected every 15 mins
## Want to forecast for 6 hours = 24 future steps

end = datetime.now()
start = (end - timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%S')
end = end.strftime('%Y-%m-%dT%H:%M:%S')

data_raw = get_data(start = start, end = end) ## only use the last 24 hours as input
n_future = 24

## Get forecast dates and times
end_time = datetime.now() + timedelta(hours = int(n_future/4))
future_times = []
current_time = datetime.now()
while current_time <= end_time:
    future_times.append(current_time.strftime('%Y-%m-%dT%H:%M:%S'))
    current_time += timedelta(minutes=15)

# ### Preprocess data and run model on new data
## Remove node_id
processed_data = data_raw.copy()
processed_data['Month'] = pd.to_datetime(processed_data['timestamp']).dt.month
processed_data['Year'] = pd.to_datetime(processed_data['timestamp']).dt.year
processed_data = processed_data[['Month', 'Year']].drop_duplicates()
new_data = pd.DataFrame({'Month': [7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5], 'Year': [2024, 2024, 2024, 2024, 2024, 2024, 2025, 2025, 2025, 2025, 2025, ]})

processed_data = pd.concat([processed_data, new_data], axis = 0).reset_index(drop = True)

## Predict model to our data
preds = list(model.predict(processed_data).flatten())
forecast_df = pd.DataFrame(preds).rename(columns = {0:"Forecast"})
start_time = datetime(2024, 6, 26, 20, 0, 0) 
end_time = datetime(2024, 6, 26, 23, 0, 0)  

# Generate timestamps in 15-minute intervals
timestamps = []
current_time = start_time
while current_time < end_time:
    timestamps.append(current_time)
    current_time += timedelta(minutes=15)

forecast_df['node_id'] = 1
forecast_df['Timestamp'] = timestamps

write_forecast(forecast_df, node_id = 1)