from eval_src.costs import B1HomogeneityCost as B1HomogeneityCostEval
from eval_src.costs import B1HomogeneitySARCost as B1HomogeneitySARCostEval
from eval_src.utils import evaluate_coil_config as evaluate_coil_config_eval

import argparse
import json
import pathlib

import sys
sys.path.insert(0, './code')

from main import run
from src.data import Simulation

def parse_args():
    parser = argparse.ArgumentParser(description="Run coil configuration evaluation.")
    parser.add_argument("-f", "--simulation_file", required=True, help="Name of the simulation file.")
    parser.add_argument("-c", "--cost_function", required=True, choices=["B1HomogeneityCost", "B1HomogeneitySARCost"], help="Cost function to use.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    # Load simulation data
    base_path = pathlib.Path("test_data/simulations")
    simulation_path = base_path / args.simulation_file
    antenna_path = pathlib.Path("test_data/antenna/antenna.h5")
    if not simulation_path.exists():
        raise FileNotFoundError(f"Simulation file not found: {simulation_path}")
    if not simulation_path.is_file():
        raise ValueError(f"Expected a file, but got a directory: {simulation_path}")
    if not simulation_path.suffix == ".h5":
        raise ValueError(f"Expected a .h5 file, but got: {simulation_path.suffix}")
    simulation = Simulation(simulation_path, coil_path=antenna_path)
    
    # Define cost function
    if args.cost_function == "B1HomogeneityCost":
        cost_function = B1HomogeneityCostEval()
    elif args.cost_function == "B1HomogeneitySARCost":
        cost_function = B1HomogeneitySARCostEval()
    else:
        raise ValueError(f"Unsupported cost function: {args.cost_function}")
    
    # Run optimization
    best_coil_config = run(simulation=simulation, cost_function=cost_function)
    
    # Evaluate best coil configuration
    result = evaluate_coil_config_eval(best_coil_config, simulation, cost_function)

    # Save results to JSON file
    output_file = "best_coil_config.json"
    with open(output_file, "w") as f:
        json.dump(result, f, indent=4)
