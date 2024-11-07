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
        
        # Constructing Cue Words for Evaluating Complexity
        prompt = self.prompt_template.format(problem_description=problem_description)
        messages = [{"role": "system", "content": prompt}]
        
        # Call LLM to evaluate the complexity of the problem
        response = self.llm_call(messages=messages)
        
        # Parsing complexity scores and rationale from responses
        complexity_score = None
        explanation = None
        try:
            if "Complexity Rating:" in response:
                complexity_score = int(response.split("Complexity Rating:")[1].split(".")[0].strip())
                explanation = response.split("Explanation:")[1].strip()
        except Exception as e:
            print(f"Error parsing complexity evaluation response: {e}")
        
        # Update complexity score and rationale to status
        if complexity_score is not None:
            state["complexity_score"] = complexity_score
            state["complexity_explanation"] = explanation
        
        return "Complexity evaluation completed.", state
