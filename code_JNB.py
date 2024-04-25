#Required Imports for the code
import requests
import json
import array
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

 # Set parameters and headers for the request
#parameters = {"start": StartTime, "end": EndTime}
headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer AD9E312743A1DE9278FBB05BB3D2057AAA9A5839E625D8BB823B59C7EC7F2A7E"}

# List of endpoints to fetch data from
endpoints = [
        "http://io.catchpoint.com/api/v2/tests/explorer/favoritechart/data/34649",
        "http://io.catchpoint.com/api/v2/tests/explorer/favoritechart/data/34648",
        "http://io.catchpoint.com/api/v2/tests/explorer/favoritechart/data/34646",
        "http://io.catchpoint.com/api/v2/tests/explorer/favoritechart/data/34643",
        "http://io.catchpoint.com/api/v2/tests/explorer/favoritechart/data/35503",
        "http://io.catchpoint.com/api/v2/tests/explorer/favoritechart/data/35504",
        "http://io.catchpoint.com/api/v2/tests/explorer/favoritechart/data/35581"
            ]

# Initialize an empty list to store dataframes
dfs = []

# Iterate over each endpoint to fetch data
for endpoint in endpoints:
    # Make the API request
    JsonData = requests.get(endpoint, headers=headers).json() 

    # Extracting data from the JSON response
    Loggedtime = []
    AppName = []
    MetricHeader = []
    MetricData = []

    # Extracting metrics names
    for i in JsonData['data']['favoriteCharts'][0]['summary']['fields']['syntheticMetrics']:
        MetricHeader.append(i['name'])

    # Extracting metrics values, logged time, and app name
    for i in JsonData['data']['favoriteCharts'][0]['detail']['items']:
        Loggedtime.append(i['dateTime'])
        AppName.append(i['dimension'][1]['name'])
        MetricData.append(i['syntheticMetrics'])

    # Creating a dataframe from the extracted data
    df = pd.DataFrame(data=np.array(MetricData), columns=np.array(MetricHeader))
    df['AppName'] = AppName
    df['LogTime'] = pd.to_datetime(Loggedtime)  # Convert 'LogTime' to datetime

    # Append the dataframe to the list
    dfs.append(df)

# Concatenate all dataframes into one
result_df = pd.concat(dfs, ignore_index=True)

# Reordering the columns
result_df = result_df[['AppName','LogTime','TestTime','RequestTestResponseTime','WaitTime','SyntheticExperienceScore','AvailabilityPercent']]

#Filter records in newDF based on timestamps
if 'DF' in globals():
    max_timestamp = DF['LogTime'].max()
    new_records = result_df[result_df['LogTime'] > max_timestamp]
    DF = pd.concat([DF, new_records], ignore_index=True)
else:
    DF = result_df
