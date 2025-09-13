# XDA-Tool Vulnerability Detection Guide

## Prerequisites
- Docker installed on your system
- Basic familiarity with command line operations

## Preparation
- Before starting, you need to place your smart contract bytecode files in the bytecode1 folder. We have already provided DApp data in the bytecode1 directory for your convenience.

## Step-by-Step Instructions

### 1. Build the Docker Image
Navigate to the directory containing your Dockerfile and execute:
```bash
docker build -t xda-tool .
```
This command builds a Docker image named "xda-tool" from the Dockerfile in the current directory.

### 2. Run the Docker Container
Start a container from the xda-tool image with:
```bash
docker run -it xda-tool /bin/bash
```
This will open an interactive bash shell inside the container.

### 3. Activate the Conda Environment
Within the container, activate the xda virtual environment:
```bash
conda activate xda
```

### 4. Execute Vulnerability Detection
Run the benchmark timing script to perform vulnerability analysis:

```bash
cd satellite
python3 benchmark_timing.py
```
This process will analyze vulnerabilities and save the results to `vulnerability_analysis_results.csv`.

### 5. Access Results
After completion, the results will be available in the `vulnerability_analysis_results.csv` file within the container. You may need to copy this file to your host system if you want to preserve it after the container exits.

## Notes
- The container environment is ephemeral by default. Any changes made inside the container will be lost when it exits unless you use Docker volumes or copy files to your host system.
- Ensure you have sufficient permissions to run Docker commands on your system.

For troubleshooting or additional configuration options, refer to the Docker documentation specific to your operating system.