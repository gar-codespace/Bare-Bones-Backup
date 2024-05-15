"""
Bare Bones Backup (B3) is a file backup utility.
B3 can compare two directories for directory and file differences.
B3 can copy or mirror one location to another.
B3 can synchronize two locations.
Obsolete files in the target directory are deleted if chosen.
Distributed under the MIT Open Source license, copyright (C) 2024 Gregory A Ritacco
"""

import Entities
import Diagnostics

# import Model
# import View

SCRIPT_NAME = f"B3.{__name__}"
SCRIPT_REV = 20240401


class B3:
    """
    Check the whole app.
    Set the locale.
    Create the available component frames: Session, Results, Errors, Settings.
    Combine the frames into the app.
    Display the app.
    """

    def __init__(self) -> None:

        Entities.RESULTS = []
        Entities.EXCEPTIONS = []

    def initialize_app(self) -> None:
        """
        What to do when the app starts.
        """

        # Temporary for testing
        Diagnostics.check_config_file()
        Diagnostics.check_components()
        Entities.set_locale()

        components = ["Session", "Results", "Exceptions"]
        for component in components:
            x = Entities.IM(f"components.{component}.Controller").GUI()
            x.run_component()

    # When the GUI is implemented

    # Intro animation()
    # Diagnostics.check_config_file()
    # Diagnostics.check_components()
    # Entities.set_locale()
    # app_components = []
    # for directory in Entities.generic_get_dirs("components"):
    #     component = Entities.IM(f"components.{directory}.Controller").GUI()
    #     component.make_component()
    # app_components.append(component.get_frame())
    # b3 = View.Build_App(app_components)
    # b3.make_app()
    # On intro animation end:
    # b3.show???


if __name__ == "__main__":

    app = B3()
    app.initialize_app()
