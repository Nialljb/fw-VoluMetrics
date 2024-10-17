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
    user = fw.get_current_user().email
    print(f"Logged in as {fw.get_current_user().email}")

    input_container = context.client.get_analysis(context.destination["id"])
    proj_id = input_container.parents["project"]
    project_container = context.client.get(proj_id)
    project_label = project_container.label
    print("project label: ", project_label)

    # -------------------  Get Input Data -------------------  #

    df = context.get_input_path("input")
    if df:
        log.info(f"Loaded {df}")
        inputs_provided = True
    else:
        log.info("Session spreadsheet not provided")
        inputs_provided = False

    age_min = context.config.get("age_min")
    age_max = context.config.get("age_max")
    threshold = context.config.get("threshold")

    # -------------------  Get Input label -------------------  #

    # Specify the directory you want to list files from
    directory_path = '/flywheel/v0/input/input'
    # List all files in the specified directory
    input_labels = []
    for filename in os.listdir(directory_path):
        input_labels.append(filename)

    print("Input label: ", input_labels)

    return user, df, input_labels, age_min, age_max, threshold, project_label

