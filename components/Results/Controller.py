"""
The Results component makes the Results gui.
"""

import Entities
from components.Results import View

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
        Temporary for testing
        """

        View.display_results()
