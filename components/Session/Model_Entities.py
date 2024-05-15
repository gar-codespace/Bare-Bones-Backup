import Entities

SCRIPT_NAME = f"B3.{__name__}"
SCRIPT_REV = 20240401

"""check_config_items is moved here because Model is getting big."""


def validate_directories() -> None:
    """
    Checks that the source and target directories are valid paths.
    """

    session_name = get_selected_session_name()
    config_file = Entities.load_json(Entities.generic_read_report("config.json"))

    test_directory = config_file["Session"][session_name]["source"]
    if not Entities.OS_PATH.isdir(test_directory):
        error = f"Not a valid source directory"
        Entities.EXCEPTIONS.append(f"{error}:\n   {test_directory}")

    test_directory = config_file["Session"][session_name]["target"]
    if not Entities.OS_PATH.isdir(test_directory):
        error = f"Not a valid target directory"
        Entities.EXCEPTIONS.append(f"{error}:\n   {test_directory}")

    print(Entities.EXCEPTIONS)


def compile_exclude_directories(exclude_directories: list) -> object:
    """
    For the app, the user will type in a comma or space seperated list of excludes.
    No wild cards at this time.
    """

    corrected = [r"^\s"]  # Test if first character is whitespace.

    for exclude in exclude_directories:
        corrected.append(rf"^{exclude}$")
        # corrected.append(rf"^({exclude})$")

    return Entities.RE.compile(r"|".join(corrected))


def compile_exclude_files(exclude_files: list) -> object:
    """
    For the app, the user will type in a comma or space seperated list of excludes.
    If the exclude is .xxx, all files of type xxx are excluded.
    If the exclude is xxx, all files whose name is exactly xxx are excluded.
    Excludes are case sensitive.
    """

    corrected = [r"^\s"]  # Test if frst character is whitespace.

    for exclude in exclude_files:
        if exclude.startswith("."):
            x = rf".*[.]{exclude[1:]}$"
        else:
            x = rf"^{exclude}[.].*$"

        corrected.append(rf"{x}")

    return Entities.RE.compile(r"|".join(corrected))


def get_profile() -> dict:
    """
    Returns the data for the selected profile.
    """

    config_file = Entities.load_json(Entities.generic_read_report("config.json"))
    selected_session = config_file["selected_session"]
    current_profile = config_file["Session"][selected_session]

    return current_profile


def get_subroutine_name() -> str:

    profile = get_profile()
    for key, value in profile["subroutine"].items():
        if value:
            return key


def get_selected_session_name() -> str:

    config_file = Entities.load_json(Entities.generic_read_report("config.json"))
    selected_session = config_file["selected_session"]

    return selected_session


# def check_config_items() -> None:
#     """
#     Check that the config file items for this component are OK.
#     """
#     # TODO Expand this

#     base_name = Entities.get_component_name(__file__)
#     Entities.check_config_item(base_name)


# def check_subroutines() -> None:
#     """
#     Check that each profile has all the subroutines.
#     """

#     files = Entities.generic_get_files("components\\Session\\subroutines")
#     subroutines = [file.replace(".py", "") for file in files]

#     config_file = Entities.load_json(Entities.generic_read_report("config.json"))
#     for s_name, s_settings in config_file["Session"].items():
#         names = []
#         for name, state in s_settings["subroutine"].items():
#             names.append(name)
#         for sub in subroutines:
#             if sub not in names:
#                 config_file["Session"][s_name]["subroutine"][sub] = False

#     Entities.generic_write_report("config.json", Entities.dump_json(config_file))
