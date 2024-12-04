import asyncio
import aiohttp
import os
import json
from nest_asyncio import apply

api_key = "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"

# Asynchronous function to generate responses in batch
async def generate_responses_in_batch_async(prompts, model="gpt-4o", max_tokens=1500):
    responses = []
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        tasks = []
        for prompt in prompts:
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens
            }
            task = session.post(
                "https://api.openai.com/v1/chat/completions",
                json=payload,
                headers=headers
            )
            tasks.append(task)

        # Execute all tasks concurrently
        responses_data = await asyncio.gather(*tasks, return_exceptions=True)

        for response in responses_data:
            if isinstance(response, Exception):
                # Handle exceptions by appending None and printing the error
                responses.append(None)
                print(f"Error: {str(response)}")
            elif response.status == 200:
                # If the response is successful, extract the content
                result = await response.json()
                responses.append(result['choices'][0]['message']['content'])
            else:
                # If the response is not successful, append None and print the status code
                responses.append(None)
                print(f"Error: Received response with status code {response.status}")

    return responses

# Generate prompts for integer programming problems
def generate_ip_prompts(problem_type):
    return {
        "description": (
            f"Write a natural language description of a {problem_type} problem. "
            "This description should be highly realistic and related to practical use cases in industry or society. "
            "Include a clear scenario with specific goals, constraints, and resource limitations. "
            "Provide concrete sample values for all key variables, such as production limits, resource capacities, costs, and profits. "
            "Write the description in a professional, concise, and client-facing tone, as if it were a consulting case. "
            "The description should be plain text, DO NOT use markdown since we need to keep it human readable. "
            "Ensure the scenario references numerical values that will align with the subsequent JSON data."
            "Please keep in your mind to keep a high complexity of the problem. "
            "Do not give any comment, only give the content of the file. "
            "The following is an example: "
            "A scientific research team is equipping a new laboratory and needs to purchase specialized instruments for conducting advanced experiments. The team has a budget of $450,000 and a maximum storage space of 600 square meters for the equipment. "
            "The costs for each piece of equipment are as follows: Equipment 1 costs $60,000, Equipment 2 costs $80,000, Equipment 3 costs $100,000, Equipment 4 costs $75,000, Equipment 5 costs $90,000, Equipment 6 costs $50,000, Equipment 7 costs $85,000, Equipment 8 costs $45,000, Equipment 9 costs $55,000, and Equipment 10 costs $70,000. The corresponding storage requirements (in square meters) are: Equipment 1 requires 50, Equipment 2 requires 70, Equipment 3 requires 80, Equipment 4 requires 65, Equipment 5 requires 60, Equipment 6 requires 40, Equipment 7 requires 75, Equipment 8 requires 30, Equipment 9 requires 35, and Equipment 10 requires 55. "
            "Each piece of equipment has a research value score, which reflects its importance for achieving the team's experimental objectives. The research values are: Equipment 1 has a score of 300, Equipment 2 has a score of 400, Equipment 3 has a score of 500, Equipment 4 has a score of 350, Equipment 5 has a score of 450, Equipment 6 has a score of 250, Equipment 7 has a score of 380, Equipment 8 has a score of 200, Equipment 9 has a score of 280, and Equipment 10 has a score of 320. "
            "Certain pieces of equipment (Equipment 1, Equipment 3, and Equipment 5) are essential for the lab's operation, and at least 3 such essential items must be included in the purchases. The objective is to maximize the total research value while adhering to budget and storage limitations. "
        ),
        "data_json": (
            f"Create a JSON file containing all the essential data parameters for a {problem_type} problem. "
            "Include values for all constraints, costs, capacities, and any other relevant data, using clear key-value pairs. "
            "The structure should only include numerical values or lists of values. Example format: "
            "{{ \"MaxProduction\": 100, \"ProfitPerUnit\": 200, \"ResourceLimits\": [50, 75, 100] }}. "
            "Ensure every value matches the variables and constraints described in the natural language description."
            "Do not give any comment, only give the content of the file. "
            "If you can, don't put the symbols that indicate blocks of code, which is ``` in the output at the same time. "
            "The following is an example: "
            "{ "
            "    \"BudgetLimit\": 450000, "
            "    \"StorageLimit\": 600, "
            "    \"MinEssentialEquipment\": 3, "
            "    \"EquipmentCosts\": [60000, 80000, 100000, 75000, 90000, 50000, 85000, 45000, 55000, 70000], "
            "    \"EquipmentStorage\": [50, 70, 80, 65, 60, 40, 75, 30, 35, 55], "
            "    \"ResearchValueScores\": [300, 400, 500, 350, 450, 250, 380, 200, 280, 320], "
            "    \"EssentialEquipment\": [1, 3, 5] "
            "} "
        ),
        "input_json": (
            f"Create a JSON file that defines the parameters for a {problem_type} problem. "
            "Each parameter should have a definition, symbol, value, and shape (if applicable). "
            "Include a 'description' section that references placeholders (e.g., \\\\param{{ParameterName}}, and do pay attention that ensure that double backslashes are properly rendered in the output) to contextualize the parameters within the problem scenario. "
            "Use the following structure: "
            "{{ "
            "\"parameters\": ["
            "{{ \"definition\": \"Description of parameter\", \"symbol\": \"ParameterName\", \"value\": Value, \"shape\": [] }}, "
            "... ], "
            "\"description\": \"Detailed problem description referencing placeholders, such as \\\\param{{ParameterName}}.\" "
            "}}. "
            "Do not include any comments, only provide the JSON content."
            "If you can, don't put the symbols that indicate blocks of code, which is ``` in the output at the same time. "
            "The following is an example: "
            "{ "
            "    \"parameters\": [ "
            "        { "
            "            \"definition\": \"Total budget available for purchasing laboratory equipment\", "
            "            \"symbol\": \"BudgetLimit\", "
            "            \"value\": 450000, "
            "            \"shape\": [] "
            "        }, "
            "        { "
            "            \"definition\": \"Total storage capacity available for equipment (in square meters)\", "
            "            \"symbol\": \"StorageLimit\", "
            "            \"value\": 600, "
            "            \"shape\": [] "
            "        }, "
            "        { "
            "            \"definition\": \"Minimum number of essential items required for basic lab functionality\", "
            "            \"symbol\": \"MinEssentialEquipment\", "
            "            \"value\": 3, "
            "            \"shape\": [] "
            "        }, "
            "        { "
            "            \"definition\": \"List of costs for each equipment\", "
            "            \"symbol\": \"EquipmentCosts\", "
            "            \"value\": [60000, 80000, 100000, 75000, 90000, 50000, 85000, 45000, 55000, 70000], "
            "            \"shape\": [\"NumEquipment\"] "
            "        }, "
            "        { "
            "            \"definition\": \"List of storage requirements for each equipment (in square meters)\", "
            "            \"symbol\": \"EquipmentStorage\", "
            "            \"value\": [50, 70, 80, 65, 60, 40, 75, 30, 35, 55], "
            "            \"shape\": [\"NumEquipment\"] "
            "        }, "
            "        { "
            "            \"definition\": \"Research value score of each equipment\", "
            "            \"symbol\": \"ResearchValueScores\", "
            "            \"value\": [300, 400, 500, 350, 450, 250, 380, 200, 280, 320], "
            "            \"shape\": [\"NumEquipment\"] "
            "        }, "
            "        { "
            "            \"definition\": \"List of essential equipment that must be included\", "
            "            \"symbol\": \"EssentialEquipment\", "
            "            \"value\": [1, 3, 5], "
            "            \"shape\": [\"MinEssentialEquipment\"] "
            "        } "
            "    ], "
            "    \"description\": \"A research team has a budget of \\\\param{BudgetLimit} dollars and \\\\param{StorageLimit} square meters of space for equipment. Each equipment has a cost \\\\param{EquipmentCosts}, storage requirement \\\\param{EquipmentStorage}, and research value score \\\\param{ResearchValueScores}. Essential equipment \\\\param{EssentialEquipment} require at least \\\\param{MinEssentialEquipment} selections for lab functionality. The objective is to maximize research value within budget and storage constraints.\" "
            "} "
        ),
        "input_targets_json": (
            f"Provide a machine-readable representation of a {problem_type} problem in JSON format. "
            "The file should include four sections: 'background', 'constraints', 'objective', and 'parameters'. "
            "Use this format: "
            "{{ \"background\": \"Brief problem description\", "
            "\"constraints\": [\"List of constraints such as non-negativity, maximum capacities, etc. In natural language description, not in mathematical form.\"], "
            "\"objective\": \"Clearly state the optimization goal (e.g., maximize profit, minimize cost)\", "
            "\"description\": \"A detailed natural language explanation using placeholders like \\\\var{{ParameterName}}\", and do pay attention that ensure that double backslashes are properly rendered in the output"
            "\"parameters\": [{{ \"definition\": \"Parameter explanation\", \"symbol\": \"ParameterName\", \"value\": Value, \"shape\": [] }}, ... ] }}. "
            "Ensure all numerical values align with the description and data JSON files."
            "If you can, don't put the symbols that indicate blocks of code, which is ``` in the output at the same time. "
            "Do not give any comment, only give the content of the file. "
            "The following is an example: "
            "{ "
            "    \"background\": \"A research team is selecting laboratory equipment to maximize research value while adhering to budget and storage constraints.\", "
            "    \"constraints\": [ "
            "        \"The total cost of selected equipment must not exceed BudgetLimit\", "
            "        \"The total storage required for selected equipment must not exceed StorageLimit\", " 
            "        \"At least MinEssentialEquipment items must be selected from the list of EssentialEquipment\", "
            "        \"All costs and storage requirements are non-negative integers\" "
            "    ], "
            "    \"objective\": \"Maximize the total research value score from selected equipment while adhering to budget and storage limits.\", "
            "    \"description\": \"A research team has a budget of \\\\var{BudgetLimit} dollars and \\\\var{StorageLimit} square meters of space for equipment. Each equipment has a cost \\\\var{EquipmentCosts}, storage requirement \\\\var{EquipmentStorage}, and research value score \\\\var{ResearchValueScores}. Essential equipment \\\\var{EssentialEquipment} require at least \\\\var{MinEssentialEquipment} selections for lab functionality. The objective is to maximize research value within budget and storage constraints.\", "
            "    \"parameters\": [ "
            "        { "
            "            \"definition\": \"Total budget available for purchasing laboratory equipment\", "
            "            \"symbol\": \"BudgetLimit\", "
            "            \"value\": 450000, "
            "            \"shape\": [] "
            "        }, "
            "        { "
            "            \"definition\": \"Total storage capacity available for equipment (in square meters)\", "
            "            \"symbol\": \"StorageLimit\", "
            "            \"value\": 600, "
            "            \"shape\": [] "
            "        }, "
            "        { "
            "            \"definition\": \"Minimum number of essential items required for basic lab functionality\", "
            "            \"symbol\": \"MinEssentialEquipment\", "
            "            \"value\": 3, "
            "            \"shape\": [] "
            "        }, "
            "        { "
            "            \"definition\": \"List of costs for each equipment\", "
            "            \"symbol\": \"EquipmentCosts\", "
            "            \"value\": [60000, 80000, 100000, 75000, 90000, 50000, 85000, 45000, 55000, 70000], "
            "            \"shape\": [\"NumEquipment\"] "
            "        }, "
            "        { "
            "            \"definition\": \"List of storage requirements for each equipment (in square meters)\", "
            "            \"symbol\": \"EquipmentStorage\", "
            "            \"value\": [50, 70, 80, 65, 60, 40, 75, 30, 35, 55], "
            "            \"shape\": [\"NumEquipment\"] "
            "        }, "
            "        { "
            "            \"definition\": \"Research value score of each equipment\", "
            "            \"symbol\": \"ResearchValueScores\", "
            "            \"value\": [300, 400, 500, 350, 450, 250, 380, 200, 280, 320], "
            "            \"shape\": [\"NumEquipment\"] "
            "        }, "
            "        { "
            "            \"definition\": \"List of essential equipment that must be included\", "
            "            \"symbol\": \"EssentialEquipment\", "
            "            \"value\": [1, 3, 5], "
            "            \"shape\": [\"MinEssentialEquipment\"] "
            "        } "
            "    ] "
            "} "
        )
    }

