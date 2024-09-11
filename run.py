#!/usr/bin/env python
import logging
from app.parser import parse_config
from app.main import create_cover_page, parse_csv, create_data_report, merge_pdfs
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

    user, df, input_label = parse_config()

    # Step 1: Create the cover page
    cover = create_cover_page(user, input_label)

    # Step 2: Parse the CSV file
    summary_table, filtered_df, n, n_projects, n_sessions, n_clean_sessions, outlier_n, project_labels, labels = parse_csv(df)

    # Step 3: Create the data report
    report = create_data_report(summary_table, filtered_df, n, n_projects, n_sessions, n_clean_sessions, outlier_n, project_labels, labels)

    # Step 4: Merge cover page and data report
    merge_pdfs(cover, report, "final_report.pdf")

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
