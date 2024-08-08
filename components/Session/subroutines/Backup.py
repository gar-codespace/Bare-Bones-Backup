"""
The Backup subroutine.
"""

import Entities
from components.Session.Model_Base import Subroutine_Base as SB

SUBROUTINE_NAME = "Backup"
SCRIPT_NAME = f"B3.{__name__}"
SCRIPT_REV = 20240401


class Controller(SB):

    def run(self) -> None:

        start_time = Entities.TIME.time()

        self.boiler_plate()
        
        A = self.SOURCE_PATH
        B = self.TARGET_PATH

        self.STATUS = _("Backup Directories")
        self.align = True
        self.correlate_directories(A, B)
        self.SOURCE_NEW_DIRECTORY_COUNT += self.new
        self.EXCLUDED_DIRECTORY_COUNT += self.excluded
        self.MATCHED_DIRECTORY_COUNT += self.aligned
        self.align = False
        self.correlate_directories(B, A)
        self.TARGET_NEW_DIRECTORY_COUNT += self.new

        self.STATUS = _("Backup Files")
        self.align = True
        self.correlate_files(A, B)
        self.SOURCE_NEW_FILE_COUNT += self.new
        self.EXCLUDED_FILE_COUNT += self.excluded
        self.MATCHED_FILE_COUNT += self.matched
        self.SOURCE_NEWER_FILE_COUNT += self.newer
        self.align = False
        self.correlate_files(B, A)
        self.TARGET_NEW_FILE_COUNT += self.new
        self.TARGET_NEWER_FILE_COUNT += self.newer

        self.STATUS = _("Subroutine Completed")

        run_time = Entities.TIME.time() - start_time

        self.RESULTS = self.get_run_results()
        self.RESULTS["run_time"] = Entities.convert_time(run_time)
        self.RESULTS["run_date"] = Entities.get_date()
    
    def get_subroutine_results(self) -> dict:

        return self.RESULTS
    
    def get_subroutine_exceptions(self) -> list:

        return self.EXCEPTIONS
    
    def get_subroutine_verbose(self) -> list:

        return self.VERBOSE


class View:

    formatted = []

    def __init__(self) -> None:
        pass

    def formatted_results(self, results: dict) -> list:
        """
        Apply i18n and formatting to the result from Backup.
        """

        self.formatted.append(f"{_("Profile")}: {results["profile"]}")
        self.formatted.append(f"{_("Subroutine")}: {results["subroutine"]}")
        self.formatted.append(f"{_("Source Directory")}: {results["source_directory"]}")
        self.formatted.append(f"{_("Target Directory")}: {results["target_directory"]}")
        self.formatted.append(f"{_("Source Directory Count")}: {results["source_directory_count"]}")
        self.formatted.append(f"{_("Source File Count")}: {results["source_file_count"]}")
        self.formatted.append("")
        self.formatted.append(f"{_("Excluded Directory Count")}: {results["excluded_directory_count"]}")
        self.formatted.append(f"{_("Matched Directory Count")}: {results["matched_directory_count"]}")
        self.formatted.append(f"{_("Source New Directory Count")}: {results["new_source_directory_count"]}")
        self.formatted.append(f"{_("Target New Directory Count")}: {results["new_target_directory_count"]}")
        self.formatted.append(f"{_("Target Orphan Directory Count")}: {results["obsolete_target_directory_count"]}")
        self.formatted.append("")
        self.formatted.append(f"{_("Excluded File Count")}: {results["excluded_file_count"]}")
        self.formatted.append(f"{_("Matched File Count")}: {results["matched_file_count"]}")
        self.formatted.append("")
        self.formatted.append(f"{_("Source New File Count")}: {results["new_source_file_count"]}")
        self.formatted.append(f"{_("Source Newer File Count")}: {results["newer_source_file_count"]}")
        self.formatted.append(f"{_("Source Updated File Count")}: {results["updated_source_file_count"]}")
        self.formatted.append("")
        self.formatted.append(f"{_("Target New File Count")}: {results["new_target_file_count"]}")
        self.formatted.append(f"{_("Target Newer File Count")}: {results["newer_target_file_count"]}")
        self.formatted.append(f"{_("Target Updated File Count")}: {results["updated_target_file_count"]}")
        self.formatted.append(f"{_("Target Orphan File Count")}: {results["target_orphan_file_count"]}")
        self.formatted.append("")
        self.formatted.append(f"{_("Run Date")}: {results["run_date"]}")
        self.formatted.append(f"{_("Run Duration")}: {results["run_time"]}")

        return self.formatted

    def append_verbose(self, verbose:list) -> list:

        for item in verbose:
            self.formatted.append(item)

        return self.formatted
