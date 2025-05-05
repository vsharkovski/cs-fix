import sys
import time
from pathlib import Path

from csfix.application import Application

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def main() -> None:
    app = Application()

    # this variable holds test project files to be scanned
    test_files_dir = Path("tests/buggy-python")
    files = list(test_files_dir.glob("*.py"))
    num_files = len(files)
    if num_files == 0:
        print("No test files found in:", test_files_dir)
        return

    # Measure SPA Tool Runtime (static analysis runtime)
    print("Measuring SPA Tool Runtime by scanning directory...")
    scan_start = time.perf_counter()
    # Provide a list of tools to use
    app.scan(test_files_dir, ["ruff"])
    scan_end = time.perf_counter()
    spa_tool_runtime = scan_end - scan_start
    print(f"SPA Tool Runtime: {spa_tool_runtime:.2f} seconds")

    total_llm_time = 0.0
    total_e2e_time = 0.0
    print("\nMeasuring LLM Response Time and End-to-End Latency on each file:")
    for file in files:
        # End-to-End: from file selection to suggestions displayed.
        start_e2e = time.perf_counter()

        # Measure LLM response time
        start_llm = time.perf_counter()
        app.get_suggestions(file)
        llm_end = time.perf_counter()
        llm_response_time = llm_end - start_llm

        end_e2e = time.perf_counter()
        e2e_latency = end_e2e - start_e2e

        print(f"File: {file.name}")
        print(f"  LLM Response Time: {llm_response_time:.2f} seconds")
        print(f"  End-to-End Latency: {e2e_latency:.2f} seconds")
        total_llm_time += llm_response_time
        total_e2e_time += e2e_latency

    # Calculate throughput (number of files processed per minute)
    throughput = num_files / ((total_e2e_time / num_files) / 60)
    print(f"\nThroughput: {throughput:.2f} files per minute")


if __name__ == "__main__":
    main()
