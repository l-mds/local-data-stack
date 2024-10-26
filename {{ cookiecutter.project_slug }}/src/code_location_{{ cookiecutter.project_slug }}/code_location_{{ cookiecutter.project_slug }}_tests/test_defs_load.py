from code_location_{{ cookiecutter.project_slug }} import defs
from dagster import Definitions


# @pytest.mark.filterwarnings("ignore::dagster.ExperimentalWarning")
def test_project_loads():
    # will raise errors if the project can't load
    # similar to loading a failing project in dagit
    # prevents fatal error in dagit
    # implied_repo = defs.get_repository_def()
    # implied_repo.load_all_definitions()
    Definitions.validate_loadable(defs)
