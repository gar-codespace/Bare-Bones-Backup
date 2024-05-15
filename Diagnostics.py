"""
Test the integrity of any element in B3.
"""

import Entities


def check_config_file() -> None:
    """
    Mini controller.
    Check that the config.json has the required elements.
    Run all component specific checks.
    """

    Entities.RESULTS.append(f"B3 startup:")
    test_config_file()
    check_components
    check_selected_profile()
    Entities.check_languages()


def test_config_file() -> None:
    """
    Read the config file to test if it's a valid json.
    """

    try:
        Entities.load_json(Entities.generic_read_report("config.json"))
        Entities.RESULTS.append(f"Configuration file integrity validated")
    except:
        Entities.make_new_config_file()
        Entities.EXCEPTIONS.append(f"Corrupted configuration file, new file written")


def check_selected_profile() -> None:
    """
    Check that selected_session has a profile in config_file["profiles"]
    """

    config_file = Entities.load_json(Entities.generic_read_report("config.json"))

    profiles = [k for k, v in config_file["Session"].items()]
    if config_file["selected_session"] in profiles:
        Entities.RESULTS.append(f"Current profile: {config_file["selected_session"]}")
    else:
        Entities.EXCEPTIONS.append(f"Selected profile invalid: {config_file["selected_session"]}")
        config_file.update({"selected_session": config_file["profiles"][0]})
        Entities.generic_write_report("config.json", Entities.dump_json(config_file))


def check_components() ->None:
    """
    Each component has its own diagnostic.
    Run them all.
    """

    for directory in Entities.generic_get_dirs("components"):
        Entities.IM(f"components.{directory}.Model").run_diagnostic()
