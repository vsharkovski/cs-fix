import os
import sqlite3
import subprocess
import sys
import time

# Directory to scan
# This variable can change depending on the directory you want to scan.
TARGET_DIR = "tests"


# this function is used to run the CS-Fix scan command
# and save the output to a file.
def run_csfix_scan(output_file):
    """Run CS-Fix scan and save output to a file."""
    with open(output_file, "w") as f:
        subprocess.run(
            ["pipenv", "run", "python", "-m", "csfix", "scan", "ruff", TARGET_DIR],
            stdout=f,
            stderr=subprocess.STDOUT,
            check=True,
        )


# this function is used to run the CS-Fix show command
# and display the files with errors.
def show_errors():
    """Run the show command to display files with errors."""
    subprocess.run(
        ["pipenv", "run", "python", "-m", "csfix", "show", TARGET_DIR],
        check=True,
    )


# this function is used to query the SQLite database
# and print the number of problems per file.
def print_problems_count():
    """Query the SQLite database and print the number of problems per file (for files with issues)."""
    db_path = os.path.join(".", ".csfix_data", "data.sqlite")
    if not os.path.exists(db_path):
        print("Database not found at", db_path)
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Only include files with one or more issues.
    cursor.execute(
        "SELECT file, COUNT(*) FROM problems GROUP BY file HAVING COUNT(*) > 0;"
    )
    results = cursor.fetchall()
    if results:
        print("\nProblems per file:")
        for file_path, count in results:
            print(f"{file_path}: {count} issues")
    else:
        print("\nNo problems stored in the database.")
    conn.close()


# this function is used to apply fixes automatically
# to all files with recorded problems.
# It queries the database for distinct file paths
# and then runs the CS-Fix fix command on each file.
def auto_apply_fixes():
    """
    Automatically apply fixes to all files with recorded problems.
    This function queries the database for distinct file paths
    and then runs the CS-Fix fix command on each file.
    """
    db_path = os.path.join(".", ".csfix_data", "data.sqlite")
    if not os.path.exists(db_path):
        print("Database not found at", db_path)
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT file FROM problems;")
    files = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not files:
        print("No files with problems found to fix.")
        return

    for file_path in files:
        print(f"\nApplying fixes automatically for: {file_path}")
        try:
            subprocess.run(
                ["pipenv", "run", "python", "-m", "csfix", "fix", file_path],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to apply fix for {file_path}. Skipping. Error: {e}")


def main():
    # Clean previous scan data.
    if os.path.exists(".csfix_data"):
        subprocess.run(["rm", "-rf", ".csfix_data"])

    print("Running initial scan...")
    start_scan = time.time()
    run_csfix_scan("before.txt")
    end_scan = time.time()
    print(f"SPA Tool Runtime: {end_scan - start_scan:.2f} seconds")

    print("\nRunning show command to display only files with errors...")
    show_errors()
    print_problems_count()

    print("\nApplying LLM fixes automatically...")
    auto_apply_fixes()

    print("Running scan after fixes...")
    run_csfix_scan("after.txt")
    print("\nRunning show command after fixes...")
    show_errors()
    print_problems_count()

    print("\nCalculating effectiveness metrics...")
    subprocess.run(
        [
            sys.executable,
            "test_scripts/calculate_metrics.py",
            "before.txt",
            "after.txt",
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
