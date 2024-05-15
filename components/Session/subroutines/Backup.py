"""
The Backup subroutine.
"""

import Entities
from components.Session import Model_Entities

SUBROUTINE_NAME = "Backup"
SCRIPT_NAME = f"B3.{__name__}"
SCRIPT_REV = 20240401


class Model:

    def __init__(self) -> None:

        self.current_profile = Model_Entities.get_profile()
        self.subroutine_name = Model_Entities.get_subroutine_name()

        self.SOURCE_PATH = self.current_profile["source"]

        target = self.current_profile["target"]
        root = Entities.OS_PATH.basename(Entities.OS_PATH.normpath(self.SOURCE_PATH))
        self.TARGET_PATH = Entities.OS_PATH.join(target, root)

        self.mirror = self.current_profile["mirror"]
        self.implement_excludes = self.current_profile["implement_excludes"]
        exd = self.current_profile["exclude_directories"]
        self.regex_directories = Model_Entities.compile_exclude_directories(exd)
        exf = self.current_profile["exclude_files"]
        self.regex_files = Model_Entities.compile_exclude_files(exf)

        self.STATUS: str
        # These are returned to the GUI results frame.
        self.PROFILE = self.current_profile
        self.SUBROUTINE = self.subroutine_name
        self.SOURCE_DIRECTORY_COUNT: int = 0
        self.SOURCE_FILE_COUNT: int = 0

        self.SOURCE_NEW_DIRECTORY_COUNT: int = 0
        self.TARGET_NEW_DIRECTORY_COUNT: int = 0
        self.TARGET_OBSOLETE_DIRECTORY_COUNT: int = 0
        self.MATCHED_DIRECTORY_COUNT: int = 0
        self.EXCLUDED_DIRECTORY_COUNT: int = 0

        self.SOURCE_NEW_FILE_COUNT: int = 0
        self.SOURCE_NEWER_FILE_COUNT: int = 0
        self.SOURCE_UPDATED_FILE_COUNT: int = 0

        self.TARGET_NEW_FILE_COUNT: int = 0
        self.TARGET_NEWER_FILE_COUNT: int = 0
        self.TARGET_UPDATED_FILE_COUNT: int = 0
        self.TARGET_ORPHAN_FILE_COUNT: int = 0

        self.MATCHED_FILE_COUNT: int = 0
        self.EXCLUDED_FILE_COUNT: int = 0

        self.RUN_DATE: str
        self.RUN_TIME: str

        self.RESULTS = {}
        self.EXCEPTIONS = []

    def run(self) -> None:
        """
        Mini controller.
        """

        start_time = Entities.TIME.time()

        self.STATUS = f"Validate Directories"
        Model_Entities.validate_directories()

        self.STATUS = f"Poll Source"
        self.poll_source()

        self.STATUS = f"Add Target Root"
        self.add_target_root()

        self.align_items()

        run_time = Entities.TIME.time() - start_time

        self.RESULTS = self.get_run_results()
        self.RESULTS["run_time"] = Entities.convert_time(run_time)
        self.RESULTS["run_date"] = Entities.get_date()

    def poll_source(self) -> None:
        """
        Counts the number of source directories and files.
        """

        A, B = Entities.generic_tally_items(self.SOURCE_PATH)

        self.SOURCE_DIRECTORY_COUNT = A
        self.SOURCE_FILE_COUNT = B

    def add_target_root(self) -> None:
        """
        The base of the source is the root of the target.
        """

        if self.subroutine_name == "Compare":
            return

        result = Entities.generic_make_directory(self.TARGET_PATH)
        if result:
            self.TARGET_NEW_DIRECTORY_COUNT += 1
        else:
            # TODO add error here
            pass

    def align_items(self) -> None:
        """
        Run the selected subroutine.
        Aligns the directories and files in the source and target.
        """

        A = self.SOURCE_PATH
        B = self.TARGET_PATH

        self.STATUS = f"Backup Directories"
        self.backup_directories(A, B)

        self.TARGET_NEW_DIRECTORY_COUNT += self.get_new()
        self.EXCLUDED_DIRECTORY_COUNT += self.get_excluded()
        self.MATCHED_DIRECTORY_COUNT += self.get_aligned()

        self.STATUS = f"Backup Files"
        self.backup_files(A, B)
        self.SOURCE_NEW_FILE_COUNT += self.get_new()
        self.SOURCE_NEWER_FILE_COUNT += self.get_different()
        self.EXCLUDED_FILE_COUNT += self.get_excluded()
        self.MATCHED_FILE_COUNT += self.get_aligned()
        self.TARGET_NEWER_FILE_COUNT += self.get_target_newer()

        self.STATUS = f"Remove Obsolete Files"
        self.remove_obsolete_files(A, B)
        self.TARGET_ORPHAN_FILE_COUNT += self.get_obsolete()

        self.STATUS = f"Remove Obsolete Directories"
        self.remove_obsolete_directories(A, B)
        self.TARGET_OBSOLETE_DIRECTORY_COUNT += self.get_obsolete()

        self.STATUS = f"Subroutine Completed"

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
                            self.EXCEPTIONS.append(f"Not created: {x_rel}")

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
                            self.EXCEPTIONS.append(f"Source not copied: {x_rel}")

                    if a_date < b_date:
                        x_rel = Entities.OS_PATH.relpath(b_file_path, B)
                        self.EXCEPTIONS.append(
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
                        self.EXCEPTIONS.append(f"Not copied: {x_rel}")

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
                        self.EXCEPTIONS.append(f"Not removed: {x_rel}")
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
                            self.EXCEPTIONS.append(f"Not removed: {x_rel}")


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

    def get_run_results(self) -> dict:

        results = {
            "profile": Model_Entities.get_selected_session_name(),
            "subroutine": self.subroutine_name,
            "source_directory": self.SOURCE_PATH,
            "target_directory": self.TARGET_PATH,
            "source_directory_count": self.SOURCE_DIRECTORY_COUNT,
            "source_file_count": self.SOURCE_FILE_COUNT,
            "new_source_directory_count": self.SOURCE_NEW_DIRECTORY_COUNT,
            "new_target_directory_count": self.TARGET_NEW_DIRECTORY_COUNT,
            "obsolete_target_directory_count": self.TARGET_OBSOLETE_DIRECTORY_COUNT,
            "matched_directory_count": self.MATCHED_DIRECTORY_COUNT,
            "excluded_directory_count": self.EXCLUDED_DIRECTORY_COUNT,
            "new_source_file_count": self.SOURCE_NEW_FILE_COUNT,
            "newer_source_file_count": self.SOURCE_NEWER_FILE_COUNT,
            "updated_source_file_count": self.SOURCE_UPDATED_FILE_COUNT,
            "new_target_file_count": self.TARGET_NEW_FILE_COUNT,
            "newer_target_file_count": self.TARGET_NEWER_FILE_COUNT,
            "updated_target_file_count": self.TARGET_UPDATED_FILE_COUNT,
            "target_orphan_file_count": self.TARGET_ORPHAN_FILE_COUNT,
            "excluded_file_count": self.EXCLUDED_FILE_COUNT,
            "matched_file_count": self.MATCHED_FILE_COUNT
        }

        return results
    
    def get_subroutine_results(self) -> list:

        return self.RESULTS
    
    def get_exceptions(self) -> list:

        return self.EXCEPTIONS
    
    def get_new(self) -> int:

        return self.new

    def get_different(self) -> int:

        return self.different
    
    def get_excluded(self) -> int:

        return self.excluded

    def get_aligned(self) -> int:

        return self.aligned
    
    def get_status(self) -> None:

        return self.STATUS
    
    def get_target_newer(self) -> int:

        return self.target_newer
    
    def get_obsolete(self) -> int:

        return self.obsolete


class View:

    def __init__(self) -> None:
        pass

    def formatted_results(self, results: dict) -> list:
        """
        Apply i18n and formatting to the result from Backup.
        """


        formatted = []

        formatted.append(f"{_("Profile")}: {results["profile"]}")
        formatted.append(f"{_("Subroutine")}: {results["subroutine"]}")
        formatted.append(f"{_("Source Directory")}: {results["source_directory"]}")
        formatted.append(f"{_("Target Directory")}: {results["target_directory"]}")
        formatted.append(f"{_("Source Directory Count")}: {results["source_directory_count"]}")
        formatted.append(f"{_("Source File Count")}: {results["source_file_count"]}")
        formatted.append("")
        formatted.append(f"{_("Excluded Directory Count")}: {results["excluded_directory_count"]}")
        formatted.append(f"{_("Matched Directory Count")}: {results["matched_directory_count"]}")
        formatted.append(f"{_("Source New Directory Count")}: {results["new_source_directory_count"]}")
        formatted.append(f"{_("Target New Directory Count")}: {results["new_target_directory_count"]}")
        formatted.append(f"{_("Target Obsolete Directory Count")}: {results["obsolete_target_directory_count"]}")
        formatted.append("")
        formatted.append(f"{_("Excluded File Count")}: {results["excluded_file_count"]}")
        formatted.append(f"{_("Matched File Count")}: {results["matched_file_count"]}")
        formatted.append("")
        formatted.append(f"{_("Source New File Count")}: {results["new_source_file_count"]}")
        formatted.append(f"{_("Source Newer File Count")}: {results["newer_source_file_count"]}")
        formatted.append(f"{_("Source Updated File Count")}: {results["updated_source_file_count"]}")
        formatted.append("")
        formatted.append(f"{_("Target New File Count")}: {results["new_target_file_count"]}")
        formatted.append(f"{_("Target Newer File Count")}: {results["newer_target_file_count"]}")
        formatted.append(f"{_("Target Updated File Count")}: {results["updated_target_file_count"]}")
        formatted.append(f"{_("Target Orphan File Count")}: {results["target_orphan_file_count"]}")
        formatted.append("")
        formatted.append(f"{_("Run Date")}: {results["run_date"]}")
        formatted.append(f"{_("Run Duration")}: {results["run_time"]}")

        return formatted
