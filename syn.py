# Generate sample data
data = []
for _ in range(130):
    created_date = datetime.strptime("2024-04-18", "%Y-%m-%d") + timedelta(days=random.randint(0, 7))
    start_time, end_time = generate_time(created_date)
    status = 'Closed' if random.random() < 0.8 and end_time is not None else 'Open'
    closed_date = start_time + timedelta(minutes=random.randint(30, 1440)) if status == 'Closed' else None
    mttr = str(end_time - start_time) if status == 'Closed' else None
    jira_ref = 'AIML-' + str(random.randint(1000, 9999))
    priority = 'P' + str(random.randint(1, 3))
    data.append([created_date, status, jira_ref, priority, start_time, end_time, mttr, closed_date])

# Create DataFrame
columns = ['Created Date', 'Status', 'Jira Ref#', 'Priority', 'Start Time', 'End Time', 'MTTR', 'Closed Date']
df = pd.DataFrame(data, columns=columns)

# Export DataFrame to CSV
df.to_csv('sample_data_with_timestamp.csv', index=False)