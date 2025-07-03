import argparse
import os
import json
from datetime import datetime
from simulation_engine.simulation_generator import SimulationGenerator



def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description="Run FMU simulations with control.")
    parser.add_argument("--scenario", required=True, help="Name of the scenario.")
    parser.add_argument("--n", type=int, required=True, help="Number of simulations to run.")
    parser.add_argument("--duration", type=float, required=True, help="Simulation duration.")
    parser.add_argument("--step_size", type=float, required=True, help="Simulation step size.")
    parser.add_argument("--controller", required=True, choices=["pid", "onoff", "fuzzy"], help="Controller type.")
    parser.add_argument("--plot", action="store_true", help="Plot the results.")

    args = parser.parse_args()

    for i in range(args.n):
        print(f"Running simulation {i+1}/{args.n}...")

        # Prepare result folder
        sim_folder = os.path.join("simulation_results", args.scenario, args.controller, f"sim_{i+1}")
        ensure_dir(sim_folder)

        simulation = SimulationGenerator(
            scenario_name=args.scenario,
            duration=args.duration,
            step_size=args.step_size,
            controller_type=args.controller,
            simulation_id=i,
            seed = i
        )

        times, plot_data, simulation_results = simulation.run_simulation(['temperatureSensor.T'])
        simulation.save_results_to_csv(times, simulation_results, sim_folder)
        
        if args.plot : simulation.plot_results(times, plot_data)
        
        # Save metadata
        metadata = {
            "scenario": args.scenario,
            "simulation_id": i + 1,
            "controller": args.controller,
            "duration": args.duration,
            "step_size": args.step_size,
            "timestamp": datetime.now().isoformat()
        }
        with open(os.path.join(sim_folder, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)

        print(f"Simulation {i+1} complete. Results saved to {sim_folder}")

if __name__ == "__main__":
    main()
