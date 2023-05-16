import os
import argparse
from pathlib import Path

from azureml.core import Workspace, Model, Environment
from azureml.core.model import InferenceConfig


ws = Workspace.from_config()

model = Model(ws, 'anomaly_model')

environment = Environment.from_pip_requirements(
    name='AMLEnvironment',
    file_path='requirements.txt'
)

inference_config = InferenceConfig(
    entry_script='score.py',
    source_directory='.',
    environment=environment
)

package = Model.package(ws,
                        models=[model],
                        inference_config=inference_config,
                        image_name='anomaly-detection-service',
                        generate_dockerfile=True)
package.wait_for_creation(show_output=True)

# package.pull()  # Download image locally
package.save("docker/")  # Download Dockerfile & dependencies (if generate_dockerfile=True)

# acr = package.get_container_registry()
# print("Address:", acr.address)
# print("Username:", acr.username)
# print("Password:", acr.password)