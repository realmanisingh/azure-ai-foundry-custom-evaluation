# Import libraries
import os
from azure.identity import DefaultAzureCredential
from azure.ai.evaluation import GroundednessProEvaluator, GroundednessEvaluator
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Load credentials
credential = DefaultAzureCredential()

# Initialize Azure AI project and Azure OpenAI connection with the environment variables
azure_ai_project = {
    "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID"),
    "resource_group_name": os.environ.get("AZURE_RESOURCE_GROUP"),
    "project_name": os.environ.get("AZURE_PROJECT_NAME"),
}

# Define the model config
model_config = {
    "azure_endpoint": os.environ.get("AZURE_OPENAI_ENDPOINT"),
    "api_key": os.environ.get("AZURE_OPENAI_API_KEY"),
    "azure_deployment": os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
    "api_version": os.environ.get("AZURE_OPENAI_API_VERSION"),
}

# Initialzing Groundedness and Groundedness Pro evaluators
groundedness_eval = GroundednessEvaluator(model_config)
groundedness_pro_eval = GroundednessProEvaluator(azure_ai_project=azure_ai_project, credential=credential)

# Define a query and response pair for evaluation
query_response = dict(
    query="Which tent is the most waterproof?",
    context="The Alpine Explorer Tent is the most water-proof of all tents available.",
    response="The Alpine Explorer Tent is the most waterproof."
)

# Running Groundedness Evaluator on a query and response pair
groundedness_score = groundedness_eval(
    **query_response
)
print(groundedness_score)

# Running Groundedness Pro Evaluator on a query and response pair
groundedness_pro_score = groundedness_pro_eval(
    **query_response
)
print(groundedness_pro_score)