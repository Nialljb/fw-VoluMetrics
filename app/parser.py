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
    #recon-all output, QC output , [add more as needed]
    input_labels = {"qc":""} #REMOVE HARCODED FILENAME AFTER TESTING ; parsed_qc_annotations_2024-10-31_22-33-35.csv
    name_key_maping = {
    "recon-all-clinical": "volumetric",
    "synthseg": "volumetric",
    "mrr_axireg": "volumetric",
    "parsed_qc_annotations": "qc"
}

    # file_inputs = ['parsed_qc_annotations_2024-10-31_22-33-35.csv','UCT-Khula-Hyperfine-rec_mrr_axireg_volumes.csv']
    # print('This report will contain data from:\n',list(input_labels.keys)[0],list(input_labels.keys)[1])
    for filename in os.listdir(directory_path):
    #for filename in file_inputs: #This line was used when debugging locally and specifying filenames
        for keyword, key in name_key_maping.items():
            if keyword in filename:
                if key == "qc":
                    input_labels['qc'] = filename
                else:
                    input_labels['volumetric'] = filename
                #break

    print("Input files found: ", input_labels)

    impute_information(context,input_labels['volumetric'])
    rename_columns (input_labels['volumetric'])

    return user, df, input_labels, age_min, age_max, threshold, project_label, directory_path


def impute_information(context,vols):

    """Imputes missing information needed for the plotting functions. 
    Currently it handles sex (Add as needed)

    Returns:
        imputed file
    """

    
    api_key = context.get_input("api-key").get("key")
    fw = flywheel.Client(api_key=api_key)

    input_container = context.client.get_analysis(context.destination["id"])
    proj_id = input_container.parents["project"]
    project_container = context.client.get(proj_id)
    project_label = project_container.label
    
    project = fw.projects.find_first(f'label="{project_label}"')



    directory_path = '/flywheel/v0/input/input'
    df = pd.read_csv(os.path.join(directory_path,vols))
    # Check if the sex column has empty values
    column_name = 'sex'
    #has_empty_values = df[column_name].isnull().any()

    #For every session get the sex information for those with missing
    for index, row in df[df[column_name].isnull()].iterrows():
        subject_label = row['subject']

        # Find the subject by label
        subject = next((s for s in project.subjects() if s.label == subject_label), None)

        print(f"Imputing value for subject: {subject_label}")
        print("Subject label: ", subject.label)

        subject = subject.reload()
        
        df.at[index, column_name] = subject.sex

        #Printing the imputed csv to the input directory to be used for plotting
        df.to_csv(os.path.join(directory_path,vols))

def rename_columns (vols):

    print('RENAMING COLUMNS....')

    directory_path = '/flywheel/v0/input/input'
    df = pd.read_csv(os.path.join(directory_path,vols))
    

    name_key_maping = {
    "recon-all":{'total intracranial': 'total intracranial'},
    "synthseg": {'total intracranial': 'total intracranial'},
    "mrr_axireg":{'icv': 'total intracranial'}}

    for keyword, key in name_key_maping.items():
        print(keyword,vols)
        if keyword in vols:
            print(df.columns.tolist())
            column_mapping = name_key_maping[keyword]
            df.rename(columns=column_mapping,inplace=True)
            print('Column has been renamed')
        


    df.to_csv(os.path.join(directory_path,vols))
