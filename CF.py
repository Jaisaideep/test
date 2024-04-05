import requests
import json
import array
import pandas as pd
import numpy as np
from google.cloud import bigquery
from datetime import datetime, timedelta

def terradata(event,context):
    d = datetime.utcnow() - timedelta(hours=1)
    StartTime = d.strftime('%Y-%m-%dT%H:00:0000000Z')
    EndTime = datetime.utcnow().strftime('%Y-%m-%dT%H:00:0000000Z')
    endpoint = "http://io.catchpoint.com/api/v2/tests/explorer/favoritechart/data/25334"
    # parameters = {"startTimeUtc": {StartTime}, "endTimeUtc": {EndTime}}
    parameters = {"start": {StartTime}, "end": {EndTime}}
    headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer AD9E312743A1DE9278FBB05BB3D2057AAA9A5839E625D8BB823B59C7EC7F2A7E"}
    #http_proxy = "http://proxy.ebiz.verizon.com:80"
    #proxies = {"http": http_proxy}
    JsonData = requests.get(endpoint, params=parameters, headers=headers).json()
    # Manually loaded the JSON result from postman to a file to parse the JSON values;
    # This can be removed and  JSONData can be passed to JsonSampleData

    # data = json.load(ResponseJson)

    # Declaring arrays
    Loggedtime = []
    AppName = []
    MetricsName = []
    MetricsVal = []
    # code to get the metrics name by Traversing the JSON
    for i in JsonData['data']['favoriteCharts'][0]['summary']['fields']['syntheticMetrics']:
        MetricsName.append(i['name'])
    # Code to get other values like Time, AppName and Test results
    for i in JsonData['data']['favoriteCharts'][0]['detail']['items']:

        Loggedtime.append(i['dateTime'])
        AppName.append(i['dimension'][1]['name'])
        MetricsVal.append(i['syntheticMetrics'])

    # Creating a Dataframe to Load the data in tabular format, this can be pushed to BQ

    df = pd.DataFrame(data=np.array(MetricsVal), columns=np.array(MetricsName))
    df['AppName'] = AppName
    df['LogTime'] = Loggedtime

    print(df)
    table_id = 'AIDSRE.DATAROBOT_CP_DATA'
    Client = bigquery.Client()
   # table_id1 = 'AIDSRE.TD_LOWVERSIONDRIVERS'
    # Since string columns use the "object" dtype, pass in a (partial) schema
    # to ensure the correct BigQuery data type.
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.job.WriteDisposition.WRITE_APPEND
    )
    
    job = Client.load_table_from_dataframe(
                        df, table_id,job_config=job_config
                            )
    job.result()
