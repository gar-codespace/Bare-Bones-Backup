"""
All in one, Model applies either Backup, Compare, or Synchronize.
"""

import Entities
from components.Session import Model_Entities

SUBROUTINE_NAME = "Model"
SCRIPT_NAME = f"B3.{__name__}"
SCRIPT_REV = 20240401


def run_diagnostic() -> None:
    """
    Mini controller.
    Whatever tests are necessary to check this component.
    """

    _check_config_items()
    _check_subroutines()


def _check_config_items() -> None:
    """
    Check the config file items for this component.
    """
    # TODO Expand this

    component_name = Entities.get_component_name(__file__)
    Entities.check_config_item(component_name)


def _check_subroutines() -> None:
    """
    Check that each profile has all the subroutines.
    """

    files = Entities.generic_get_files("components\\Session\\subroutines")
    subroutines = [file.replace(".py", "") for file in files]

    config_file = Entities.load_json(Entities.generic_read_report("config.json"))
    for s_name, s_settings in config_file["Session"].items():
        names = []
        for name, state in s_settings["subroutine"].items():
            names.append(name)
        for sub in subroutines:
            if sub not in names:
                config_file["Session"][s_name]["subroutine"][sub] = False

    Entities.generic_write_report("config.json", Entities.dump_json(config_file))
