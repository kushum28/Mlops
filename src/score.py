import os
import logging
import json
import joblib

import pandas as pd
from azureml.contrib.services.aml_response import AMLResponse


def init():
    """
    This function is called when the container is initialized/started, typically after create/update of the deployment.
    You can write the logic here to perform init operations like caching the model in memory
    """
    global model_artifact

    # AZUREML_MODEL_DIR is an environment variable created during deployment.
    # It is the path to the model folder (./azureml-models/$MODEL_NAME/$VERSION)
    model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR"), "model.pkl")
    model_artifact = joblib.load(model_path)

    logging.info("Init complete")


def run(raw_data):
    """
    This function is called for every invocation of the endpoint to perform the actual scoring/prediction.
    In the example we extract the data from the json input and call the scikit-learn model's predict()
    method and return the result back
    """
    logging.info(f"Request received: {raw_data[:500]}...")

    try:
        data = format_input(raw_data)
        print(data.head())  #TODO: remove when fully tested with new data
    except ValueError as e:
        return AMLResponse(f"Wrong input: {str(e)}", 400)

    model = model_artifact['model']
    scores = model.predict_proba(data)[:,1]
    anomalies_flag = scores > model_artifact['threshold']

    print("++++")  #TODO: remove when fully tested with new data
    print(scores)
    print(anomalies_flag)
    print("++++")

    output = format_output(
        timestamps=data.index.values,
        scores=scores,
        is_anomaly=anomalies_flag
    )

    logging.info(f"Request processed. {len(data)} records, {sum(anomalies_flag)} anomalies found.")

    return output


def format_input(raw_data):
    '''
    Expected format:
    {
        'DateTime': '2/3/2022 15:00:00',
        'items': [
            {'Tag': 'FFR_4_SO3_Concentration_Calc.Out_PV', 'NumericValue': '3.214424372'},
            {'Tag': 'FIT004D.Out_PV', 'NumericValue': '463.9176025'}, 
            ...
         ]
    }
    '''
    data_json = json.loads(raw_data)
    if not isinstance(data_json, dict):
        raise ValueError('Input should be a dictionary.')

    features_in_order = model_artifact['features']

    try:
        timestamp = data_json['DateTime']
        tags_values = {item['Tag']: [item['NumericValue']] for item in data_json['items'] 
                        if item['Tag'] in features_in_order}
    except KeyError as e:
        raise ValueError(f"Expected dict key: {str(e)}")

    data_df = pd.DataFrame(tags_values, index=[timestamp])

    try:
        data_df = data_df[features_in_order]
    except KeyError:
        missing_features = set(features_in_order) - set(data_df.columns)
        raise ValueError(f"Tag(s) missing in input: {','.join(missing_features)}")

    return data_df


def format_output(timestamps, scores, is_anomaly):
    '''
    Output format:
    {
        'DateTime': '2/3/2022 15:00:00',
        'score': 0.XX,
        'anomaly': 0/1
    }
    '''
    nrecords = len(timestamps)
    assert nrecords == len(scores) == len(is_anomaly) == 1

    output = {
        'DateTime': timestamps[0],
        'score': scores[0],
        'anomaly': int(is_anomaly[0])
    }

    return output