import os, sys, glob
import json
import pandas as pd
import makePlan, applyPlan
from datetime import datetime
from zipfile import ZipFile


def main():
    # Load env vars (variable deliminator)
    separator = os.environ.get("SEPARATOR")
    input_dir = os.environ.get("INPUT_DIR")

    if separator is not None:
        print(f"\nUsing {separator} to split variable into parts")
    else:
        print("\nSEPARATOR was not provided, defaulting to '_'")
        separator = '_'

    if input_dir is not None:
        print(f"\nUsing {separator} to split variable into parts")
    else:
        print("\INPUT_DIR was not provided, defaulting to '/input'")
        input_dir = '/input'

    # Load map files (at least primary changemap.json required--pre and post script maps are optional)
    print(f"\nSearching for change map files (required)...")
    print(f"\nLooking for existing plan file to include changes made in previous instruments...")

    # Find all the config files: changemap, preChangemap, postChangemap, plan
    configfiles = glob.glob(f'{input_dir}/*.json')
    print(f'Using these configs: {configfiles}')
    
    # load config files and enforce proper json formatting
    # flexible config file labelling
    for file in configfiles:
        if file.startswith('pre'):
            predata = json.load(open(file))
            prejsoncontent = json.dumps(predata)
            preChangemaps = json.loads(prejsoncontent)
        elif file.startswith('post'):
            postdata = json.load(open(file))
            postjsoncontent = json.dumps(postdata)
            postChangemaps = json.loads(postjsoncontent)
        # uncomment to apply pre-existing plans (needs accommodation in zips loop below)
        # elif file.startswith('plan'):
        #     try:
        #         plandata = json.load(open(file))
        #         planjsoncontent = json.dumps(plandata)
        #         plan = json.loads(planjsoncontent)
        #     except: pass
        else:
            data = json.load(open(file))
            jsoncontent = json.dumps(data) #json.dumps take a dictionary as input and returns a string as output.
            changemaps = json.loads(jsoncontent) # json.loads take a string as input and returns a dictionary as output.

    try: print(f"\nLoading existing change plan: {plan}\n")
    except: plan = {}
    
    # Redcap instruments are exported as zips
    zips = glob.glob(os.path.join(input_dir), "*.zip")

    for surveyzip in zips:

        print(f"\nUnzipping {surveyzip}...")
        with ZipFile(surveyzip, 'r') as zObject:
            zObject.extractall(input_dir)

        # Find all project files extracted from zip
        projectfiles = glob.glob(f'{input_dir}/*.csv') + glob.glob(f'{input_dir}/*.txt')
        
        # find datadict in project files
        for projectfile in projectfiles:
            # data dict is called 'instrument.csv'
            if 'instrument' in projectfile:
                print(f"\nUsing data dictionary file: {projectfile}")
                datadict = projectfile
        print(f"\nLoading data dictionary into dataframe...")
        with open(datadict, 'r') as f:
            df = pd.read_csv(f)
        varcol = str('Variable / Field Name')
        formcol = str('Form Name')
        varnames = df.loc[:, (varcol)]      # varnames and formnames will be compared to changemap
        formnames = df.loc[:, (formcol)]

        # read map file and apply changes for each survey map supplied in it
        for survey in changemaps:
            
            #######################################
            #    THE REAL ACTION - MAKE PLAN
            #######################################

            # Take each survey in list of zip files and generate a find & replace key:value file
            plan = makePlan(separator, varnames, formnames, survey, preChangemaps, changemaps, postChangemaps)

            print(f"\nSaving plan for future modifications. This is experimental and may have unexpected results...")
            planfile = f'{input_dir}/plan_{survey}.json'
            with open(planfile, 'w') as pf:
                pf.write(json.dumps(plan))

            print(f"\nApplying plan \n\n {plan} \n\nto all files found: \n{projectfiles}\n")
            print(f"Will result in new zip file in {input_dir} that you can upload to redcap")
            #######################################
            #    REAL ACTION - APPLY PLAN
            #######################################
            applyPlan(plan, zipfile)    # variables scanned in datadict appear all over the project in various files, so we need to run mass find & replace using the key we just generated

main()

    