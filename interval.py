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

    # Initialize an empty dictionary to store the latest processed timestamp for each endpoint
    latest_processed_timestamps = {endpoint: None for endpoint in endpoints}

    # Initialize an empty list to store dataframes
    dfs = []

    # Iterate over each endpoint to fetch data
    for endpoint in endpoints:
        # Get the latest processed timestamp for this endpoint
        latest_processed_timestamp = latest_processed_timestamps[endpoint]

        # Make the API request
        JsonData = requests.get(endpoint, params=parameters, headers=headers).json()

        # Extracting data from the JSON response
        Loggedtime = []
        AppName = []
        MetricHeader = []
        MetricData = []

        # Extracting metrics values, logged time, and app name
        for i in JsonData['data']['favoriteCharts'][0]['detail']['items']:
            timestamp = i['dateTime']
            # Check if the timestamp is newer than the latest processed one
            if latest_processed_timestamp is None or timestamp > latest_processed_timestamp:
                Loggedtime.append(timestamp)
                AppName.append(i['dimension'][1]['name'])
                MetricData.append(i['syntheticMetrics'])

        # Update the latest processed timestamp for this endpoint
        if Loggedtime:
            latest_processed_timestamps[endpoint] = max(Loggedtime)

        # Creating a dataframe from the extracted data
        df = pd.DataFrame(data=np.array(MetricData), columns=np.array(MetricHeader))
        df['AppName'] = AppName
        df['LogTime'] = pd.to_datetime(Loggedtime)  # Convert 'LogTime' to datetime

        # Append the dataframe to the list
        dfs.append(df)

    # Check if any data was retrieved
    if dfs:
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
    else:
        print("No new data retrieved")

fetch_and_store_data()