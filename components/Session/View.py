import Entities

from . import View_Entities

SUBROUTINE_NAME = __name__
SCRIPT_NAME = f"B3.{__name__}"
SCRIPT_REV = 20240401


class Session_GUI:
    """
    Makes the Session GUI.
    """

    def __init__(self) -> None:
        pass


def populate_gui(self) -> None:
    """
    Populate the GUI profile widgets with the currently selected profile data.
    """

    config_file = Entities.load_json(Entities.generic_read_report("config.json"))
    h2 = config_file["selected_session"]

    # Profile details
    p1 = config_file["profiles"][h2]["mirror"]
    p2 = ", ".join(config_file["profiles"][h2]["exclude_directories"])
    p3 = ", ".join(config_file["profiles"][h2]["exclude_files"])
    p4 = config_file["profiles"][h2]["implement_excludes"]
    p5 = config_file["profiles"][h2]["modified"]  # How to set a radio button?
    p6 = config_file["profiles"][h2]["run_queue"]
    p7 = config_file["profiles"][h2]["source"]
    p8 = config_file["profiles"][h2]["subroutine"]
    p9 = config_file["profiles"][h2]["target"]


def get_profile(self) -> dict:
    """
    Returns items from the currently displayed profile.
    """

    # Pull these from the GUI.
    profile_name = "Test"
    mirror = True
    exclude_directories = ".git, __pycache__,junk"
    exclude_files = ".class"
    implement_excludes = True
    modified = {"different": True, "newer": False, "older": False}
    run_queue = False
    source = "C:\\Users\\greg9\\Documents\\Python\\Test Source\\Layouts"
    subroutine = "Backup"
    target = "C:\\Users\\greg9\\Documents\\Python\\Test Destination"

    profile = {
        profile_name: {
            "mirror": mirror,
            "exclude_directories": exclude_directories,
            "exclude_files": exclude_files,
            "implement_excludes": implement_excludes,
            "modified": modified,
            "run_queue": run_queue,
            "source": source,
            "subroutine": subroutine,
            "target": target,
        }
    }

    return profile


def append_results(formatted_results: list) -> None:

    Entities.RESULTS.append(f"{_("Session Results")}:")

    for item in formatted_results:
        Entities.RESULTS.append(item)


def append_exceptions(formatted_exceptions: list) -> None:

    # Entities.EXCEPTIONS.prepend(f"{_("Session Exceptions")}:")

    Entities.EXCEPTIONS.insert(0, f"{_("Session Exceptions")}:")

    for item in formatted_exceptions:
        Entities.EXCEPTIONS.append(item)
