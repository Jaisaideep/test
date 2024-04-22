import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from google.cloud import bigquery

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
    MetricsName = []
    MetricsVal = []

    # Extracting metrics names
    for i in JsonData['data']['favoriteCharts'][0]['summary']['fields']['syntheticMetrics']:
        MetricsName.append(i['name'])

    # Extracting metrics values, logged time, and app name
    for i in JsonData['data']['favoriteCharts'][0]['detail']['items']:
        Loggedtime.append(i['dateTime'])
        AppName.append(i['dimension'][1]['name'])
        MetricsVal.append(i['syntheticMetrics'])

    # Creating a dataframe from the extracted data
    df = pd.DataFrame(data=np.array(MetricsVal), columns=np.array(MetricsName))
    df['AppName'] = AppName
    df['LogTime'] = Loggedtime

    return df

# Function to dump dataframe to BigQuery
def dump_to_bigquery(dataframe, project_id, dataset_id, table_id):
    client = bigquery.Client()
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    # Configure job for loading data into BigQuery
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.job.WriteDisposition.WRITE_APPEND
    )

    # Load dataframe into BigQuery table
    job = client.load_table_from_dataframe(
        dataframe, table_ref, job_config=job_config
    )
    job.result()  # Wait for the job to complete

# Main function triggered by Cloud Function
def main(event, context):
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

    # Specify BigQuery project ID, dataset ID, and table ID
    project_id = 'your_project_id'
    dataset_id = 'your_dataset_id'
    table_id = 'AIDSRE.SRE_DA_Prod_Reliability_Ingress_CP'

    # Dump dataframe to BigQuery
    dump_to_bigquery(result_df, project_id, dataset_id, table_id)

    print("Data dumped to BigQuery successfully.")

SELECT day, ROUND(SUM(SuccessPercent),2) as UserPerformance
FROM
(
select day, successpercent * .30 as SuccessPercent
from `sre_dashboard.ML_DataProc_Job_Success_Percent_Vw`
union all
select day, DataProcUIHealth * .30 as SuccessPercent
from `sre_dashboard.ML_DataProc_UIHealth_Status_Percent`
UNION ALL
Select LogDate as day, WaitTime * .20 as SuccessPercent
FROM AIDSRE.DOMINO_DATAROBOT_WAITTIME_SUMMARY
UNION ALL
Select LogDate as day, ResponseTime * .20 as SuccessPercent
FROM AIDSRE.DOMINO_DATAROBOT_RESPONSETIME_SUMMARY

) Derived
GROUP BY day
