import Entities

from . import View_Entities

SUBROUTINE_NAME = __name__
SCRIPT_NAME = f"B3.{__name__}"
SCRIPT_REV = 20240401


class Get_GUI:
    """
    Makes the Exceptions GUI.
    """

    def __init__(self) -> None:
        pass

    def populate_gui(settings: dict) -> None:
        """
        Populate the GUI exceptions widgets with the exceptions data.
        """
        pass


def display_exceptions() -> None:

    x = ""

    for result in Entities.EXCEPTIONS:

        x += f"{result}\n"

    print(x)
