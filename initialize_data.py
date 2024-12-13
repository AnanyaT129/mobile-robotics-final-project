# this python script runs the 2 initializing algorithms for all 10 datasets

import os
import subprocess

def initialize_data(exePath, inputPath, outputPath):
    command = [exePath, inputPath, outputPath]
    try:
        result = subprocess.run(
            command,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text = True,
            check = False
        )

        stdOut = result.stdout.splitlines()
        for i in range(len(stdOut)):
            if "Runtime" in stdOut[i]:
                return stdOut[i]
            
        return "RUntime not found"

    except FileNotFoundError:
        print(f"File {exePath} not found")

folders = [
    "input_data/10kHog-man",
    "input_data/city10k",
    "input_data/FR079_P",
    "input_data/FRH_P",
    "input_data/grid3D",
    "input_data/input_M3500",
    "input_data/INTEL_P",
    "input_data/parking-garage",
    "input_data/sphere3D",
    "input_data/torus3D",
]

runtimes = []

for f in folders:
    inputFile = os.path.join(f, "original_data.g2o")
    masatOutputFile = os.path.join(f, "MASAT_output.g2o")
    weightedOutputFile = os.path.join(f, "MASAT_weighted_output.g2o")

    runtime_masat = initialize_data("./MASAT", inputFile, masatOutputFile)
    runtime_masat_weighted = initialize_data("./MASAT_weighted", inputFile, weightedOutputFile)

    runtimes.append(f"{f} - MASAT: {runtime_masat}")
    runtimes.append(f"{f} - MASAT_weighted: {runtime_masat_weighted}")

with open("initialize_runtimes.txt", "w") as f:
    f.write("\n".join(runtimes))