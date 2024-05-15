"""
The word exceptions is not used in the programming sense,
rather Exceptions can display errors,
but it will also display a list of work not from Session.
"""

import Entities
from components.Exceptions import View

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

    def clear_exceptions(self) -> None:
        """
        When the 'Clear Exceptions' button is pressed.
        """
        pass

    def run_component(self) -> None:
        """
        Temporary for testing
        """

        View.display_exceptions()
