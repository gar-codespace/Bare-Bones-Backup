"""
All in one, Model applies either Backup, Compare, or Synchronize.
"""

import Entities

# from components.Session import Model_Entities

SUBROUTINE_NAME = "Model"
SCRIPT_NAME = f"B3.{__name__}"
SCRIPT_REV = 20240401


def run_diagnostic() -> None:
    """
    Mini controller.
    When the app starts.
    Whatever tests are necessary to check this component.
    """

    _check_config_items()


def _check_config_items() -> None:
    """
    Check the config file items for this component.
    """
    # TODO Expand this

    component_name = Entities.get_component_name(__file__)
    Entities.check_config_item(component_name)
