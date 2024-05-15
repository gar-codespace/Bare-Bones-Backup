"""
The Compare Subroutine
"""

import Entities
from components.Session import Model_Entities

SUBROUTINE_NAME = "Compare"
SCRIPT_NAME = f"B3.{__name__}"
SCRIPT_REV = 20240401


class Model:

    def __init__(self) -> None:

        self.current_profile = Model_Entities.get_profile()
        self.implement_excludes = self.current_profile["implement_excludes"]

        exd = self.current_profile["exclude_directories"]
        self.regex_directories = Model_Entities.compile_exclude_directories(exd)

        exf = self.current_profile["exclude_files"]
        self.regex_files = Model_Entities.compile_exclude_files(exf)

        self.new: int
        self.excluded: int
        self.aligned: int
        self.different: int
        self.obsolete: int
        self.target_newer: int

        self.exceptions = []

    def backup_directories(self, A, B) -> None:

        self.new = 0
        self.excluded = 0
        self.aligned = 0

        for root, directories, files in Entities.OS.walk(A):
            for directory in directories:
                a_path = Entities.OS_PATH.join(root, directory)

                if self.implement_excludes:
                    x = a_path.split("\\")
                    if [hit for hit in x if self.regex_directories.match(hit)]:
                        self.excluded += 1
                        continue

                rel_path = Entities.OS_PATH.relpath(a_path, A)
                b_path = Entities.OS_PATH.join(B, rel_path)

                if Entities.OS_PATH.isdir(b_path):
                    self.aligned += 1
                else:
                    success = Entities.generic_make_directory(b_path)
                    if success:
                        self.new += 1
                    else:
                        x_rel = Entities.OS_PATH.relpath(b_path, B)
                        self.exceptions.append(f"Not created: {x_rel}")

    def backup_files(self, A, B) -> None:

        self.new = 0
        self.excluded = 0
        self.matched = 0
        self.different = 0
        self.target_newer = 0

        for root, directories, files in Entities.OS.walk(A):
            for file in files:

                a_file_path = Entities.OS_PATH.join(root, file)

                if self.implement_excludes:
                    x = a_file_path.split("\\")
                    exd = [hit for hit in x if self.regex_directories.match(hit)]
                    exf = self.regex_files.match(file)
                    if exd or exf:
                        self.excluded += 1
                        continue

                rel_path = Entities.OS_PATH.relpath(root, A)
                b_file_path = Entities.OS_PATH.join(B, rel_path, file)

                if Entities.OS_PATH.isfile(b_file_path):
                    a_date = Entities.OS_PATH.getmtime(a_file_path)
                    b_date = Entities.OS_PATH.getmtime(b_file_path)

                    if a_date > b_date:
                        success = Entities.generic_copy_file(a_file_path, b_file_path)
                        if success:
                            self.different += 1
                        else:
                            x_rel = Entities.OS_PATH.relpath(a_file_path, A)
                            self.exceptions.append(f"Source not copied: {x_rel}")

                    if a_date < b_date:
                        x_rel = Entities.OS_PATH.relpath(b_file_path, B)
                        self.exceptions.append(
                            f"Newer in target: {x_rel}"
                        )
                        self.target_newer += 1

                    if a_date == b_date:
                        self.matched += 1
                else:
                    success = Entities.generic_copy_file(a_file_path, b_file_path)
                    if success:
                        self.new += 1
                    else:
                        x_rel = Entities.OS_PATH.relpath(a_file_path, A)
                        self.exceptions.append(f"Not copied: {x_rel}")

    def remove_obsolete_files(self, A, B):
        """
        A is source.
        B is target.
        Remove files that are in B if they're not in A.
        Remove files in B that are in the regex.
        """

        if self.current_profile["mirror"] == False:
            return

        self.obsolete = 0

        for root, directories, files in Entities.OS.walk(B):
            for file in files:

                b_file_path = Entities.OS_PATH.join(root, file)
                rel_path = Entities.OS_PATH.relpath(root, B)
                a_file_path = Entities.OS_PATH.join(A, rel_path, file)

                if not Entities.OS_PATH.isfile(a_file_path):
                    success = Entities.generic_file_remove(b_file_path)
                    if success:
                        self.obsolete += 1
                    else:
                        x_rel = Entities.OS_PATH.relpath(b_file_path, B)
                        self.exceptions.append(f"Not removed: {x_rel}")
                if self.implement_excludes:
                    x = b_file_path.split("\\")
                    exd = [hit for hit in x if self.regex_directories.match(hit)]
                    exf = self.regex_files.match(file)
                    if exd or exf:
                        success = Entities.generic_file_remove(b_file_path)
                        if success:
                            self.obsolete += 1
                        else:
                            x_rel = Entities.OS_PATH.relpath(b_file_path, B)
                            self.exceptions.append(f"Not removed: {x_rel}")

    def remove_obsolete_directories(self, A, B):
        """
        A is source.
        B is target.
        Remove directories that are in B if they're not in A.
        Remove directories in B that are in the regex.
        Because only empty directories are removed, walk from bottom up.
        """

        if self.current_profile["mirror"] == False:
            return

        self.obsolete = 0
        for root, directories, files in Entities.OS.walk(B, topdown=False):
            for directory in directories:

                b_path = Entities.OS_PATH.join(root, directory)
                rel_path = Entities.OS_PATH.relpath(b_path, B)
                a_path = Entities.OS_PATH.join(A, rel_path)

                if self.implement_excludes:
                    x = b_path.split("\\")
                    if [hit for hit in x if self.regex_directories.match(hit)]:
                        success = Entities.generic_directory_remove(b_path)
                        if success:
                            self.obsolete += 1
                        else:
                            x_rel = Entities.OS_PATH.relpath(b_path, B)
                            self.exceptions.append(f"Not removed: {x_rel}")

                if not Entities.OS_PATH.isdir(a_path):
                    success = Entities.generic_directory_remove(b_path)
                    if success:
                        self.obsolete += 1
                    else:
                        x_rel = Entities.OS_PATH.relpath(b_path, B)
                        self.exceptions.append(f"Not removed: {x_rel}")

    def subroutine_complete(self) -> None:

        self.subroutine_status = f"Subroutine Complete"

    def get_new(self) -> int:

        return self.new

    def get_excluded(self) -> int:

        return self.excluded

    def get_aligned(self) -> int:

        return self.aligned

    def get_different(self) -> int:

        return self.different

    def get_obsolete(self) -> int:

        return self.obsolete

    def get_target_newer(self) -> int:

        return self.target_newer
    
    def get_exceptions(self) -> list:

        return self.exceptions


