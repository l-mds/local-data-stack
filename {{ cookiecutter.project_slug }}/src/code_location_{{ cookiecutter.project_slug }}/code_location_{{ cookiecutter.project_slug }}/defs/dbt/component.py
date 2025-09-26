import re
import dagster as dg
from .resources import get_resources_for_deployment

class DbtMinimalComponent(dg.Component, dg.Model, dg.Resolvable):
    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        return dg.Definitions(resources=get_resources_for_deployment())


@dg.component_instance
def load(context: dg.ComponentLoadContext) -> DbtMinimalComponent:
    return DbtMinimalComponent()
