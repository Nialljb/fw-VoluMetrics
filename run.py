#!/usr/bin/env python
import logging
from app.parser import parse_config
from app.main import create_cover_page, parse_csv, create_data_report, merge_pdfs
from datetime import datetime

# import flywheel functions
from flywheel_gear_toolkit import GearToolkitContext


"""The run script.

This script is the entry point for the gear. It is responsible for setting up the
gear environment and executing the main function.
- logging is initialized
- the gear context is created
- the main function is executed

"""

# Initialize the logger
log = logging.getLogger(__name__)

# Define the main function
def main(context: GearToolkitContext) -> None:

    # Step 0: Parse the configuration file
    user, filepath, input_label, age_min, age_max, threshold, project_label = parse_config(context)

    # Step 1: Create the cover page
    cover = create_cover_page(user, input_label, age_min, age_max, threshold, project_label)

    # Step 2: Parse the CSV file
    df, summary_table, filtered_df, n, n_projects, n_sessions, n_clean_sessions, outlier_n, project_labels, labels = parse_csv(filepath, project_label, age_min, age_max, threshold)

    # Step 3: Create the data report
    report = create_data_report(df, summary_table, filtered_df, n, n_projects, n_sessions, n_clean_sessions, outlier_n, project_labels, labels, age_min, age_max, threshold)

    # Step 4: Merge cover page and data report
        # Get the current timestamp
    current_timestamp = datetime.now()
    # Format the timestamp as a string
    formatted_timestamp = current_timestamp.strftime('%Y-%m-%d_%H-%M-%S')

    final_report = "/flywheel/v0/output/" + project_label + "_" + formatted_timestamp + "_report.pdf"

    merge_pdfs(cover, report, final_report)

    print("Report generated: final_report.pdf")


# Only execute if file is run as main, not when imported by another module
if __name__ == "__main__":  # pragma: no cover
    # Get access to gear config, inputs, and sdk client if enabled.
    with GearToolkitContext() as gear_context:

        # Initialize logging, set logging level based on `debug` configuration
        # key in gear config.
        gear_context.init_logging()

        # Pass the gear context into main function defined above.
        main(gear_context)
