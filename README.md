# Azure AI Foundry Custom Evaluation

## Overview
This repo contains sample code for creating and running custom evaluators in Azure AI Foundry.

---

## Getting Started

Follow these steps to set up and run the code:

### 1. Install Requirements
Ensure you have Python installed. I used version 3.11. The latest Python version, 3.13, is incompatible with some functions in the Azure AI Foundry SDK. Then, install the required dependencies:

`pip install -r requirements.txt`

### 2. Update the `.env` File
The project requires certain secrets and configuration values to be set in the `.env` file. Update the `.env` file with your secrets and configuration values.

## File Descriptions
Here’s a summary of what each file in this repository does:

- **`cloud_evaluation.py`**: Contains logic for running custom evaluators in Azure AI Foundry.
  
- **`local_evaluation.py`**: Runs local evaluations (Will not show up in the Foundry portal).

- **`custom_evaluation.py`**: Initial testing of custom evaluators (similar to `local_evaluation.py`, can ignore).

- **`microsoft_evaluation.py`**: Runs Microsoft evaluators in Foundry.

- **`neutrality/`**: Contains code for the neutrality custom evaluator.

- **`neutrality_local/`**: The artifacts created after registering the neutrality custom evaluator.

- **`evaluator_registration/`**: Contains code for registering the custom evaluators (pushes evaluators to the "Evaluators" section of Azure AI Foundry).

- **`data/`**: Contains the sample data.

- **`answer_len/`, `answer_len_local/`**: Similar to the neutrality artifacts.

## Running the Code

Once you've installed the requirements and updated your `.env` file, run any script by executing it with Python:

`python file_name.py`




