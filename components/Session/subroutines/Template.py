"""
Use this template to add a new subroutine.
Each subroutine has two classes, Model and View.
The controller is Session.Controller
"""

import Entities
from components.Session import Model_Entities

SUBROUTINE_NAME = "Template"
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

        self.STATUS: str

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

        # What this subroutine does

        run_time = Entities.TIME.time() - start_time

        self.RESULTS = self.get_run_results()
        self.RESULTS["run_time"] = Entities.convert_time(run_time)
        self.RESULTS["run_date"] = Entities.get_date()

    def get_status(self) -> None:

        return self.STATUS

    def get_run_results(self) -> dict:

        results = {}

        return results

    def get_subroutine_results(self) -> list:

        return self.RESULTS

    def get_exceptions(self) -> list:

        return self.EXCEPTIONS


class View:

    def __init__(self) -> None:
        pass

    def formatted_results(results: dict) -> list:
        """
        Apply i18n and formatting to the result from Template.
        """

        formatted = []

        return formatted
