# Import libraries
import os
from dotenv import load_dotenv
from azure.ai.evaluation import evaluate
from neutrality.neutral import NeutralityEvaluator
from answer_len.answer_length import AnswerLengthEvaluator

# Load the environment variables
load_dotenv()

# Define your model config
model_config = {
    "azure_endpoint": os.environ.get("AZURE_OPENAI_ENDPOINT"),
    "api_key": os.environ.get("AZURE_OPENAI_API_KEY"),
    "azure_deployment": os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
    "api_version": os.environ.get("AZURE_OPENAI_API_VERSION"),
}

# Create instances of the custom evaluators
answer_length = AnswerLengthEvaluator()
neutrality_eval = NeutralityEvaluator(model_config)

# Evaluate the response using the custom evaluators
if __name__ == '__main__':
    result = evaluate(
        data="C:/Users/simani/OneDrive - Microsoft/Desktop/azure-ai-evaluation/data/evaluation_data.jsonl", # provide your data here
        evaluators={
            "neutrality": neutrality_eval,
            "answer_length": answer_length
        },
        # Column mapping
        evaluator_config={
            "answer_length": {
                "column_mapping": {
                    "answer": "${data.response}"
                } 
            },
            "neutrality": {
                "column_mapping": {
                    "response": "${data.response}"
                }
            }
        },
        # Optionally provide your Azure AI project information to track your evaluation results in your Azure AI project
        # azure_ai_project = azure_ai_project,
        # Optionally provide an output path to dump a json of metric summary, row level data and metric and Azure AI project URL
        output_path="./output/evalresults.json"
    )