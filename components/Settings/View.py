import Entities

from . import View_Entities

SUBROUTINE_NAME = __name__
SCRIPT_NAME = f"B3.{__name__}"
SCRIPT_REV = 20240401


class Get_GUI:
    """
    Makes ths Settings GUI.
    """

    def __init__(self) -> None:
        pass

    def populate_gui(settings: dict) -> None:
        """
        Populate the GUI settings widgets with the settings data.
        """

        # Profile details
        s1 = settings["q_run_auto"]
        s2 = settings["q_run_time"]
        s3 = settings["report_verbose"]
        s4 = settings["save_on_run"]
        s5 = settings["selected_language"]
