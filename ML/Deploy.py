from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import ManagedOnlineEndpoint
from azure.ai.ml.entities import ManagedOnlineDeployment


import requests

ml_client = MLClient(DefaultAzureCredential(), "afdfbcba-0f7e-4bf8-9f21-19b34a0c6be5", "Jake", "JakeWS")

endpoint = ManagedOnlineEndpoint(
    name="JobTitlesEndpoint"
)

ml_client.online_endpoints.begin_create_or_update(endpoint).result()

deployment = ManagedOnlineDeployment(
    name="jobTitlesML",
    endpoint_name="JobTitlesEndpoint",
    model="jobTitlesRandomForestModel:1",
    instance_type="Standard_D2as_v4",
    instance_count=1,
)

ml_client.online_deployments.begin_create_or_update(deployment).result()

# url = "https://your-endpoint-name.region.inference.azureml.net/score"
# headers = {"Authorization": "Bearer your-access-token"}
# data = {"input_data": [[your_test_data]]}

# response = requests.post(url, json=data, headers=headers)
# print(response.json())