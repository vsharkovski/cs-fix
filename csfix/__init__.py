import argparse
from pathlib import Path
from typing import Sequence

from csfix.application import Application
from csfix.tools.tool_details import TOOLS


def scan_subcommand(args: argparse.Namespace):
    scan_directory = Path(args.directory)
    tool_codes = args.tools

    application = Application()
    application.scan(scan_directory, tool_codes)

    if args.show:
        application.show_problems(scan_directory)


def show_subcommand(args: argparse.Namespace):
    directory = Path(args.directory)
    application = Application()
    application.show_problems(directory)


def suggest_subcommand(args: argparse.Namespace):
    file_path = Path(args.file)
    application = Application()
    application.get_suggestions(file_path)


def tools_subcommand(args: argparse.Namespace):
    print("Available tools:")
    for tool in TOOLS:
        print(f"* {tool.name} (code: {tool.code}): {tool.description}")


def main(args: Sequence[str] | None = None):
    parser = argparse.ArgumentParser(prog=__name__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    # scan subcommand
    scan_parser = subparsers.add_parser(
        "scan", help="Scan a directory with static analysis tools"
    )
    scan_parser.add_argument(
        "tools",
        nargs="+",
        help="List of tool codes to run. Use `csfix tools` for more information.",
    )
    scan_parser.add_argument("directory", help="Target directory to scan")
    scan_parser.add_argument(
        "--show", action="store_true", help="Show problems found after scanning"
    )
    scan_parser.set_defaults(func=scan_subcommand)

    # show subcommand
    show_parser = subparsers.add_parser(
        "show", help="Show problems for a scanned directory"
    )
    show_parser.add_argument("directory", help="Target directory")
    show_parser.set_defaults(func=show_subcommand)

    # suggest subcommand
    suggest_parser = subparsers.add_parser(
        "suggest", help="Suggest fixes for a given file"
    )
    suggest_parser.add_argument("file", help="Target file")
    suggest_parser.set_defaults(func=suggest_subcommand)

    # tools subcommand
    tools_parser = subparsers.add_parser("tools", help="Show tools information")
    tools_parser.set_defaults(func=tools_subcommand)

    options = parser.parse_args(args)
    options.func(options)


if __name__ == "__main__":
    main()
