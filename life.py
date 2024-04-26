import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pandas_gbq import to_gbq
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

def fetch_and_store_data():
    # Set parameters and headers for the request
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
    result_df = result_df[['AppName', 'LogTime', 'TestTime', 'RequestTestResponseTime', 'WaitTime',
                           'SyntheticExperienceScore', 'AvailabilityPercent']]

    # Initialize Google BigQuery client
    client = bigquery.Client()

    # Define BQ Table Details
    project_id = "vz-it-np-jabv-dev-aidplt-0"
    table_name = "AIDSRE.SRE_DA_Prod_Reliability_Ingress_CP"
    table_ref = client.dataset("AIDSRE").table("SRE_DA_Prod_Reliability_Ingress_CP")

    # Check if the table exists
    try:
        table = client.get_table(table_ref)
        table_exists = True
    except NotFound:
        table_exists = False

    if table_exists:
        # Query BigQuery to get the maximum timestamp
        query = f"SELECT MAX(LogTime) AS max_timestamp FROM {table_name}"
        max_timestamp_df = client.query(query).to_dataframe()
        max_timestamp = max_timestamp_df['max_timestamp'][0]

        # Filter records in result_df based on timestamps
        new_records = result_df[result_df['LogTime'] > max_timestamp]

        if not new_records.empty:
            # Append new records to the existing table
            to_gbq(new_records, destination_table=table_name, project_id=project_id, if_exists="append")
            print("New data appended to the existing table.")
            print("Start Timestamp:", new_records['LogTime'].min())
            print("End Timestamp:", new_records['LogTime'].max())
        else:
            print("No new records to append.")
    else:
        # Create a new table and insert all data
        to_gbq(result_df, destination_table=table_name, project_id=project_id, if_exists="replace")
        print("New table created and data inserted.")
        print("Start Timestamp:", result_df['LogTime'].min())
        print("End Timestamp:", result_df['LogTime'].max())

    print("Done")

# Call the function to fetch and store data
fetch_and_store_data()