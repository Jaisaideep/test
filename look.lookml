import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Define the date range
start_date = datetime.strptime("2024-06-03", "%Y-%m-%d")
end_date = datetime.strptime("2024-06-10", "%Y-%m-%d")
date_range = pd.date_range(start_date, end_date)

# Define the platforms and ILM stages
platforms = ["ML", "BI Tools", "Teradata", "Hadoop", "GCP", "D&A"]
ilm_stages = ["Experience", "Performance", "Compliance"]

# Create an empty DataFrame
data = []

# Generate synthetic data
for date in date_range:
    for platform in platforms:
        for stage in ilm_stages:
            ilm_percentage = np.random.uniform(90, 100)  # Random float between 90 and 100
            data.append([date, platform, stage, ilm_percentage])

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Logdate", "Platform", "ILM Stage Metric", "ILM %"])

# Save to CSV
df.to_csv("ilm_synthetic_data.csv", index=False)

print("Synthetic data generated and saved to 'ilm_synthetic_data.csv'.")