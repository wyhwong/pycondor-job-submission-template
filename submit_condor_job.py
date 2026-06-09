import argparse
import subprocess
import logging

from pycondor import Dagman, Job

LOGGER = logging.getLogger(__name__)


def prepare_parser() -> argparse.ArgumentParser:
    """Prepare the argument parser for the script"""

    parser = argparse.ArgumentParser(
        description="Setting of the condor job submission workflow"
    )
    parser.add_argument(
        "--accounting-group",
        type=str,
        help="Accounting group to charge for the job.",
    )
    parser.add_argument(
        "-j",
        "--job",
        type=str,
        help="Path to the scripts",
        required=True,
    )
    parser.add_argument(
        "--n-cpus",
        type=str,
        default="1",
        help="Number of CPUs to request for the job.",
    )
    parser.add_argument(
        "--memory-in-gb",
        type=str,
        default="4",
        help="Amount of memory in GB to request for the job.",
    )
    parser.add_argument(
        "--disk-in-gb",
        type=str,
        default="50",
        help="Amount of disk space in GB to request for the job.",
    )
    LOGGER.info("Argument parser prepared successfully: %s", parser.format_help())
    return parser.parse_args()


def get_default_condor_paths():
    """Get the default paths for condor job submission"""

    # Output directory for condor, will be created automatically if not exist
    return {
        "error": "condor/run.err",
        "output": "condor/run.out",
        "log": "condor/run.log",
        "submit": "condor/run.sub",
    }


def get_python_executable():
    """Get the python executable path currently used"""

    python_executable = (
        subprocess.check_output(["which", "python"]).decode("utf-8").strip()
    )
    LOGGER.info("Python executable found at: %s", python_executable)
    return python_executable


def main():
    """Main function to run the workflow"""

    args = prepare_parser()
    condor_paths = get_default_condor_paths()
    python_executable = get_python_executable()

    # Here add the extra lines to request memory and disk
    extra_lines = [
        f"accounting_group = {args.accounting_group}",
        "notification = error",
        f"request_cpus = {args.n_cpus}",
        f"request_memory = {args.memory_in_gb}GB",
        f"request_disk = {args.disk_in_gb}GB",
        f"transfer_input_files = jobs,data,{python_executable}",
        f"transfer_output_files = data",
        "should_transfer_files = YES",
        "when_to_transfer_output = ON_EXIT_OR_EVICT",
        "transfer_executable = TRUE",
        "queue",
    ]

    # Instantiate a Dagman
    dagman = Dagman(name="dagman", submit=condor_paths["submit"])

    # Instantiate Jobs
    child_job = Job(
        name="job",
        executable=python_executable,
        submit=condor_paths["submit"],
        error=condor_paths["error"],
        output=condor_paths["output"],
        getenv=False,
        log=condor_paths["log"],
        extra_lines=extra_lines,
        dag=dagman,
    )
    child_job.add_arg(args.job, retry=3)
    dagman.add_job(child_job)
    dagman.build_submit()


main()
