import logging
import sys
from datetime import datetime
from pathlib import Path

from csfix.data.scan_status_repository import ScanStatusRepository
from csfix.exceptions import ToolNotFoundError
from csfix.model.scan_status import ScanStatus
from csfix.service.problem_service import ProblemService
from csfix.service.tool_service import ToolService
from csfix.tools.tool_details import ToolDetails
from csfix.util import glob_files_resolved

logger = logging.getLogger(__name__)


class ScanService:
    def __init__(
        self,
        tool_service: ToolService,
        problem_service: ProblemService,
        scan_status_repository: ScanStatusRepository,
    ):
        self._tool_service = tool_service
        self._problem_service = problem_service
        self._scan_status_repository = scan_status_repository

    def scan(self, directory: Path, tool_codes: list[str]) -> None:
        logger.info(f"Scanning directory {directory} with tools {tool_codes}")
        try:
            tools = [self._tool_service.get_tool_by_code(code) for code in tool_codes]
        except ToolNotFoundError as e:
            logger.error(e)
            sys.exit(1)

        files = glob_files_resolved(directory, "**/*.py")
        files_with_modified_times = [
            (file, self._get_modified_time(file)) for file in files
        ]

        for tool in tools:
            for file, modified_time in files_with_modified_times:
                if self._should_scan(file, modified_time, tool):
                    self._scan(file, tool)

    def _get_modified_time(self, file: Path) -> datetime:
        stat_result = file.stat()
        modified_time_seconds = stat_result.st_mtime
        return datetime.fromtimestamp(modified_time_seconds)

    def _should_scan(
        self, file: Path, modified_time: datetime, tool: ToolDetails
    ) -> bool:
        scan_status = self._scan_status_repository.get_by_file_and_tool_name(
            str(file), tool.name
        )
        if not scan_status:
            # This file has never been scanned in the past.
            return True

        if scan_status.scan_time < modified_time:
            # This file was scanned but later modified.
            return True

        # This file was scanned after it was last modified.
        return False

    def _scan(self, file: Path, tool: ToolDetails) -> None:
        # Run the tool on the file
        logger.info(f"Scanning with tool {tool.name} on file: {file}")
        scan_time = datetime.now()

        runner = tool.create_runner()
        problems = runner.run(file)

        # Delete old scan status and insert new one
        scan_status = ScanStatus(
            file=str(file),
            tool_name=tool.name,
            scan_time=scan_time,
            problem_count=len(problems),
        )
        self._scan_status_repository.delete_by_file_and_tool_name(
            scan_status.file, scan_status.tool_name
        )
        self._scan_status_repository.insert(scan_status)

        # Delete old problems and insert new ones
        self._problem_service.delete_problems_by_file_and_tool_before(
            file, tool, scan_time
        )
        self._problem_service.insert_problems(problems)
