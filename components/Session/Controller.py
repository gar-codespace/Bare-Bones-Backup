"""
The Session component makes the session gui and runs
Compare, Backup, or Synchronize.
"""

import Entities
from components.Session import Model
from components.Session import View
from components.Session import Model_Entities

SUBROUTINE_NAME = __name__
SCRIPT_NAME = f"B3.{__name__}"
SCRIPT_REV = 20240401


class GUI:

    def __init__(self) -> None:

        self.component_frame: object

    def make_component(self) -> None:
        """
        Make the component frame here.
        """

    def get_frame(self) -> object:

        return self.component_frame

    def run_component(self) -> None:
        """
        When the 'Run Session' button is pressed.
        Directly call the subroutine.
        """

        self.save_session()

        check_source = Model_Entities.check_path("source")
        if check_source == False:
            self.formatted_results.append(f"None: invalid source path.")
            self.exceptions.append(f"Session not run: Invalid source path.")

        check_target = Model_Entities.check_path("target")
        if check_target == False:
            self.formatted_results.append(f"None: invalid target path.")
            self.exceptions.append(f"Session not run: Invalid target path.")

        if check_source and check_target:
            subroutine_name = Model_Entities.get_subroutine_name()
            subroutine = Entities.IM(
                f"components.Session.subroutines.{subroutine_name}"
            )
            subroutine_controller = subroutine.Controller()
            subroutine_view = subroutine.View()

            subroutine_controller.run()
            subroutine_results = subroutine_controller.get_subroutine_results()
            subroutine_verbose = subroutine_controller.get_subroutine_verbose()
            subroutine_exceptions = subroutine_controller.get_subroutine_exceptions()

            results = subroutine_view.formatted_results(subroutine_results)

            config_file = Entities.load_json(
                Entities.generic_read_report("config.json")
            )
            report_verbose = config_file["Settings"]["report_verbose"]

            if report_verbose == True:
                results = subroutine_view.append_verbose(subroutine_verbose)

        View.append_results(results)
        View.append_exceptions(subroutine_exceptions)

    def get_session(self) -> None:
        """
        When the user selects one of the sessions from the dropdown.
        """

    def save_session(self) -> None:
        """
        When the user presses the 'Save' button.
        """

    def delete_session(self, profile: str) -> None:
        """
        When the user presses the 'Delete' button.
        'Delete' changes to 'Confirm' to confirm delete.
        """

    def confirm_delete(self, profile: str) -> None:
        """
        When the user presses the 'Confirm' button.
        Delets the current profile.
        """
