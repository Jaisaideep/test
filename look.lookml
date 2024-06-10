import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Define the date range
start_date = datetime.strptime("2024-06-03", "%Y-%m-%d")
end_date = datetime.strptime("2024-06-10", "%Y-%m-%d")
date_range = pd.date_range(start_date, end_date)

# Define the platforms, categories, and services
platform = "ML"
categories_services = {
    "Domino GCP": ["Domino", "GKE Cluster", "Mongo DB", "One Artifactory"],
    "Domino On-Prem": ["Domino", "GKE Cluster", "Mongo DB", "One Artifactory"],
    "Datarobot GCP": ["DataRobot", "GKE Cluster", "Mongo DB", "One Artifactory"],
    "Vertex AI": ["Vertex AI", "GKE Cluster", "Mongo DB", "One Artifactory"]
}

# Create an empty DataFrame
data = []

# Generate synthetic data
for date in date_range:
    for category, services in categories_services.items():
        for service in services:
            availability = np.random.uniform(85, 100)  # Random float between 85 and 100
            data.append([date, platform, category, service, availability])

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Logdate", "Platform", "Application/Category", "Services", "Availability%"])

# Save to CSV
df.to_csv("ml_synthetic_data.csv", index=False)

print("Synthetic data generated and saved to 'ml_synthetic_data.csv'.")