class Compare:
    """
    Compare two directories for differences.
    Works in both directions.
    Report differences.
    Take no action.
    """

    def __init__(self) -> None:

        self.current_profile = Model_Entities.get_profile()
        self.implement_excludes = self.current_profile["implement_excludes"]

        exd = self.current_profile["exclude_directories"]
        self.regex_directories = Model_Entities.compile_exclude_directories(exd)

        exf = self.current_profile["exclude_files"]
        self.regex_files = Model_Entities.compile_exclude_files(exf)

        self.new: int
        self.excluded: int
        self.aligned: int
        self.different: int

    def compare_directories(self, A, B) -> None:

        self.new = 0
        self.excluded = 0
        self.aligned = 0

        for root, directories, files in Entities.OS.walk(A):
            for directory in directories:

                a_path = Entities.OS_PATH.join(root, directory)

                if self.implement_excludes:
                    x = a_path.split("\\")
                    if [hit for hit in x if self.regex_directories.match(hit)]:
                        self.excluded += 1
                        continue

                rel_path = Entities.OS_PATH.relpath(a_path, A)
                b_path = Entities.OS_PATH.join(B, rel_path)
                if Entities.OS_PATH.isdir(b_path):
                    self.aligned += 1
                else:
                    self.new += 1

    def compare_files(self, A, B) -> None:

        self.new = 0
        self.excluded = 0
        self.matched = 0
        self.different = 0

        for root, directories, files in Entities.OS.walk(A):
            for file in files:

                a_file_path = Entities.OS_PATH.join(root, file)

                if self.implement_excludes:
                    x = a_file_path.split("\\")
                    exd = [hit for hit in x if self.regex_directories.match(hit)]
                    exf = self.regex_files.match(file)
                    if exd or exf:
                        self.excluded += 1
                        continue

                rel_path = Entities.OS_PATH.relpath(a_file_path, A)
                b_file_path = Entities.OS_PATH.join(B, rel_path)

                if Entities.OS_PATH.isfile(b_file_path):
                    a_date = Entities.OS_PATH.getmtime(a_file_path)
                    b_date = Entities.OS_PATH.getmtime(b_file_path)

                    if a_date > b_date:
                        self.different += 1

                    if a_date == b_date:
                        self.matched += 1

                else:
                    self.new += 1

    def subroutine_complete(self) -> None:

        self.subroutine_status = f"Subroutine Complete"

    def get_new(self) -> int:

        return self.new

    def get_excluded(self) -> int:

        return self.excluded

    def get_aligned(self) -> int:

        return self.aligned

    def get_different(self) -> int:

        return self.different

    def get_status(self) -> int:

        return self.subroutine_status

