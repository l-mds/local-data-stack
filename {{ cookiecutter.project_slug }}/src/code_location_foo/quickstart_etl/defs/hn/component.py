import dagster as dg


class HnComponent(dg.Component, dg.Model, dg.Resolvable):
    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        return dg.Definitions()


@dg.component_instance
def load(context: dg.ComponentLoadContext) -> HnComponent:
    return HnComponent()
