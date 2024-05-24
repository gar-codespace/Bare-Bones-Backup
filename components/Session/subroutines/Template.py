"""
Use this template to add a new subroutine.
Each subroutine has two classes, Model and View.
The controller is Session.Controller
"""

import Entities
from components.Session import Model_Entities
from components.Session.Model_Base import Subroutine_Base as SB

SUBROUTINE_NAME = "Backup"
SCRIPT_NAME = f"B3.{__name__}"
SCRIPT_REV = 20240401


class Controller(SB):

    def run(self) -> None:

        start_time = Entities.TIME.time()

        self.initialize()

        self.STATUS = f"{_("Validate Directories")}"
        Model_Entities.validate_directories()

        self.STATUS = f"{_("Poll Source")}"
        SB.poll_source(self)

        # self.STATUS = f"Add Target Root"
        # SB.add_target_root(self)

        # Do your thing here.

        self.STATUS = f"{_("Subroutine Completed")}"

        run_time = Entities.TIME.time() - start_time

        self.RESULTS = self.get_run_results()
        self.RESULTS["run_time"] = Entities.convert_time(run_time)
        self.RESULTS["run_date"] = Entities.get_date()

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
