"""
The base classes for Session go here.
"""

import Entities
from components.Session import Model_Entities


SCRIPT_NAME = f"B3.{__name__}"
SCRIPT_REV = 20240401


class Subroutine_Base:

    # These are returned to the Session GUI frame.
    STATUS: str
    # These are returned to the Results GUI frame.
    PROFILE = Model_Entities.get_session()
    SUBROUTINE = Model_Entities.get_subroutine_name()

    SOURCE_PATH = PROFILE["source"]
    TARGET_PATH = PROFILE["target"]

    SOURCE_DIRECTORY_COUNT: int
    SOURCE_FILE_COUNT: int

    SOURCE_NEW_DIRECTORY_COUNT: int = 0
    TARGET_NEW_DIRECTORY_COUNT: int = 0
    TARGET_ORPHAN_DIRECTORY_COUNT: int = 0
    MATCHED_DIRECTORY_COUNT: int = 0
    EXCLUDED_DIRECTORY_COUNT: int = 0

    SOURCE_NEW_FILE_COUNT: int = 0
    SOURCE_NEWER_FILE_COUNT: int = 0
    SOURCE_UPDATED_FILE_COUNT: int = 0

    TARGET_NEW_FILE_COUNT: int = 0
    TARGET_NEWER_FILE_COUNT: int = 0
    TARGET_UPDATED_FILE_COUNT: int = 0
    TARGET_ORPHAN_FILE_COUNT: int = 0

    MATCHED_FILE_COUNT: int = 0
    EXCLUDED_FILE_COUNT: int = 0

    RUN_DATE: str
    RUN_TIME: str

    RESULTS: dict
    EXCEPTIONS: list

    # Toggles
    align: bool
    implement_excludes: bool

    # Variables for the functions.
    new: int
    excluded: int
    aligned: int
    matched: int
    different: int
    target_newer: int
    obsolete: int
    newer: int
    a_date: float
    b_date: float

    def boiler_plate(self) -> None:
        """
        Mini Controller.
        """

        self.initialize()

        self.STATUS = f"{_("Poll Source")}"
        self.poll_source()

        self.STATUS = f"{_("Add Target Root")}"
        self.add_target_root()

    def initialize(self) -> None:

        self.EXCEPTIONS = []

        self.implement_excludes = self.PROFILE["implement_excludes"]
        exd = self.PROFILE["exclude_directories"]
        self.regex_directories = Model_Entities.compile_exclude_directories(exd)
        exf = self.PROFILE["exclude_files"]
        self.regex_files = Model_Entities.compile_exclude_files(exf)

    def poll_source(self) -> None:
        """
        Counts the number of source directories and files.
        """

        A, B = Model_Entities.tally_items(self.SOURCE_PATH)

        self.SOURCE_DIRECTORY_COUNT = A
        self.SOURCE_FILE_COUNT = B

    def add_target_root(self) -> None:
        """
        The base of the source is the root of the target.
        """

        result = Model_Entities.make_directory(self.TARGET_PATH)
        if result == True:
            self.TARGET_NEW_DIRECTORY_COUNT += 1
        else:
            self.EXCEPTIONS.append(f"Target exists: {self.TARGET_PATH}")
            pass

    def correlate_directories(self, A, B) -> None:

        self.new = 0
        self.excluded = 0
        self.aligned = 0

        for root, directories, files in Entities.OS.walk(A):
            for directory in directories:
                a_path = Entities.OS_PATH.join(root, directory)

                if self._exclude_directories(a_path):
                    continue

                rel_path = Entities.OS_PATH.relpath(a_path, A)
                b_path = Entities.OS_PATH.join(B, rel_path)

                if Entities.OS_PATH.isdir(b_path):
                    self.aligned += 1
                    continue

                self.new += 1
                if self.align == False:
                    continue

                success = Model_Entities.make_directory(b_path)
                if success == False:
                    x_rel = Entities.OS_PATH.relpath(a_path, A)
                    self.EXCEPTIONS.append(f"Not copied: {x_rel}")

    def _exclude_directories(self, path) -> bool:

        exclude_toggle = False

        if not self.implement_excludes:
            return exclude_toggle

        x = path.split("\\")
        if [hit for hit in x if self.regex_directories.match(hit)]:
            self.excluded += 1
            exclude_toggle = True

        return exclude_toggle

    def correlate_files(self, A, B) -> None:

        self.new = 0
        self.newer = 0
        self.excluded = 0
        self.matched = 0
        self.target_newer = 0

        for root, directories, files in Entities.OS.walk(A):
            for file in files:

                if self._exclude_files(file):
                    continue

                a_file_path = Entities.OS_PATH.join(root, file)
                if self._exclude_directories(a_file_path):
                    continue

                rel_path = Entities.OS_PATH.relpath(root, A)
                b_file_path = Entities.OS_PATH.join(B, rel_path, file)

                a_date = Entities.OS_PATH.getmtime(a_file_path)

                try:
                    b_date = Entities.OS_PATH.getmtime(b_file_path)
                except FileNotFoundError:
                    b_date = 0.0

                if a_date == b_date:
                    self.matched += 1
                    continue

                if b_date == 0.0:
                    self.new += 1

                if a_date > b_date and b_date != 0.0:
                    self.newer += 1

                if a_date < b_date and self.align == True:
                    continue

                if self.align == False:
                    continue

                success = Model_Entities.copy_file(a_file_path, b_file_path)
                if success == False:
                    x_rel = Entities.OS_PATH.relpath(a_file_path, A)
                    self.EXCEPTIONS.append(f"Not copied: {x_rel}")

    def _exclude_files(self, file) -> bool:

        exclude_toggle = False

        if not self.implement_excludes:
            return exclude_toggle

        if self.regex_files.match(file):
            self.excluded += 1
            exclude_toggle = True

        return exclude_toggle

    def remove_obsolete_files(self, A, B):
        """
        A is source.
        B is target.
        Remove files that are in B if they're not in A.
        Remove files in B that are in the regex.
        """

        self.obsolete = 0

        for root, directories, files in Entities.OS.walk(B):
            for file in files:

                b_file_path = Entities.OS_PATH.join(root, file)
                rel_path = Entities.OS_PATH.relpath(root, B)
                a_file_path = Entities.OS_PATH.join(A, rel_path, file)

                if self.implement_excludes:
                    x = b_file_path.split("\\")
                    exd = [hit for hit in x if self.regex_directories.match(hit)]
                    exf = self.regex_files.match(file)
                else:
                    exd = False
                    exf = False

                a: bool = Entities.OS_PATH.isfile(a_file_path)
                b = not bool(exd)
                c = not bool(exf)

                if a and b and c:
                    continue

                self.obsolete += 1
                success = Model_Entities.file_remove(b_file_path)
                if not success:
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

        self.obsolete = 0
        for root, directories, files in Entities.OS.walk(B, topdown=False):
            for directory in directories:

                b_path = Entities.OS_PATH.join(root, directory)
                rel_path = Entities.OS_PATH.relpath(root, B)
                a_path = Entities.OS_PATH.join(A, rel_path, directory)
                a_path = Entities.OS_PATH.normpath(a_path)

                if self.implement_excludes:
                    x = b_path.split("\\")
                    exd = [hit for hit in x if self.regex_directories.match(hit)]
                else:
                    exd = False

                a: bool = Entities.OS_PATH.isdir(a_path)
                b = not bool(exd)

                if a and b:
                    continue

                self.obsolete += 1
                success = Model_Entities.directory_remove(b_path)
                if not success:
                    x_rel = Entities.OS_PATH.relpath(b_path, B)
                    self.EXCEPTIONS.append(f"Not removed: {x_rel}")


    def get_run_results(self) -> dict:

        results = {
            "profile": Model_Entities.get_selected_session_name(),
            "subroutine": self.SUBROUTINE,
            "source_directory": self.SOURCE_PATH,
            "target_directory": self.TARGET_PATH,
            "source_directory_count": self.SOURCE_DIRECTORY_COUNT,
            "source_file_count": self.SOURCE_FILE_COUNT,
            "new_source_directory_count": self.SOURCE_NEW_DIRECTORY_COUNT,
            "new_target_directory_count": self.TARGET_NEW_DIRECTORY_COUNT,
            "obsolete_target_directory_count": self.TARGET_ORPHAN_DIRECTORY_COUNT,
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
            "matched_file_count": self.MATCHED_FILE_COUNT,
        }

        return results
