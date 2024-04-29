import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Function to generate random start time within the specified date range
def generate_start_time(created_date):
    max_duration = timedelta(days=2)
    max_seconds = int(max_duration.total_seconds())
    start_time = created_date + timedelta(minutes=random.randint(0, max_seconds // 60))
    return start_time

# Generate sample data
data = []
for _ in range(130):
    created_date = datetime.strptime("2024-04-18", "%Y-%m-%d") + timedelta(days=random.randint(0, 7))
    start_time = generate_start_time(created_date)
    status = 'Closed' if random.random() < 0.8 else 'Open'
    closed_date = start_time + timedelta(minutes=random.randint(30, 1440)) if status == 'Closed' else None
    mtta = str(start_time - created_date)
    mttr = str(closed_date - created_date) if closed_date else None
    jira_ref = 'AIML-' + str(random.randint(1000, 9999))
    priority = 'P' + str(random.randint(1, 3))
    data.append([created_date, status, jira_ref, priority, start_time, mtta, mttr])

# Create DataFrame
columns = ['Created Date', 'Status', 'Jira Ref#', 'Priority', 'Start Time', 'MTTA', 'MTTR']
df = pd.DataFrame(data, columns=columns)

# Export DataFrame to CSV
df.to_csv('sample_data_with_timestamp.csv', index=False)