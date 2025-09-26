from pathlib import Path

from dagster import file_relative_path, get_dagster_logger
from dagster_dbt import DbtCliResource, DbtProject
from shared_library.orchestration.resources.utils import (
    get_dagster_deployment_environment,
)
import os

from .duckdb_path import DuckDBPathResource

def get_env(deployment_key: str = "DAGSTER_DEPLOYMENT", default_value="dev"):
    if (
        (os.getenv("DAGSTER_CLOUD_IS_BRANCH_DEPLOYMENT", "") == "1")
        or (os.environ.get(deployment_key, default_value) == "dev")
        or (os.environ.get(deployment_key, default_value) == "BRANCH")
    ):
        return "dev"
    if (
        (os.getenv("DAGSTER_CLOUD_DEPLOYMENT_NAME", "") == "prod")
        or (os.environ.get(deployment_key, default_value) == "prod")
        or (os.environ.get(deployment_key, default_value) == "PROD")
    ):
        return "prod"
    raise ValueError(
        f"Unknown environment: {os.environ.get(deployment_key, default_value)}"
    )

DBT_PROJECT_DIR = file_relative_path(__file__, "../../code_location_{{ cookiecutter.project_slug }}_dbt")
dbt_project_path = Path(DBT_PROJECT_DIR)

dbt_project = DbtProject(
    project_dir=dbt_project_path,
    profiles_dir=dbt_project_path,
    target=get_env(),
)
dbt_project.prepare_if_dev()

RESOURCES_LOCAL = {
    "dbt": dbt_project,
    "ddb": DuckDBPathResource(
        file_path=str(
            Path(
                "/home/heiler/development/projects/{{ cookiecutter.project_slug }}/{{ cookiecutter.project_slug }}/prototyping/tech-exploration/dagster/z_state/analytics/analytics_database_dev.duckdb"
            )
            .expanduser()
            .resolve()
        )
    ),
}

RESOURCES_PROD = {
    "dbt": dbt_project,
    "ddb": DuckDBPathResource(
        file_path=str(
            Path(
                "./{{ cookiecutter.project_slug }}/code_location_{{ cookiecutter.project_slug }}_dbt/analytics_database_prod.duckdb"
            )
        )
    ),
}

resource_defs_by_deployment_name = {
    "dev": RESOURCES_LOCAL,
    "prod": RESOURCES_PROD,
}


def get_resources_for_deployment(log_env: bool = True):
    deployment_name = get_dagster_deployment_environment()
    if log_env:
        get_dagster_logger().info(f"Using deployment of: {deployment_name}")

    return resource_defs_by_deployment_name[deployment_name]
