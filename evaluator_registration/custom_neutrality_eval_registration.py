import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Model
from promptflow.client import PFClient

load_dotenv()

# Import your prompt-based custom evaluator
from neutrality.neutral import NeutralityEvaluator

# Define your deployment 
model_config = dict(
    azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
    azure_deployment=os.environ.get("AZURE_DEPLOYMENT_NAME"),
    api_version=os.environ.get("AZURE_API_VERSION"),
    api_key=os.environ.get("AZURE_API_KEY")
)

# Define ml_client to register custom evaluator
ml_client = MLClient(
       subscription_id=os.environ.get("AZURE_SUBSCRIPTION_ID"),
       resource_group_name=os.environ.get("AZURE_RESOURCE_GROUP"),
       workspace_name=os.environ.get("AZURE_PROJECT_NAME"),
       credential=DefaultAzureCredential()
)

# # Convert evaluator to evaluation flow and save it locally
local_path = "neutrality_local"
pf_client = PFClient()
pf_client.flows.save(entry=NeutralityEvaluator, path=local_path) 

# Specify evaluator name to appear in the Evaluator library
evaluator_name = "NeutralityEvaluator"

# Register the evaluator to the Evaluator library
custom_evaluator = Model(
    path=local_path,
    name=evaluator_name,
    description="prompt-based custom evaluator measuring response neutrality.",
)
registered_evaluator = ml_client.evaluators.create_or_update(custom_evaluator)
print("Registered evaluator id:", registered_evaluator.id)
# Registered evaluators have versioning. You can always reference any version available.
versioned_evaluator = ml_client.evaluators.get(evaluator_name, version=1)
print("Versioned evaluator id:", registered_evaluator.id)