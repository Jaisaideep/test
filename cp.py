import requests
import json
import array
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

d = datetime.utcnow() - timedelta(hours=1)

StartTime = d.strftime('%Y-%m-%dT%H:00:0000000Z')
EndTime = datetime.utcnow().strftime('%Y-%m-%dT%H:00:0000000Z')
print (StartTime)
print (EndTime)

endpoint = "http://io.catchpoint.com/api/v2/tests/explorer/favoritechart/data/34649"
parameters = {"start": {StartTime}, "end": {EndTime}}
headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer AD9E312743A1DE9278FBB05BB3D2057AAA9A5839E625D8BB823B59C7EC7F2A7E"}

JsonData = requests.get(endpoint, params=parameters, headers=headers).json()

# Declaring arrays
Loggedtime = []
AppName = []
MetricsName = []
MetricsVal = []

# code to get the metrics name by Traversing the JSON
for i in JsonData['data']['favoriteCharts'][0]['summary']['fields']['syntheticMetrics']:
    MetricsName.append(i['name'])
print (MetricsName)

# Code to get other values like Time, AppName and Test results
for i in JsonData['data']['favoriteCharts'][0]['detail']['items']:
    Loggedtime.append(i['dateTime'])
    AppName.append(i['dimension'][1]['name'])
    MetricsVal.append(i['syntheticMetrics'])

df = pd.DataFrame(data=np.array(MetricsVal), columns=np.array(MetricsName))
df['AppName'] = AppName
df['LogTime'] = Loggedtime
print(df)

#Rearrange the order of df
NewDF = df[['AppName','LogTime','TestTime','RequestTestResponseTime','WaitTime','SyntheticExperienceScore','AvailabilityPercent']]
