import sys

#TODO: to be remove
AWS_TEST_PATH = "s3://wagon-public-datasets/taxi-fare-test.csv"

class Config(object):
    def __init__(self):
        """
        Configuration file for GCP and MLFlow, Google Bucket, ...
        """
        self.config = {
            ## global project metadata
            'PROJECT_NAME': 'taxi_fare_ui_image',
            'PROJECT_VER': 'v1',

            ## google GCS configuration
            'PROJECT_ID': 'le-wagon-bootcamp-348503',
            # from https://cloud.google.com/storage/docs/locations#available_locations
            'REGION': 'asia-east2',
            'JOB_NAME': 'taxi_fare_training_pipeline',

            ## google bucket configuration
            'BUCKET_NAME': 'le-wagon-bootcamp-850-loic',
            'BUCKET_TRAINING_FOLDER': 'trainings',
            'BUCKET_MODELS_FOLDER': 'models',
            'BUCKET_TRAIN_DATA_PATH': 'data/train_1k.csv',
            'BUCKET_TEST_DATA_PATH': 'data/test.csv',

            ## MLFlow connfiguration
            'MLFLOW_URI': "https://mlflow.lewagon.ai/",
            'MLFLOW_EXPERIMENT_NAME': "[CN][SZ][850][Loic] TaxiFaireModel - v1.0",
        }

    def get_config(self, key=None):
        if key == None:
            return self.config
        else:
            return self.config.get(key, "config not found...")


if __name__ == "__main__":
    config = Config()
    args = sys.argv[1:]

    if len(args) == 1:
        print(config.get_config(args[0]))
    elif len(args) > 1:
        print('Error: too much arguments...')
        exit(1)
    else:
        print(config.get_config())
