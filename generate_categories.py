import asyncio
import aiohttp
import os
import json
from nest_asyncio import apply

# Step 1: 生成问题类型和领域的分类库
def generate_problem_categories(file_path="categories.json"):
    categories = {
        "academic": {
            "combinatorial_optimization": [
                "0-1 knapsack problem", "multi-knapsack problem", "fractional knapsack problem", "multi-dimensional knapsack problem"
            ],
            "traveling_salesman_problem": [
                "symmetric TSP", "asymmetric TSP", "multi-TSP", "TSP with time windows"
            ],
            "facility_location": [
                "fixed cost facility location problem", "capacitated facility location", "p-median problem", "p-center problem"
            ],
            "network_design": [
                "minimum spanning tree", "Steiner tree", "network flow design"
            ],
            "scheduling": [
                "single machine scheduling", "parallel machine scheduling", "flow shop scheduling", "job shop scheduling"
            ],
            "assignment": [
                "assignment problem", "generalized assignment problem", "quadratic assignment problem"
            ],
            "inventory_management": [
                "economic order quantity", "dynamic lot-sizing"
            ],
            "set_covering_partitioning": [
                "minimum set covering", "maximum set covering"
            ],
            "vehicle_routing": [
                "basic VRP", "VRP with time windows", "capacitated VRP"
            ],
            "cutting_packing": [
                "one-dimensional bin packing", "two-dimensional bin packing"
            ],
            "graph_theory": [
                "graph coloring problem", "maximum clique problem"
            ],
            "resource_allocation": [
                "project selection and scheduling", "personnel rostering"
            ],
            "telecommunications": [
                "frequency assignment", "antenna site selection"
            ]
        },
        "real_world": {
            "manufacturing": [
                "automobile assembly line production planning", "steel plant furnace scheduling and raw material mixing",
                "garment factory cutting plan design", "semiconductor wafer fabrication scheduling"
            ],
            "logistics_transportation": [
                "courier company's delivery route planning", "container port unloading scheduling"
            ],
            "retail_commercial": [
                "chain supermarket site selection planning", "goods shelf display optimization"
            ],
            "energy_resources": [
                "power system generation scheduling", "oil extraction drilling layout"
            ],
            "public_services": [
                "hospital operating room scheduling", "fire station site selection planning"
            ],
            "telecommunications_network": [
                "base station antenna layout planning", "communication network routing design"
            ]
        }
    }

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(categories, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    generate_problem_categories()