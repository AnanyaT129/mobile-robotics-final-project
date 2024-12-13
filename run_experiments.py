# This file will run an experiment 
# - for all 10 datasets,
# - across all 3 methods of initialization
# given that initialized data is already provided
import os
import gtsam
import time
import matplotlib.pyplot as plt
from gtsam.utils.plot import plot_trajectory
import pandas as pd

def pathToFile(folder):
    return {
        "original": os.path.join(folder, "original_data.g2o"),
        "MASAT": os.path.join(folder, "MASAT_output.g2o"),
        "weighted_MASAT": os.path.join(folder, "MASAT_weighted_output.g2o")
    }

def plot(values, savePath, is3D):
    if (is3D):
        plot_3d_trajectory(values, savePath)
    else:
        plot_2d_trajectory(values, savePath)

# uses matplotlib to plot the trajectory of a 2D dataset
def plot_2d_trajectory(values, savePath, title="2D Trajectory", axis_labels=("X", "Y")):
    x_vals = []
    y_vals = []

    # Extract x, y from Pose2 values
    for key in values.keys():
        pose = values.atPose2(key)
        x_vals.append(pose.x())
        y_vals.append(pose.y())

    # Plot trajectory
    plt.figure()
    plt.plot(x_vals, y_vals, color='green',linestyle='dashed',linewidth=1,markersize=2, label="Trajectory")  # Line with markers
    plt.title(title)
    plt.xlabel(axis_labels[0])
    plt.ylabel(axis_labels[1])
    plt.legend()
    plt.grid(True)
    plt.axis("equal")  # Ensure equal aspect ratio
    plt.savefig(savePath)
    plt.close()

# uses matplotlib to plot the trajectory of a 3D dataset
def plot_3d_trajectory(values, savePath, title="3D Trajectory", axis_labels=("X", "Y", "Z")):
    plot_trajectory(0, values, title=title, axis_labels=axis_labels)
    plt.savefig(savePath)
    plt.close()

# Function to load the datasets in a given folder
# Runs SLAM optimization on each .g2o file within
# Saves metrics and plots of trajectory
def optimizeDataset(folder, is3D):
    files = pathToFile(folder)
    results = []

    # check that filepath exsits
    for algorithm, filePath in files.items():
        if not os.path.exists(filePath):
            print(f"File {filePath} not found.")
            continue
    
        # load factor graph
        graph, initial_guess = gtsam.readG2o(filePath, is3D)

        # plot inital guess
        plot(initial_guess, os.path.join(folder, f"{algorithm}_initial"), is3D)

        # initial error
        initial_error = graph.error(initial_guess)

        # run SLAM
        params = gtsam.LevenbergMarquardtParams()
        params.setVerbosityLM("SUMMARY")
        params.setVerbosity("TERMINATION") 
        optimizer = gtsam.LevenbergMarquardtOptimizer(graph, initial_guess, params)
        start_time = time.time()
        optimized_result = optimizer.optimize()
        end_time = time.time()

        # get metrics
        optimization_runtime = end_time - start_time
        iterations = optimizer.iterations()
        error = graph.error(optimized_result)

        # save results
        results.append({
            "Dataset": folder,
            "Algorithm": algorithm,
            "Initial Error": initial_error,
            "Optimization Runtime": optimization_runtime,
            "Optimizer Iterations": iterations,
            "Post Optimization Error": error
        })

         # plot optimized result
        plot(optimized_result, os.path.join(folder, f"{algorithm}_optimized"), is3D)

    return results


datasets = [
    # {"folder": "input_data/10kHog-man", "is3D": False},
    # {"folder": "input_data/city10k", "is3D": False},
    # {"folder": "input_data/FR079_P", "is3D": False},
    # {"folder": "input_data/FRH_P", "is3D": False},
    # {"folder": "input_data/grid3D", "is3D": True},
    {"folder": "input_data/input_M3500", "is3D": False},
    {"folder": "input_data/INTEL_P", "is3D": False},
    # {"folder": "input_data/parking-garage", "is3D": True},
    # {"folder": "input_data/sphere3D", "is3D": True},
    {"folder": "input_data/torus3D", "is3D": True},
]

results = []

# loop through all datasets and perform optimization
# optimization returns metrics, which are saved to the overall list
for d in datasets:
    folder = d["folder"]
    is3D = d["is3D"]
    print(f"Optimizing dataset {folder}")
    result = optimizeDataset(folder, is3D)
    results.extend(result)

# list gets saved as a csv file for easy analysis
results_dataframe = pd.DataFrame(results)
results_dataframe.to_csv("experiment_results_3d_2.csv", index=False)