# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import argparse

from azureml.core import Datastore, Environment
from azureml.pipeline.core import PipelineData
from azureml.pipeline.steps import PythonScriptStep
from azureml.core.runconfig import RunConfiguration

import config 
import workspace 
import compute
import pipeline


def main(dataset_name, model_name, pipeline_name, compute_name, environment_path,
         model_metric_name, maximize, pipeline_version=None):

    # Retrieve workspace
    ws = workspace.retrieve_workspace()
    #env=Environment.get(ws,'AMLEnvironment')
    env=Environment.from_conda_specification(name='AMLEnvironment',file_path='../configuration/environments/environment_training/conda_dependencies.yml')
    # Create run config
    run_config=RunConfiguration()
    run_config.environment=env
    # Training setup
    compute_target = compute.get_compute_target(ws, compute_name)
    #env = Environment.load_from_directory(path=environment_path)
    
    run_config = RunConfiguration()
    run_config.environment = env
    print(env)
    print(run_config)
    # Create a PipelineData to pass data between steps
    pipeline_data = PipelineData(
        'pipeline_data', datastore=Datastore.get(ws, os.getenv('DATASTORE_NAME', 'workspaceblobstore'))
    )
    datadir_param = PipelineData('datadir', is_directory=True)
    # Create steps
    dataprep_step = PythonScriptStep(
        name="data preparation",
        source_directory="../src",
        script_name="data_prep.py",
        compute_target=compute_target,
        #inputs=[pipeline_data],
        arguments=['--dataset-name', dataset_name],
        runconfig=run_config,
        allow_reuse=False
    )

    train_step = PythonScriptStep(
    name="Train model",
    source_directory="../src",
    script_name="train.py",
    compute_target=compute_target,
    outputs=[datadir_param],
    arguments=[
            '--dataset-name', dataset_name,
            '--model-name', model_name,
            '--output-dir', datadir_param,            
        ],
    runconfig=run_config,
    allow_reuse=False
    )


    model_reg_step = PythonScriptStep(
        name="model register",
        source_directory="../src",
        script_name="data_register.py",
        compute_target=compute_target,
        inputs=[datadir_param],
        arguments=[
            '--output-dir', datadir_param,
            '--model-name', model_name,
            '--model-metric-name', model_metric_name,
            ],
        runconfig=run_config,
        allow_reuse=False
    )

    # train_model_reg = PythonScriptStep(
    # name="train model reg",
    # source_directory="../src",
    # script_name="data_register.py",
    # compute_target=compute_target,
    # #inputs=[pipeline_data],
    # arguments=[],
    # runconfig=run_config,
    # allow_reuse=False
    # )
    
    # train_step = PythonScriptStep(
    #     name="Train Model",
    #     source_directory="../src",
    #     script_name="train.py",
    #     compute_target=compute_target,
    #     outputs=[pipeline_data],
    #     arguments=[
    #         '--dataset-name', dataset_name,
    #         '--model-name', model_name,
    #         '--output-dir', pipeline_data,
    #         '--model-metric-name', model_metric_name,
    #     ],
    #     runconfig=run_config,
    #     allow_reuse=False
    # )
    

    # Set the sequence of steps in a pipeline
    train_step.run_after(dataprep_step)
    model_reg_step.run_after(train_step)

    # Publish training pipeline
    published_pipeline = pipeline.publish_pipeline(
        ws,
        name=pipeline_name,
        steps=[dataprep_step,train_step,model_reg_step],
        description="Model training/retraining pipeline",
        version=pipeline_version
    )
    
    print(f"Published pipeline {published_pipeline.name} version {published_pipeline.version}")


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", type=str)
    args_parsed = parser.parse_args(args_list)
    return args_parsed


if __name__ == "__main__":
    args = parse_args()

    # Get argurments from environment (these variables are defined in the yml file)
    main(
        model_name=config.get_env_var("AML_MODEL_NAME"),
        dataset_name=config.get_env_var("AML_DATASET"),
        pipeline_name=config.get_env_var("AML_TRAINING_PIPELINE"),
        compute_name=config.get_env_var("AML_TRAINING_COMPUTE"),
        environment_path=config.get_env_var("AML_TRAINING_ENV_PATH"),
        model_metric_name=config.get_env_var("TRAINING_MODEL_METRIC_NAME"),
        maximize=config.get_env_var("TRAINING_MAXIMIZE"),
        pipeline_version=args.version
    )
    # main(
    #     model_name="PG_train_model",
    #     dataset_name="PG_src_data",
    #     pipeline_name="PG_TRAINING_PIPELINE",
    #     compute_name="cpu-cluster12",
    #     environment_path="AMLEnvironment",
    #     model_metric_name="TRAINING_MODEL_METRIC_NAME",
    #     maximize="TRAINING_MAXIMIZE",
    #     pipeline_version=args.version
    # )

