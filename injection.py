import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from google.cloud import bigquery

def fetch_and_store_data():
    """
    Fetches data from multiple endpoints, consolidates it into a dataframe,
    and stores new records in a BigQuery table.

    Returns:
        str: A message indicating the completion of data extraction and storage.
    """
    # Set headers for the request
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
    final_df = pd.concat(dfs, ignore_index=True)

    # Reordering the columns
    final_df = final_df[['AppName','LogTime','TestTime','RequestTestResponseTime','WaitTime','SyntheticExperienceScore','AvailabilityPercent']]

    # Initialize variable to store old max timestamp
    old_max_time = datetime.min

    # Dataframe to store the new records alone
    new_records_df = pd.DataFrame()

    # Injecting DataFrame data into BigQuery
    bq_client = bigquery.Client()

    # Setting the target table name
    table_id = "vz-it-pr-jabv-aidplt-0.AIDSRE.SRE_DA_Prod_Reliability_Ingress_CP"

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

    # Check if it's the first run or not
    if bq_client.get_table(table_id).num_rows > 0:
        # Get old max timestamp from the existing table
        query = f"SELECT MAX(LogTime) FROM `{table_id}`"
        old_max_time_result = bq_client.query(query).result().to_dataframe()
        if not old_max_time_result.empty:
            old_max_time = old_max_time_result.iloc[0, 0]

    # Filter new records from the result dataframe
    new_records_df = final_df[final_df['LogTime'] > old_max_time]

    # Append new records to the existing table
    if not new_records_df.empty:
        job_config = bigquery.LoadJob