import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Define the date range
start_date = datetime.strptime("2024-06-03", "%Y-%m-%d")
end_date = datetime.strptime("2024-06-10", "%Y-%m-%d")
date_range = pd.date_range(start_date, end_date)

# Define the platforms and categories
platform = "ML"
categories = ["Domino GCP", "Domino On-Prem", "Datarobot GCP", "Vertex AI"]

# Create an empty DataFrame
data = []

# Generate synthetic data
for date in date_range:
    for category in categories:
        experience = np.random.uniform(90, 100)  # Random float between 90 and 100
        performance = np.random.uniform(90, 100)  # Random float between 90 and 100
        compliance = np.random.uniform(90, 100)  # Random float between 90 and 100
        data.append([date, platform, category, experience, performance, compliance])

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Logdate", "Platform", "Application/Category", "Experience%", "Performance%", "Compliance%"])

# Save to CSV
df.to_csv("ml_synthetic_data.csv", index=False)

print("Synthetic data generated and saved to 'ml_synthetic_data.csv'.")