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
        # 获取用户提供的问题描述
        problem_description = state.get("problem_description", "No description available.")
        
        # 构建评估复杂度的提示词
        prompt = self.prompt_template.format(problem_description=problem_description)
        messages = [{"role": "system", "content": prompt}]
        
        # 调用 LLM 来评估问题的复杂度
        response = self.llm_call(messages=messages)
        
        # 从响应中解析出复杂度评分和理由
        complexity_score = None
        explanation = None
        try:
            # 假设响应是形如 "Complexity Rating: 7. Explanation: This problem is challenging because..." 的文本
            if "Complexity Rating:" in response:
                complexity_score = int(response.split("Complexity Rating:")[1].split(".")[0].strip())
                explanation = response.split("Explanation:")[1].strip()
        except Exception as e:
            print(f"Error parsing complexity evaluation response: {e}")
        
        # 将复杂度评分和理由更新到状态中
        if complexity_score is not None:
            state["complexity_score"] = complexity_score
            state["complexity_explanation"] = explanation
        
        return "Complexity evaluation completed.", state
