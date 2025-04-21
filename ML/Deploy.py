from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import ManagedOnlineEndpoint, ManagedOnlineDeployment
import requests

# Initialize MLClient
ml_client = MLClient(DefaultAzureCredential(), "afdfbcba-0f7e-4bf8-9f21-19b34a0c6be5", "Jake", "JakeWS")

# Create a local endpoint instead of a cloud-managed online endpoint
endpoint = ManagedOnlineEndpoint(
    name="JobTitlesEndpoint",
    auth_mode="key"  # Local endpoints typically use key-based authentication
)

ml_client.online_endpoints.begin_create_or_update(endpoint).result()

# Adjust deployment settings for local execution
deployment = ManagedOnlineDeployment(
    name="jobTitlesML",
    endpoint_name="JobTitlesEndpoint",
    model="jobTitlesRandomForestModel:1",
    instance_type="local",  # Use "local" to indicate on-prem execution
    instance_count=1,  # Local setups usually work with single instances
)

ml_client.online_deployments.begin_create_or_update(deployment).result()

# Test the local endpoint
response = requests.post("http://localhost:5001/jobTitlesEndpoint/predict", json={"input_data": {"columns": [], "data": []}})
print(response.json())

# url = "https://your-endpoint-name.region.inference.azureml.net/score"
# headers = {"Authorization": "Bearer your-access-token"}
# data = {"input_data": [[your_test_data]]}

# response = requests.post(url, json=data, headers=headers)
# print(response.json())