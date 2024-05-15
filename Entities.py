"""
Helper functions and imports for the whole app.
"""

"""External dependencies."""

"""Standard library dependencies."""
from importlib import import_module as IM
from json import loads as JSON_LOAD_S, dumps as JSON_DUMP_S
from codecs import open as CODECS_OPEN
import pathlib as PATHLIB
import datetime as DATE_TIME
import locale as LOCALE
import gettext as GETTEXT
import time as TIME
import re as RE
import os as OS
import os.path as OS_PATH
import shutil as SHUTIL


SCRIPT_NAME = f"B3.{__name__}"
SCRIPT_REV = 20240401
APP_NAME = "Bare Bones Backup"
LOCALE_DIRECTORY = "./locales"

ENCODING = "utf-8"

RESULTS: list
EXCEPTIONS: list


"""Methods specific to this app."""


def make_new_config_file() -> None:
    """
    Creates a new default config file.
    """

    new_config_file = {}
    # new_config_file.update({"description": f"B3 version {SCRIPT_REV}"})
    new_config_file.update({"selected_session": "Default"})
    new_config_file.update({"languages": {}})

    generic_write_report("config.json", dump_json(new_config_file))

    check_languages()

    for directory in generic_get_dirs("components"):
        IM(f"components.{directory}.Model").run_diagnostic()


def check_languages() -> None:
    """
    Checks that all the language dirs in locales are included in config_file["languages"].
    Languages are dynamically added or removed fron config.
    """

    cwd = OS.getcwd()
    config_file = load_json(generic_read_report("config.json"))

    for directory in generic_get_dirs("locales"):
        ld = f"locales\\{directory}"
        lf = OS_PATH.join(cwd, ld, f"{directory}.txt")
        try:
            name = generic_read_report(str(lf))
            RESULTS.append(f"Language added: {name}")
        except:
            name = "unknown"
            EXCEPTIONS.append(f"Unknown language for: {directory}")

        config_file["languages"].update({directory: name})

    generic_write_report("config.json", dump_json(config_file))


def get_component_name(file_name: str) -> str:
    """
    The prefered method to get a components name.
    """

    return OS_PATH.basename(OS_PATH.dirname(file_name))


def check_config_item(component_name: str) -> None:
    """
    Checks that component_name is included in the config file.
    Does not check the integrity of component_name, only that it's there.
    """

    error_toggle = 0
    config_file = load_json(generic_read_report("config.json"))

    try:
        config_file[component_name]
        RESULTS.append(f"Found: {component_name} section of config file")
    except:
        cwd = OS.getcwd()
        file_path = OS_PATH.join(cwd, "components", component_name, "config.json")
        file = load_json(generic_read_report(file_path))
        config_file.update({component_name: file})
        EXCEPTIONS.append(f"Added: {component_name} section of config file")
        error_toggle = 1

    if error_toggle:
        generic_write_report("config.json", dump_json(config_file))


def set_locale() -> None:

    config_file = load_json(generic_read_report("config.json"))
    selected_language = config_file["Settings"]["selected_language"]

    LOCALE.setlocale(LOCALE.LC_ALL, selected_language)

    i18n = GETTEXT.translation(
        APP_NAME, LOCALE_DIRECTORY, fallback=True, languages=[selected_language]
    )
    i18n.install()


def get_date() -> str:
    """
    Returns an internationalized date string.
    """

    return DATE_TIME.datetime.today().strftime("%a, %x %X")


def convert_time(timed_event: float) -> object:

    return DATE_TIME.timedelta(seconds=timed_event)


"""Generic file handeling methods."""


def generic_get_dirs(dir: str) -> list:
    """
    Returns a list of directory names in 'dir'
    Filters out dunders.
    """

    test_dir = f".\\{dir}"
    result = []
    directories = OS.listdir(path=test_dir)
    for directory in directories:
        if directory.startswith("__"):
            continue
        test_path = OS_PATH.join(test_dir, directory)
        if not OS_PATH.isdir(test_path):
            continue
        result.append(directory)

    return result


def generic_get_files(dir: str) -> list:
    """
    Returns a list of file names in 'dir'
    Filters out dunders.
    """

    test_dir = f".\\{dir}"
    result = []
    directories = OS.listdir(path=test_dir)
    for file in directories:
        if file.startswith("__"):
            continue
        test_path = OS_PATH.join(test_dir, file)
        if not OS_PATH.isfile(test_path):
            continue
        result.append(file)

    return result


def generic_make_directory(target_path: str) -> int:
    """
    The prefered mathod to make a directory.
    """

    result = 1
    try:
        OS.mkdir(target_path, mode=0o777, dir_fd=None)
    except FileExistsError as e:
        result = 0

    return result


def generic_copy_file(source_path: str, target_path: str) -> int:
    """
    The prefered method to copy files.
    """

    result = 1
    SHUTIL.copy2(source_path, target_path, follow_symlinks=True)

    a_date = OS_PATH.getmtime(source_path)
    b_date = OS_PATH.getmtime(target_path)

    if a_date != b_date:
        result = 0

    return result


def generic_file_remove(target_path: str) -> int:
    """
    The prefered method to remove a file.
    """

    result = 1
    try:
        PATHLIB.Path(target_path).unlink()
    except FileNotFoundError as e:
        # TODO add to errors list.
        result = 0
    except PermissionError as e:
        # TODO add to errors list
        # Source files marked as read only.
        result = 0

    return result


def generic_directory_remove(target_path: str) -> str:
    """
    The prefered method to delete a directory.
    Only removes empty directories.
    """

    error = ""
    result = 1

    try:
        OS.rmdir(target_path, dir_fd=None)
    except FileNotFoundError as e:
        error = f"Directory not removed: {e}"
        result = 0
    except OSError as e:
        error = f"Directory not removed: {e}"
        result = 0

    return result


def generic_tally_items(path: str) -> int:
    """
    Counts the number of directories and files in a path.
    """

    directory_count = 0
    file_count = 0

    for root, directories, files in OS.walk(path):
        directory_count += len(directories)
        file_count += len(files)

    return directory_count, file_count


def generic_read_report(filePath: str) -> str:
    """
    The prefered method to read files.
    """

    with CODECS_OPEN(filePath, "r", encoding=ENCODING) as textWorkFile:
        genericReport = textWorkFile.read()

    return genericReport


def generic_write_report(filePath: str, genericReport: str) -> None:
    """
    The prefered method to write files.
    """

    try:
        ENCODING
    except UnboundLocalError:
        ENCODING = "utf-8"

    with CODECS_OPEN(filePath, "wb", encoding=ENCODING) as textWorkFile:
        textWorkFile.write(genericReport)


def load_json(file: str) -> str:
    """
    The prefered method to load a json file.
    """

    return JSON_LOAD_S(file)


def dump_json(file: str) -> str:
    """
    The prefered method to dump a json file.
    """

    return JSON_DUMP_S(file, indent=2, sort_keys=True)
