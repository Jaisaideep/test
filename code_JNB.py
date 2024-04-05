#Required Imports for the code
import requests
import json
import array
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Function to fetch data from a given endpoint
def fetch_data(endpoint):
    # Calculate start and end time
    d = datetime.utcnow() - timedelta(hours=1)
    StartTime = d.strftime('%Y-%m-%dT%H:00:0000000Z')
    EndTime = datetime.utcnow().strftime('%Y-%m-%dT%H:00:0000000Z')
    
    # Set parameters and headers for the request
    parameters = {"start": StartTime, "end": EndTime}
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer AD9E312743A1DE9278FBB05BB3D2057AAA9A5839E625D8BB823B59C7EC7F2A7E"
    }

    # Make the API request
    JsonData = requests.get(endpoint, params=parameters, headers=headers).json()

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
    df['LogTime'] = Loggedtime

    return df

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

# Fetch data from all endpoints and concatenate into one dataframe
dfs = []
for endpoint in endpoints:
    df = fetch_data(endpoint)
    dfs.append(df)
    
result_df = pd.concat(dfs, ignore_index=True)

#Reordering the coloumns 
DF = result_df[['AppName','LogTime','TestTime','RequestTestResponseTime','WaitTime','SyntheticExperienceScore','AvailabilityPercent']]

# Print the consolidated dataframe
DF.head()
