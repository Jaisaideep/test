import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Define the date range
start_date = datetime.strptime("2024-06-03", "%Y-%m-%d")
end_date = datetime.strptime("2024-06-10", "%Y-%m-%d")
date_range = pd.date_range(start_date, end_date)

# Define the platforms, categories, and services
platform = "GCP"
categories_services = {
    "Storage": ["GCS", "Local SSD"],
    "Compute": ["Cloud Functions", "Cloud Run", "GCE", "GKE"],
    "Data & Analytics": ["BigQuery", "Composer", "Dataflow", "Dataproc", "Pub/Sub", "Data Catalog", "Data Fusion"],
    "Database": ["BigTable", "CloudSQL", "Memory Store"],
    "Developer Tools": ["Artifact Registry", "Cloud Build", "Cloud Scheduler", "Cloud SDK"]
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
df.to_csv("synthetic_data.csv", index=False)

print("Synthetic data generated and saved to 'synthetic_data.csv'.")