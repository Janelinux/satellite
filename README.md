# Satellite

## Prerequisites
- Docker installed on your system
- Basic familiarity with command line operations

## Dataset
- Before starting, you need to place your smart contract bytecode files in the bytecode1 folder. We have already provided DApp data in the bytecode1 directory for your convenience.
- In the dataset folder,there are the dataset we provide
- Manually-labeled real-attack SMV dataset: We exhaustively search for SMV attack reports from the public,construct a manually-labeled attack dataset with a groundtruth of 58 SMV instances.
- Library-misuse dataset: This dataset consists of 56 contracts containing SMVs which are extracted  from SOTA studies and open-source platforms (e.g., GitHub).  
- Large-scale contract dataset: This dataset is composed of 10,011 wild contracts which is randomly sampled from the current largest available open-source contract dataset.
- The dataset commit hash is bdf7e0c54ca36c702ad5953e358f245487e0806a. However, please note that the hash changes with each commit.
## Step-by-Step Instructions

### 1. Build the Docker Image
Navigate to the directory containing your Dockerfile and execute:
```bash
docker build -t satellite .
```
This command builds a Docker image named "xda-tool" from the Dockerfile in the current directory.

### 2. Run the Docker Container
Start a container from the xda-tool image with:
```bash
docker run -it satellite /bin/bash
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
- The dependency.txt file contains all the dependency information.
- The commit hash is 0ab778bdf1b46d37416ad1d7af289df80c02b56b. However, please note that the hash changes with each commit. The provided hash value specifically represents the commit hash for the significant code submission.
- The container environment is ephemeral by default. Any changes made inside the container will be lost when it exits unless you use Docker volumes or copy files to your host system.
- Ensure you have sufficient permissions to run Docker commands on your system.

For troubleshooting or additional configuration options, refer to the Docker documentation specific to your operating system.