class View:

    def __init__(self) -> None:
        pass

    def formatted_results(results: dict) -> str:
        """
        Apply i18n and formatting to the result from Backup.
        """

        report =  f"{_("Results")}:\n"
        report += f"{_("Profile")}: {results["profile"]}\n"
        report += f"{_("Subroutine")}: {results["subroutine"]}\n"
        report += f"{_("Source Directory")}: {results["source_directory"]}\n"
        report += f"{_("Target Directory")}: {results["target_directory"]}\n"
        report += f"{_("Source Directory Count")}: {results["source_directory_count"]}\n"
        report += f"{_("Source File Count")}: {results["source_file_count"]}\n"
        report += "\n"
        report += f"{_("Excluded Directory Count")}: {results["excluded_directory_count"]}\n"
        report += f"{_("Matched Directory Count")}: {results["matched_directory_count"]}\n"
        report += f"{_("Source New Directory Count")}: {results["new_source_directory_count"]}\n"
        report += f"{_("Target New Directory Count")}: {results["new_target_directory_count"]}\n"
        report += f"{_("Target Obsolete Directory Count")}: {results["obsolete_target_directory_count"]}\n"
        report += "\n"
        report += f"{_("Excluded File Count")}: {results["excluded_file_count"]}\n"
        report += f"{_("Matched File Count")}: {results["matched_file_count"]}\n"
        report += "\n"
        report += f"{_("Source New File Count")}: {results["new_source_file_count"]}\n"
        report += f"{_("Source Newer File Count")}: {results["newer_source_file_count"]}\n"
        report += f"{_("Source Updated File Count")}: {results["updated_source_file_count"]}\n"
        report += "\n"
        report += f"{_("Target New File Count")}: {results["new_target_file_count"]}\n"
        report += f"{_("Target Newer File Count")}: {results["newer_target_file_count"]}\n"
        report += f"{_("Target Updated File Count")}: {results["updated_target_file_count"]}\n"
        report += f"{_("Target Orphan File Count")}: {results["target_orphan_file_count"]}\n"
        report += "\n"
        report += f"{_("Exception Count")}: {len(self.exceptions)}\n"
        report += f"{_("Run Date")}: {results["run_date"]}\n"
        report += f"{_("Run Duration")}: {results["run_time"]}\n"

        return report
