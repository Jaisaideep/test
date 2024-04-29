import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Function to generate random start and end times within the specified date range
def generate_times(created_date):
    max_duration = timedelta(days=2)
    max_seconds = int(max_duration.total_seconds())
    start_time = created_date + timedelta(minutes=random.randint(0, max_seconds // 60))
    end_time = start_time + timedelta(minutes=random.randint(15, 240))
    return start_time, end_time

# Generate sample data
data = []
for _ in range(130):
    created_date = datetime.strptime("2024-04-18", "%Y-%m-%d") + timedelta(days=random.randint(0, 7)) + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))
    start_time, end_time = generate_times(created_date)
    status = 'Closed' if random.random() < 0.8 else 'Open'
    closed_date = end_time if status == 'Closed' else None
    mtta = str(start_time - created_date)
    mttr = str(end_time - created_date) if closed_date else None
    jira_ref = 'AIML-' + str(random.randint(1000, 9999))
    priority = 'P' + str(random.randint(1, 3))
    data.append([created_date, start_time, end_time, status, jira_ref, priority, mtta, mttr])

# Create DataFrame
columns = ['Created Date', 'Start Time', 'End Time', 'Status', 'Jira Ref#', 'Priority', 'MTTA', 'MTTR']
df = pd.DataFrame(data, columns=columns)

# Export DataFrame to CSV
df.to_csv('sample_data_with_timestamp.csv', index=False)