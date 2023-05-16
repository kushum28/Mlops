# write.py
import argparse
import os
from azureml.core.run import _OfflineRun
from azureml.core import Run, Workspace
from azureml.core import Workspace, Dataset,Run,Datastore,Model


def main(model_dir,model_name,model_metric_name):
    run = Run.get_context()    
    ws=run.experiment.workspace 
    # ws = Workspace.from_config()
    reg_model(ws=ws,model_name=model_name,model_dir=model_dir,model_metric_name=model_metric_name)
# ----------Funtion to register dataset-------
def reg_model(ws,model_dir,model_name,model_metric_name):

    # parent_run = run.parent
    # model_tags = {**parent_run.get_tags(), **parent_run.get_metrics()}
    #print(f'Registering model with tags: {model_tags}')

    # Register model
    model_path = os.path.join(model_dir, model_name)
    model = Model.register(
        workspace=ws,
        model_path=model_path,
        model_name=model_metric_name,
        #tags=model_tags,
        description='My first model'
    )

    print(f'Registered new model {model.name} version {model.version}')

def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=str, default='./outputs')
    parser.add_argument('--model-name', type=str, default='PG_model.pkl')
    parser.add_argument('--model-metric-name', type=str, default='PG_model',help='The name of the evaluation metric used in Train step')
    args_parsed = parser.parse_args(args_list)

    return args_parsed


if __name__ == '__main__':
    args = parse_args()
    main(model_metric_name=args.model_metric_name,model_name=args.model_name,model_dir=args.output_dir,)
    #main(model_name='PG-model.pkl',model_dir='./outputs',model_metric_name='PG_model')