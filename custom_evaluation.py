# Import libraries
import os
from dotenv import load_dotenv
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

# Create an instance of the custom evaluator
neutrality_eval = NeutralityEvaluator(model_config)

# Test the Neutrality evaluator by evaluating the response
neutrality_score = neutrality_eval(
    response="'Breaking Bad' is widely regarded as one of the best TV shows ever made, according to critics and viewers alike.")
print(neutrality_score)

# Test the Answer Length evaluator by evaluating the response
answer_length_eval = AnswerLengthEvaluator()
print(answer_length_eval(answer="'Breaking Bad' is widely regarded as one of the best TV shows ever made, according to critics and viewers alike."))