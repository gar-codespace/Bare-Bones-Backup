import Entities

from . import View_Entities

SUBROUTINE_NAME = __name__
SCRIPT_NAME = f"B3.{__name__}"
SCRIPT_REV = 20240401


class Get_GUI:
    """
    Makes the Results GUI.
    """

    def __init__(self) -> None:
        pass

    def populate_gui(settings: dict) -> None:
        """
        Populate the GUI results widgets with the results data.
        """
        pass


def display_results() -> None:

    x = ""

    for result in Entities.RESULTS:

        x += f"{result}\n"

    print(x)
