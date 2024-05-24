"""
The Session component makes the session gui and runs
Compare, Backup, or Synchronize.
"""

import Entities
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
        Bypass Model, go straight to the subroutine.
        """

        try:
            subroutine_name = Model_Entities.get_subroutine_name()
            subroutine = Entities.IM(
                f"components.Session.subroutines.{subroutine_name}"
            )
            subroutine_controller = subroutine.Controller()
            subroutine_view = subroutine.View()

            subroutine_controller.run()
            subroutine_results = subroutine_controller.get_subroutine_results()
            formatted_results = subroutine_view.formatted_results(subroutine_results)
            exceptions = subroutine_controller.get_exceptions()

        except ModuleNotFoundError:  # no subroutine is selected.
            formatted_results = []
            exceptions = []
            formatted_results.append(f"None: no Session Action selested")
            exceptions.append(f"No Session Action is selected.")

        View.append_results(formatted_results)
        View.append_exceptions(exceptions)

    def get_profile(profile: str) -> None:
        """
        When the user selects one of the profiles from the dropdown.
        """

        config_file = Entities.load_json(Entities.generic_read_report("config.json"))
        config_file.update({"selected_session": profile})
        Entities.generic_write_report("config.json", Entities.dump_json(config_file))

        View.populate_gui()

    def save_profile() -> None:
        """
        When the user presses the 'Save' button.
        """

    def delete_profile(profile: str) -> None:
        """
        When the user presses the 'Delete' button.
        'Delete' changes to 'Confirm' to confirm delete.
        """

    def confirm_delete(profile: str) -> None:
        """
        When the user presses the 'Confirm' button.
        Delets the current profile.
        """
