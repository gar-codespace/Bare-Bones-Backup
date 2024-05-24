import Entities

SCRIPT_NAME = f"B3.{__name__}"
SCRIPT_REV = 20240401


"""check_config_items is moved here because Model is getting big."""


def tally_items(path: str) -> int:
    """
    Counts the number of directories and files in a path.
    """

    directory_count = 0
    file_count = 0

    for root, directories, files in Entities.OS.walk(path):
        directory_count += len(directories)
        file_count += len(files)

    return directory_count, file_count


def make_directory(target_path: str) -> int:
    """
    The prefered mathod to make a directory.
    """

    result = 1
    try:
        Entities.OS.mkdir(target_path, mode=0o777, dir_fd=None)
    except FileExistsError as e:
        result = 0

    return result


def copy_file(source_path: str, target_path: str) -> int:
    """
    The prefered method to copy files.
    """

    result = 1
    Entities.SHUTIL.copy2(source_path, target_path, follow_symlinks=True)

    a_date = Entities.OS_PATH.getmtime(source_path)
    b_date = Entities.OS_PATH.getmtime(target_path)

    if a_date != b_date:
        result = 0

    return result


def file_remove(target_path: str) -> int:
    """
    The prefered method to remove a file.
    """

    result = 1
    try:
        Entities.PATHLIB.Path(target_path).unlink()
    except FileNotFoundError as e:
        # TODO add to errors list.
        result = 0
    except PermissionError as e:
        # TODO add to errors list
        # Source files marked as read only.
        result = 0

    return result


def directory_remove(target_path: str) -> str:
    """
    The prefered method to delete a directory.
    Only removes empty directories.
    """

    error = ""
    result = 1

    try:
        Entities.OS.rmdir(target_path, dir_fd=None)
    except FileNotFoundError as e:
        error = f"Directory not removed: {e}"
        result = 0
    except OSError as e:
        error = f"Directory not removed: {e}"
        result = 0

    return result


def get_target_path() -> str:

    profile = get_profile()

    target = profile["target"]
    root = Entities.OS_PATH.basename(Entities.OS_PATH.normpath(profile["source"]))
    target_path = Entities.OS_PATH.join(target, root)

    return target_path


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
