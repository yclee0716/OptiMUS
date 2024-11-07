from typing import Dict
from agents.agent import Agent
import json
import openai

class ComplexityEvaluator(Agent):
    def __init__(self, client: openai.Client, **kwargs):
        super().__init__(
            name="ComplexityEvaluator",
            description="This is an agent that evaluates the complexity of the optimization problem based on user input and problem description.",
            client=client,
            **kwargs
        )
        self.prompt_template = """
You are an expert in evaluating the complexity of optimization problems. Your task is to evaluate the complexity level of the given problem on a scale from 1 to 10, where 1 is very simple and 10 is extremely complex.

Here is the problem description:
-----
{problem_description}
-----

Please provide a numeric rating between 1 and 10 for the complexity of this problem, along with a brief explanation of why you assigned this rating.
"""

    def generate_reply(self, task: str, state: Dict, sender: Agent) -> (str, Dict):
        # Get a description of the problem provided by the user
        problem_description = state.get("problem_description", "No description available.")

        # Get an initial score
        initial_complexity = self.evaluate_complexity(state)
        initial_score = initial_complexity["score"]
        initial_details = initial_complexity["details"]
        
        # Constructing the prompt for evaluating complexity
        prompt = self.prompt_template.format(problem_description=problem_description)
        messages = [{"role": "system", "content": prompt}]
        
        # Call LLM to evaluate the complexity of the problem
        response = self.llm_call(messages=messages)
        
        # Parsing complexity scores and rationale from responses
        complexity_score = None
        explanation = None
        
        try:
            # Use a more structured approach to parse the response
            response_lines = response.splitlines()
            for line in response_lines:
                if "Complexity Rating:" in line:
                    complexity_score = int(line.split(":")[1].strip())
                elif "Explanation:" in line:
                    explanation = line.split(":", 1)[1].strip()

            # Fallback in case structured parsing fails
            if complexity_score is None:
                complexity_score = int(response.split("Complexity Rating:")[1].split()[0].strip())
            if explanation is None:
                explanation = response.split("Explanation:")[1].strip()

        except Exception as e:
            print(f"Error parsing complexity evaluation response: {e}")
            complexity_score = 5  # Default score in case of error
            explanation = "Could not parse the explanation correctly. Assigned a default complexity score."

        # Update complexity score and rationale to state
        state["complexity_score"] = complexity_score
        state["complexity_explanation"] = explanation
        
        return "Complexity evaluation completed.", state

    def evaluate_complexity(self, state: Dict) -> Dict:
        # Extract problem features
        num_parameters = len(state.get("parameters", []))
        num_constraints = len(state.get("constraints", []))
        objective_defined = bool(state.get("objective"))

        # Simple heuristic to determine initial complexity
        complexity_score = min(10, num_parameters + num_constraints)
        
        # Adjust score based on specific characteristics
        if objective_defined:
            complexity_score += 1

        # Cap complexity score at 10
        complexity_score = min(10, complexity_score)
        
        # Provide detailed complexity explanation
        complexity_details = {
            "parameter_count": num_parameters,
            "constraint_count": num_constraints,
            "objective_defined": objective_defined,
            "comments": f"The problem involves {num_parameters} parameters and {num_constraints} constraints. The objective function is {'defined' if objective_defined else 'not defined'}, which adds to the problem complexity.",
        }

        return {
            "score": complexity_score,
            "details": complexity_details,
        }
