import os


def get_dagster_deployment_environment(
    deployment_key: str = "DAGSTER_DEPLOYMENT", default_value="dev"
):
    return os.environ.get(deployment_key, default_value)
