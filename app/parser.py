"""Parser module to parse gear config.json."""

from typing import Tuple
import os
import re
from flywheel_gear_toolkit import GearToolkitContext
import flywheel
import pandas as pd
import logging

log = logging.getLogger(__name__)


def parse_config(context):
    """Parse the config and other options from the context, both gear and app options.

    Returns:
        gear_inputs
        gear_options: options for the gear
        app_options: options to pass to the app
    """

    # -------------- Get the gear configuration -------------- #

    api_key = context.get_input("api-key").get("key")
    fw = flywheel.Client(api_key=api_key)
    user = fw.get_current_user()
    print(f"Logged in as {fw.get_current_user().email}")

    # input_container = context.client.get_analysis(context.destination["id"])

    # -------------------  Get Input Data -------------------  #

    df = context.get_input_path("input")
    if df:
        log.info(f"Loaded {df}")
        inputs_provided = True
    else:
        log.info("Session spreadsheet not provided")
        inputs_provided = False

    # -------------------  Get Input label -------------------  #

    # Specify the directory you want to list files from
    directory_path = '/flywheel/v0/input/input'
    # List all files in the specified directory
    for filename in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, filename)):
            filename_without_extension = filename.split('.')[0]
            no_white_spaces = filename_without_extension.replace(" ", "")
            # no_white_spaces = filename.replace(" ", "")
            cleaned_string = re.sub(r'[^a-zA-Z0-9]', '_', no_white_spaces)
            input_label = cleaned_string.rstrip('_') # remove trailing underscore

    print("Input label: ", input_label)

    return user, df, input_label