# Main function for batch generation of multiple sets of files asynchronously
# Load generation status from a log file
def load_generation_status(log_file="generation_status.log"):
    # Check if the log file exists and load its content, otherwise return an empty dictionary
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            return json.load(file)
    return {}

# Save generation status to a log file
def save_generation_status(status, log_file="generation_status.log"):
    # Write the current generation status to the log file
    with open(log_file, "w") as file:
        json.dump(status, file, indent=4)

# Main function for batch generation of multiple sets of files asynchronously with recovery
async def batch_generate_multiple_sets_async(problem_type, batch_count=3, log_file="generation_status.log"):
    # Load the current status
    generation_status = load_generation_status(log_file)

    for batch_index in range(batch_count):
        batch_key = f"batch_{batch_index + 1}"

        # Initialize the generation status for the current batch if not already present
        if batch_key not in generation_status:
            generation_status[batch_key] = {
                "description": False,
                "data_json": False,
                "input_json": False,
                "input_targets_json": False
            }

        prompts_dict = generate_ip_prompts(problem_type)

        # Create a list of prompts to generate responses for each output format
        prompts_list = [
            prompts_dict['description'],
            prompts_dict['data_json'],
            prompts_dict['input_json'],
            prompts_dict['input_targets_json']
        ]

        # Create a folder for the current batch
        batch_folder = f"prob_{batch_index + 1}"
        if not os.path.exists(batch_folder):
            os.makedirs(batch_folder)

        # Define fixed filenames for each output
        output_files = [
            os.path.join(batch_folder, "description.txt"),
            os.path.join(batch_folder, "data.json"),
            os.path.join(batch_folder, "input.json"),
            os.path.join(batch_folder, "input_targets.json")
        ]

        # Generate responses for all prompts at once if not already done
        if not all(generation_status[batch_key].values()):
            responses_list = await generate_responses_in_batch_async(prompts_list)

            # Iterate over each response and save if not already done
            for index, (response, output_file) in enumerate(zip(responses_list, output_files)):
                key = list(generation_status[batch_key].keys())[index]

                # Skip saving if the file has already been successfully generated
                if generation_status[batch_key][key]:
                    print(f"Skipping {output_file} as it has already been generated.")
                    continue

                if response is not None:
                    # Save the generated response to the appropriate file
                    with open(output_file, "w", encoding="utf-8") as file:
                        file.write(response)
                    print(f"{output_file} saved successfully.")
                    # Update the generation status to mark this file as done
                    generation_status[batch_key][key] = True
                else:
                    print(f"Error generating {output_file}, response was None.")

            # Save the updated status after each attempt
            save_generation_status(generation_status, log_file)

if __name__ == "__main__":
    import nest_asyncio
    apply()
    problem_type = "multivariate integer complex programming problem"
    loop = asyncio.get_event_loop()
    if loop.is_running():
        task = loop.create_task(batch_generate_multiple_sets_async(problem_type, batch_count=5))
        loop.run_until_complete(task)
    else:
        asyncio.run(batch_generate_multiple_sets_async(problem_type, batch_count=5))
