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

# Define the SLI metrics for each category and ILM Stage
sli_metrics = {
    "Domino GCP": {
        "Experience": [
            "Domino Workspace SpinUp Time < 2 Min",
            "Domino Workspace Execution Time < 5 Min",
            "Domino Job Execution Time < 10 Min",
            "% Domino Workspace SpinUp Success Rate",
            "Domino UI Load Time (CP) < 1 Sec",
            "% Domino Job Success Rate",
            "DataProc Job Execution Time < 15 Min",
            "% DataProc Job Success Rate",
            "% of GPUs Available for allocation",
            "% of Workspaces with GitLab size < 2GB",
            "% Usr Mount Space validation < 5GB",
            "% On time Provisioning",
            "% Automated Provisioning",
            "% Errors in Provisioning"
        ],
        "Performance": [
            "% CPU Utilization (GKE)",
            "% Memory Utilization (GKE)",
            "% POD Volume Utilization (GKE)",
            "% POD Restart Metrics (GKE)",
            "% Mongo DB Server CPU Utilization",
            "% Mongo DB Server Memory Utilization",
            "% Connection to MongoDB",
            "% Connection to OneArtifactory from Domino",
            "% GKE Cluster Disk Utilization",
            "% MongoDB Size Utilization",
            "% Domino License Usage"
        ],
        "Compliance": [
            "Security Patch Version Compliance",
            "GKE Version Compliance",
            "Domino Version Compliance",
            "% Gitlab key parameter Compliance",
            "% Correct Env Usage",
            "GKE Cluster Config Changes",
            "% VM Image Compliance",
            "% of User env with DataProc Parameter in Integration",
            "User Domino Key variables",
            "% of User env with Gcloud Auth Login validation",
            "Spark version Compliance",
            "% jobs with < 8 Worker cores",
            "% jobs with < 2 Executer cores",
            "% jobs with Dynamic allocation (T/F)",
            "% with correct Driver memory",
            "Executer memory",
            "VAST ID1 - Actionable Risk Score < 27.00%"
        ]
    },
    "Domino On-Prem": {
        "Experience": [
            "Domino Workspace SpinUp Time < 2 Min",
            "Domino Workspace Execution Time < 5 Min",
            "Domino Job Execution Time < 10 Min",
            "DataProc Job Execution Time < 15 Min",
            "Domino Job Success Rate",
            "DataProc Job Success Rate",
            "Domino Workspace SpinUp Success Rate",
            "Domino UI Load Time (CP) < 1 Sec",
            "% of GPUs Available for allocation",
            "% of Workspaces with GitLab size validation < 2GB",
            "Mount Space validation < 5GB",
            "On time",
            "Auto vs. Manual",
            "Errors in Provisioning"
        ],
        "Performance": [
            "% CPU Utilization (GKE)",
            "% Memory Utilization (GKE)",
            "% POD Volume Utilization (GKE)",
            "% POD Restart Metrics (GKE)",
            "% Mongo DB Server CPU Utilization",
            "% Mongo DB Server Memory Utilization",
            "% Connection to MongoDB",
            "% Connection to OneArtifactory from Domino",
            "% GKE Cluster Disk Utilization",
            "% MongoDB Size Utilization",
            "% Domino License Usage"
        ],
        "Compliance": [
            "Security Patch Version Compliance",
            "GKE Version Compliance",
            "Domino Version Compliance",
            "% Gitlab key parameter Compliance",
            "% Correct Env Usage",
            "GKE Cluster Config Changes",
            "% VM Image Compliance",
            "% of User env with DataProc Parameter in Integration",
            "User Domino Key variables",
            "% of User env with Gcloud Auth Login validation",
            "Spark version Compliance",
            "% jobs with < 2 Worker cores",
            "% jobs with < 2 Executer cores",
            "% jobs with Dynamic allocation config",
            "% with correct Driver memory",
            "Executer memory",
            "Actionable Risk Score < 27.00%",
            "% VM instances with Sysdig Agent",
            "% VM instances with Crowdstrike agent"
        ]
    },
    "Datarobot GCP": {
        "Experience": [
            "DataRobot Load Time (CP) < 2 Sec",
            "DataRobot Datasource connection Time < 1 Min",
            "% DataRobot Job Success Rate",
            "% On time",
            "Auto vs. Manual",
            "% Errors in Provisioning"
        ],
        "Performance": [
            "% CPU Utilization (VM)",
            "% Memory Utilization (VM)",
            "% VM Disk Utilization",
            "% DataRobot License Usage"
        ],
        "Compliance": [
            "OS Image Validation in VM",
            "VM Rehydration validation",
            "Load Balancer SSL certificate validation"
        ]
    },
    "Vertex AI": {
        "Experience": [
            "Vertex AI Model Deployment Time < 5 Min",
            "Vertex AI Prediction Latency < 200 ms",
            "Vertex AI Dataset Import Time < 10 Min",
            "% Vertex AI Job Success Rate",
            "% On time Model Training",
            "% Auto ML Pipeline Success Rate",
            "% Error Rate during Model Training"
        ],
        "Performance": [
            "% CPU Utilization (GKE)",
            "% Memory Utilization (GKE)",
            "% GPU Utilization",
            "% Vertex AI Model Serving Latency < 100 ms",
            "% Disk Utilization (GKE)",
            "% Network Utilization (GKE)"
        ],
        "Compliance": [
            "Security Patch Compliance",
            "Vertex AI Version Compliance",
            "Model Version Compliance",
            "% Key Parameter Compliance"
        ]
    }
}

# Create an empty DataFrame
data = []

# Generate synthetic data
for date in date_range:
    for category in categories:
        for stage, metrics in sli_metrics[category].items():
            for metric in metrics:
                sli_percentage = np.random.uniform(90, 100)  # Random float between 90 and 100
                data.append([date, platform, category, stage, metric, sli_percentage])

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Logdate", "Platform", "Application/Category", "ILM Stage", "SLI Metric", "SLI %"])

# Save to CSV
df.to_csv("ml_synthetic_data.csv", index=False)

print("Synthetic data generated and saved to 'ml_synthetic_data.csv'.")