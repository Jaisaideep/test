import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from google.cloud import bigquery

def fetch_and_store_data():
    # Calculate start and end time
    EndTime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.0000000Z')
    StartTime = (datetime.utcnow() - timedelta(minutes=30)).strftime('%Y-%m-%dT%H:%M:%S.0000000Z')

    # Set parameters and headers for the request
    parameters = {"start": StartTime, "end": EndTime}
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer AD9E312743A1DE9278FBB05BB3D2057AAA9A5839E625D8BB823B59C7EC7F2A7E"
    }

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

    # Initialize an empty dictionary to store processed timestamps for each endpoint
    processed_timestamps = {endpoint: set() for endpoint in endpoints}

    # Initialize an empty list to store dataframes
    dfs = []

    # Iterate over each endpoint to fetch data
    for endpoint in endpoints:
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
            timestamp = i['dateTime']
            if timestamp not in processed_timestamps[endpoint]:
                Loggedtime.append(timestamp)
                processed_timestamps[endpoint].add(timestamp)
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
    DF = result_df[['AppName','LogTime','TestTime','RequestTestResponseTime','WaitTime','SyntheticExperienceScore','AvailabilityPercent']]

    # Injecting DataFrame data into BigQuery
    bq_client = bigquery.Client()

    # Setting the target table name
    table_id = "vz-it-np-jabv-dev-aidplt-0.AIDSRE.SRE_DA_Prod_Reliability_Ingress_CP"

    # Define schema for the table
    schema = [
        bigquery.SchemaField("AppName", "STRING"),
        bigquery.SchemaField("LogTime", "TIMESTAMP"),
        bigquery.SchemaField("TestTime", "FLOAT64"),
        bigquery.SchemaField("RequestTestResponseTime", "FLOAT64"),
        bigquery.SchemaField("WaitTime", "FLOAT64"),
        bigquery.SchemaField("SyntheticExperienceScore", "FLOAT64"),
        bigquery.SchemaField("AvailabilityPercent", "FLOAT64")
    ]

    # Data Append Logic
    job_config = bigquery.LoadJobConfig(schema=schema, write_disposition=bigquery.WriteDisposition.WRITE_APPEND)
    job = bq_client.load_table_from_dataframe(DF, table_id, job_config=job_config)
    print("Data has been successfully pumped to BQ Table")

fetch_and_store_data()