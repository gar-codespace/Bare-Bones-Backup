import Entities

SCRIPT_NAME = f"B3.{__name__}"
SCRIPT_REV = 20240401


def run_diagnostic() -> None:
    """
    Mini controller.
    Whatever tests are necessary to check this component.
    """

    check_config_items()


def check_config_items() -> None:
    """
    Check that the config file items for this component are OK.
    """

    component_name = Entities.get_component_name(__file__)
    Entities.check_config_item(component_name)
