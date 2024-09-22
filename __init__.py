import os
import subprocess


def run_all_python_files(directory, current_file):
    executed_files = set()
    for filename in os.listdir(directory):
        if filename.endswith(".py") and filename != os.path.basename(current_file):
            if filename not in executed_files:
                filepath = os.path.join(directory, filename)
                subprocess.run(["python", filepath], check=True)
                executed_files.add(filename)


if __name__ == "__main__":
    current_file = os.path.abspath(__file__)
    directory = os.path.dirname(current_file)
    run_all_python_files(directory, current_file)


subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
