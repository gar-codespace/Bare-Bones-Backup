import Entities

from . import View_Entities

SUBROUTINE_NAME = __name__
SCRIPT_NAME = f"B3.{__name__}"
SCRIPT_REV = 20240401


class Get_GUI:
    """
    Makes the Session GUI.
    """

    def __init__(self) -> None:
        pass


    def populate_gui(self) -> None:
        """
        Populate the GUI profile widgets with the currently selected session data.
        """

        config_file = Entities.load_json(Entities.generic_read_report("config.json"))
        h2 = config_file["selected_session"]

        # Profile details
        p1 = ", ".join(config_file["profiles"][h2]["exclude_directories"])
        p2 = ", ".join(config_file["profiles"][h2]["exclude_files"])
        p3 = config_file["profiles"][h2]["implement_excludes"]
        p4 = config_file["profiles"][h2]["subroutine"] # How to set a radio button?
        p5 = config_file["profiles"][h2]["run_queue"]
        p6 = config_file["profiles"][h2]["source"]
        p7 = config_file["profiles"][h2]["target"]


def append_results(formatted_results: list) -> None:

    Entities.RESULTS.append(f"{_("Session Results")}:")

    for item in formatted_results:
        Entities.RESULTS.append(item)


def append_exceptions(formatted_exceptions: list) -> None:


    Entities.EXCEPTIONS.insert(0, f"{_("Session Exceptions")}:")

    for item in formatted_exceptions:
        Entities.EXCEPTIONS.append(item)
