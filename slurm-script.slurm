#!/bin/sh
#SBATCH --account=ie-idi
#SBATCH --job-name=trajectory-similarity-10000
#SBATCH --time=1-00:00:00

#SBATCH --partition=CPUQ
#SBATCH --mem=128G
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --output=output-10000.txt
#SBATCH --error=output-10000.err

#SBATCH --mail-user=amalieur@stud.ntnu.no
#SBATCH --mail-type=ALL

WORKDIR=${SLURM_SUBMIT_DIR}
cd ${WORKDIR}
echo "Running from this directory: $SLURM_SUBMIT_DIR"
echo "Name of job: $SLURM_JOB_NAME"
echo "ID of job: $SLURM_JOB_ID"
echo "The job was run on these nodes: $SLURM_JOB_NODELIST"

module purge

# Running your python file
module load Anaconda3/2023.09-0

#activate our environment
conda activate masteroppgave

git checkout subset-10000
git pull origin subset-10000

python code/taxi-similarity.py
