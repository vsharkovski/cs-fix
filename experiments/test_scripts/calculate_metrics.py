import sys


def parse_issues(filename):
    issues = set()
    with open(filename) as f:
        for line in f:
            # Modify this filter as needed to match the output from csfix
            if "Scanning with tool" in line:
                issues.add(line.strip())
    return issues


if len(sys.argv) < 2:
    print("Usage: python calculate_metrics.py issues.txt [issues2.txt ...]")
    sys.exit(1)

for filename in sys.argv[1:]:
    issues = parse_issues(filename)
    print(f"Total Issues in {filename}: {len(issues)}")
