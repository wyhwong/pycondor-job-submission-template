## Condor Job Submission Template for Python Scripts

This repository contains a template for submitting Python scripts as Condor jobs,
which is used as an example for submitting jobs to LIGO's computing resources after the 2025's upgrade that disable the access of local filesystems from the compute nodes.

You can use the `submit_condor_job.py` script in this repository as a template for submitting your Python scripts as Condor jobs.
Below are the instructions on how to use the script.

```bash
# Activate your conda environment
conda activate <your conda env>

# Install the required dependencies if you use poetry
poetry install
# OR if you use pip
pip install pycondor

# Submit your Python script as a Condor job
python submit_condor_job.py \
    --job <path to your python script> \
    --accounting-group <accounting group to charge for the job> \
    --n-cpus <number of CPUs to request for the job> \
    --memory-in-gb <amount of memory in GB to request for the job> \
    --disk-in-gb <amount of disk space in GB to request for the job>
```

## Example

As a starting point, you may try with the hello_world.py script in this repository.

```bash
conda activate <your conda env>
pip install pycondor
python submit_condor_job.py \
    --job jobs/hello_world.py \
    --accounting-group <accounting group to charge for the job> 
```

Then you can check the status of your job with the following command:

```bash
condor_q
```

After the job is completed, you can check the output files in the `data` directory. The directory should contain:
- hello_world.txt
- requirements.txt

## Other Notes

If there are some jobs that are on hold, you can release them with the following command:

```bash
condor_release <job_id>
```

If you would like to remove a job from the queue, you can use the following command:

```bash
condor_rm <job_id>
```
