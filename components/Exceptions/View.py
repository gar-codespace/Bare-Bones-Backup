import Entities

from . import View_Entities

SUBROUTINE_NAME = __name__
SCRIPT_NAME = f"B3.{__name__}"
SCRIPT_REV = 20240401


class Get_GUI:
    def __init__(self) -> None:
        pass

    def populate_gui(settings: dict) -> None:
        """
        Populate the GUI errors widgets with the errors data.
        """
        pass


def display_exceptions() -> None:

    x = ""

    for result in Entities.EXCEPTIONS:

        x += f"{result}\n"

    print(x)
