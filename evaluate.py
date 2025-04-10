from eval_src.costs import B1HomogeneityCost, B1HomogeneitySARCost
from eval_src.utils import evaluate_coil_config
from eval_src.data import Simulation, CoilConfig


import argparse
import json
import pathlib


def parse_args():
    parser = argparse.ArgumentParser(description="Run coil configuration evaluation.")
    parser.add_argument("-f", "--simulation_file", required=True, help="Name of the simulation file.")
    parser.add_argument("-c", "--cost_function", required=True, choices=["B1HomogeneityCost", "B1HomogeneitySARCost"], help="Cost function to use.")
    parser.add_argument("-g", "--group_name", default="default", help="Group name for the hackathon submission.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    # Load cost functions from cost_list.txt
    cost_list_file = pathlib.Path("cost_list.txt")
    if not cost_list_file.exists():
        raise FileNotFoundError(f"Cost list file not found: {cost_list_file}")
    
    with open(cost_list_file, "r") as f:
        available_cost_functions = [line.strip() for line in f if line.strip()]
    
    if args.cost_function not in available_cost_functions:
        raise ValueError(f"Unsupported cost function: {args.cost_function}. Available options are: {available_cost_functions}")

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
        cost_function = B1HomogeneityCost()
    elif args.cost_function == "B1HomogeneitySARCost":
        cost_function = B1HomogeneitySARCost()
    else:
        raise ValueError(f"Unsupported cost function: {args.cost_function}")
    
    # Read best coil config from json
    best_coil_config_json_path = "best_coil_config.json"
    if not pathlib.Path(best_coil_config_json_path).exists():
        raise FileNotFoundError(f"Best coil configuration file not found: {best_coil_config_json_path}")
    
    with open(best_coil_config_json_path, "r") as f:
        best_coil_config_data = json.load(f)
    
    best_coil_config = CoilConfig(
        phase=best_coil_config_data["best_coil_phase"],
        amplitude=best_coil_config_data["best_coil_amplitude"]
    )

    # Evaluate best coil configuration
    result = evaluate_coil_config(best_coil_config, simulation, cost_function)

    # Save results to JSON file
    simulation_name = args.simulation_file.split(".")[0]
    output_file_name = f"results_{simulation_name}.json"
    output_file = pathlib.Path("results") / args.group_name / args.cost_function /output_file_name
    
    if not output_file.parent.exists():
        output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w") as f:
        json.dump(result, f, indent=4)
