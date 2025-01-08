# Import libraries
import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import Evaluation, Dataset, EvaluatorConfiguration, ConnectionType
from azure.ai.evaluation import F1ScoreEvaluator, RelevanceEvaluator, ViolenceEvaluator

load_dotenv()

# Load Azure OpenAI config
deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
api_version = os.environ.get("AZURE_OPENAI_API_VERSION")

# Create an Azure AI Client from a connection string - from project overview page on Azure AI project UI.
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str="eastus2.api.azureml.ms;2d0ee675-17ff-4b13-a230-e84531ba4eab;rg-mani-ai-demos;content-safety-demo"
)

# Dataset ID is used to identify the evaluation dataset uploaded to Azure AI
data_id = "/subscriptions/2d0ee675-17ff-4b13-a230-e84531ba4eab/resourceGroups/rg-mani-ai-demos/providers/Microsoft.MachineLearningServices/workspaces/content-safety-demo/data/evaluation_data/versions/3"

# Connect to the Azure AI project - entrypoint for the cloud evaluation
default_connection = project_client.connections.get_default(connection_type=ConnectionType.AZURE_OPEN_AI)

# Specify the model that will be used to perform the neutrality evaluation.
# Neutrality is a custom, prompt-based evaluator so it uses a LLM to process the prompt
model_config = default_connection.to_evaluator_model_config(deployment_name=deployment_name, api_version=api_version)

# Create an evaluation
evaluation = Evaluation(
    display_name="Cloud evaluation - gpt-4o-mini", # Will show up in Azure AI evaluations with this name
    description="Evaluation of dataset",
    data=Dataset(id=data_id),
    evaluators={
        # The evaluator configuration key must follow a naming convention
        # the string must start with a letter with only alphanumeric characters 
        # and underscores. Take "f1_score" as example: "f1score" or "f1_evaluator" 
        # will also be acceptable, but "f1-score-eval" or "1score" will result in errors.
        "answer_length": EvaluatorConfiguration(
            id="azureml://locations/eastus2/workspaces/39d3a945-8784-4137-846f-cfc4518fb093/models/AnswerLenEvaluator/versions/1",
            data_mapping={
                "answer": "${data.response}" # The model expects an input variable, answer, so this needs to be mapped to what's present in the evaluation dataset
            }
        ),
        "neutrality": EvaluatorConfiguration(
            id="azureml://locations/eastus2/workspaces/39d3a945-8784-4137-846f-cfc4518fb093/models/NeutralityEvaluator/versions/2", # Specify the Neutrality Evaluator that is uploaded to the Azure AI project
            init_params={
                "model_config": model_config # Specify the model config since Neutrality is a prompt-based evaluator
            }
        )
    },
)

# Create evaluation - this starts the automated evaluation in Azure AI
evaluation_response = project_client.evaluations.create(
    evaluation=evaluation,
)

# Get evaluation info
get_evaluation_response = project_client.evaluations.get(evaluation_response.id)

print("----------------------------------------------------------------")
print("Created evaluation, evaluation ID: ", get_evaluation_response.id)
print("Evaluation status: ", get_evaluation_response.status)
print("AI project URI: ", get_evaluation_response.properties["AiStudioEvaluationUri"])
print("----------------------------------------------------------------")