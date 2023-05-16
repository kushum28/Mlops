import numpy as np # version 1.22.4
import pandas as pd # version 1.1.3
#import matplotlib.pyplot as plt # version 3.3.4
from datetime import datetime
from datetime import timedelta
# from sklearn.preprocessing import StandardScaler # version 1.2.1
# from pyod.models.iforest import IForest # version 1.0.7
# import matplotlib.dates as mdates
import os
import argparse
from azureml.core import Run, Model,Workspace,Dataset,Datastore
def main(dataset_name):
    
    file_name1 = 'Pat_Cain_Data'
    data = load_data(file_name1)
    test=data
    #dataset_name="PG_data"
    print ("data loaded  successfully")
    
    run=Run.get_context()
    ws=run.experiment.workspace
    # ws = Workspace.from_config()
    datastore = ws.get_default_datastore()
    print ("pipeline tested  successfully")
    register_data(test,dataset_name,datastore)


def parser(s):
    try: 
        to_return = datetime.strptime(str(s), '%m/%d/%Y %H:%M:%S')
    except:
        to_return = datetime.strptime(str(s), '%Y-%m-%d %H:%M:%S')
    return to_return


def load_data(file_name1):
    print('Reading data')
    test = pd.read_csv(file_name1+'.csv', parse_dates=[0], index_col=0, date_parser=parser)
    # test = pd.read_csv(file_name1+'.csv', parse_dates=[0], index_col=0, date_parser=parser)
    return test


def register_data(df,dataset_name,datastore):
# Register the dataset
    ds = Dataset.Tabular.register_pandas_dataframe(
            dataframe=df, 
            name=dataset_name, 
            description='dataset to be registered',
            target=datastore
        )

    # Display information about the dataset
    print(ds.name + " v" + str(ds.version) + ' (ID: ' + ds.id + ")")


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset-name', type=str, default='PG_data')
    # parser.add_argument('--output-dir', type=str, default='./outputs')
    # parser.add_argument('--model-name', type=str, default='oj_sales_model.pkl')
    # parser.add_argument('--model-metric-name', type=str, default='mse',
    #                     help='The name of the evaluation metric used in Train step')
    args_parsed = parser.parse_args(args_list)

    return args_parsed


if __name__ == '__main__':
    args = parse_args()
    main(dataset_name=args.dataset_name)
