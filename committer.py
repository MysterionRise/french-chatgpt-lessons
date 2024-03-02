import subprocess
import random
from datetime import datetime, timedelta
import os


def run_git_command(command):
    """Run a git command in the shell and return its output."""
    result = subprocess.run(command, shell=True, text=True,
                            capture_output=True)
    return result.stdout.strip()


def list_files(directory):
    """Recursively list all files in the directory."""
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files


def get_uncommitted_files():
    """Get a list of uncommitted files in the git repository."""
    tracked_files = run_git_command("git ls-files")
    all_files = list_files(".")
    uncommitted_files = [f for f in all_files if
                         f not in tracked_files and not os.path.isdir(f)]
    return uncommitted_files


def commit_files(start_date):
    """Commit files with a unique message on sequential dates with random times."""
    files = get_uncommitted_files()
    date = datetime.strptime(start_date, "%Y-%m-%d")

    for file in files:
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        timestamp = date.replace(hour=hour, minute=minute,
                                 second=second).isoformat()

        run_git_command(f"git add '{file}'")
        run_git_command(
            f"git commit -m 'feat: adding file {file}' --date='{timestamp}'")

        date += timedelta(days=3)  # Increment the date for the next file


if __name__ == "__main__":
    import sys

    start_date = sys.argv[1]  # Expecting date in YYYY-MM-DD format
    commit_files(start_date)
