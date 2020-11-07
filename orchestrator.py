import json
import papermill as pm
from datetime import datetime as dt
from pathlib import Path

# Directory to store executed notebooks
Path('nb-output').mkdir(exist_ok=True)


def process(region, pipeline):
    '''Processes the pipeline for a given region & stores the executed notebook inside nb-output/ folder.

    Input
        - region: Name of the region
        - pipeline: Pipeline to run (gridded-population / cluster / query-engine)

    Return
        None
    '''
    def execute(nb, pipeline, region):
        '''Execute a notebook using papermill.'''

        pm.execute_notebook(
            input_path=nb,
            output_path=f'nb-output/{pipeline}-executed-{region["REGION"]}_@_{dt.now().strftime("%Y-%m-%d_%I-%M-%S_%p")}.ipynb',
            parameters=region
        )

    if   pipeline == 'query'             : execute('2020-11-06-query-engine.ipynb'      , pipeline, region)
    elif pipeline == 'cluster'           : execute('2020-11-06-cluster.ipynb'           , pipeline, region)
    elif pipeline == 'gridded-population': execute('2020-11-06-gridded-population.ipynb', pipeline, region)
    else: print('Not a valid pipeline')


def exists(name, pipeline):
    '''Check if a notebook is already executed.'''
    for nb in Path('nb-output').glob(f'{pipeline}-*.ipynb'):
        if name in str(nb):
            return True
    return False


def main():
    # Load the config.json file
    config = json.load(open('config.json', 'r'))
    print(f'Requesting for regions: {[region["REGION"]+"-"+region["PIPELINE"] for region in config]}')

    # For each region, run the required pipeline
    for region in config:
        name = region['REGION']
        pipeline = region['PIPELINE']
        if not exists(name, pipeline):
            try:
                print(f'Processing {pipeline} pipeline for region: {name}')
                process(region, pipeline)
                print('Done\n')
            except pm.exceptions.PapermillException as e:
                print(f'Error while executing {pipeline} pipeline notebook for region: {name}. Check `nb-output/{pipeline}-executed-{name}-*.ipynb` for errors.\n')
        else:
            print(f'Skipping {pipeline} pipeline for region: {name}. Already, exists.\n')


if __name__ == '__main__':
    main()



