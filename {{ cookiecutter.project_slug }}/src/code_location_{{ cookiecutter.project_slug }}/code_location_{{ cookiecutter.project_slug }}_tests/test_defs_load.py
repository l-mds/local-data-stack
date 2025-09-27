import dagster as dg
from code_location_{{ cookiecutter.project_slug }} import defs


def test_project_loads():
    # will raise errors if the project can't load
    # similar to loading a failing project in dagit
    # prevents fatal error in dagit
    # implied_repo = defs.get_repository_def()
    # implied_repo.load_all_definitions()
    actual_defs = defs()
    dg.Definitions.validate_loadable(actual_defs)
