import Entities

SCRIPT_NAME = f"B3.{__name__}"
SCRIPT_REV = 20240401


def run_diagnostic() -> None:
    """
    Mini controller.
    Whatever tests are necessary to check this component.
    """

    _check_config_items()


def _check_config_items() -> None:
    """
    Check that the config file items for this component are OK.
    """

    component_name = Entities.get_component_name(__file__)
    Entities.check_config_item(component_name)

    error_toggle = 0
    config_file = Entities.load_json(Entities.generic_read_report("config.json"))

    try:
        config_file["Settings"]["selected_language"]
    except TypeError:
        Entities.EXCEPTIONS.append(f"Corrupt key: selected_language, new entry written")
        config_file["Settings"].update({"selected_language": "en"})
        error_toggle = 1

    try:
        config_file["Settings"]["save_on_run"]
    except:
        Entities.EXCEPTIONS.append(f"Corrupt key: save_on_run, new entry written")
        config_file["Settings"].update({"save_on_run": True})
        error_toggle = 1

    try:
        config_file["Settings"]["q_run_time"]
    except:
        Entities.EXCEPTIONS.append(f"Corrupt key: q_run_time, new entry written")
        config_file["Settings"].update({"q_run_time": ""})
        error_toggle = 1

    try:
        config_file["Settings"]["q_run_auto"]
    except:
        Entities.EXCEPTIONS.append(f"Corrupt key: q_run_auto, new entry written")
        config_file["Settings"].update({"q_run_auto": False})
        error_toggle = 1

    try:
        config_file["Settings"]["report_verbose"]
    except:
        Entities.EXCEPTIONS.append(f"Corrupt key: report_verbose, new entry written")
        config_file["Settings"].update({"report_verbose": True})
        error_toggle = 1

    if error_toggle:
        Entities.generic_write_report("config.json", Entities.dump_json(config_file))
