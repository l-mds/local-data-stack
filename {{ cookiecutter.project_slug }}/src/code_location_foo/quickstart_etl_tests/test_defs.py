import dagster as dg
from quickstart_etl import defs


def test_def_can_load():
    actual_defs = defs()
    dg.Definitions.validate_loadable(actual_defs)
