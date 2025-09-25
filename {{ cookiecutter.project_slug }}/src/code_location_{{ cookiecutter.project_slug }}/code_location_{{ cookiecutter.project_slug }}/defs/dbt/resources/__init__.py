from pathlib import Path

from dagster import file_relative_path, get_dagster_logger
from dagster_dbt import DbtCliResource, DbtProject
from shared_library.orchestration.resources.utils import (
    get_dagster_deployment_environment,
)

from .duckdb_path import DuckDBPathResource

DBT_PROJECT_DIR = file_relative_path(__file__, "../../code_location_{{ cookiecutter.project_slug }}_dbt")


def get_dbt_project(target: str, DBT_PROJECT_DIR: str):
    # dbt_project_path = Path(__file__).parent.parent.joinpath("dbt_project")
    dbt_project = DbtProject(
        project_dir=DBT_PROJECT_DIR,
        # must sit externally i.e. on s3
        # state_path="target/slim_ci",
        target=target,
    )
    dbt_project.prepare_if_dev()
    return dbt_project


dbt_resource_dev = DbtCliResource(
    project_dir=get_dbt_project(target="dev", DBT_PROJECT_DIR=DBT_PROJECT_DIR),
    global_config_flags=["--no-use-colors"],
    target="dev",
)

dbt_resource_prod = DbtCliResource(
    project_dir=get_dbt_project(target="prod", DBT_PROJECT_DIR=DBT_PROJECT_DIR),
    global_config_flags=["--no-use-colors"],
    target="prod",
)

RESOURCES_LOCAL = {
    "dbt": dbt_resource_dev,
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
    "dbt": dbt_resource_prod,
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
