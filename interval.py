import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from google.cloud import bigquery

url = "http://io.catchpoint.com/api/v2/tests/explorer/favoritechart/data/35581"

start_time = "2024-04-16T10:30:00Z"
end_time = "2024-04-16T11:00:00Z"

payload = {"start": start_time,"end": end_time} 
headers = {"Content-Type": "application/json","Authorization": "Bearer AD9E312743A1DE9278FBB05BB3D2057AAA9A5839E625D8BB823B59C7EC7F2A7E"}
  

response = requests.get(url,params=payload, headers=headers).json()
print(response)
