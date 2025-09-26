import dagster as dg

daily_refresh_schedule = dg.ScheduleDefinition(
    job=dg.define_asset_job(name="all_assets_job"), cron_schedule="0 0 * * *"
)


@dg.op
def foo_op():
    return 5


@dg.graph_asset
def my_asset():
    return foo_op()



class HnComponent(dg.Component, dg.Model, dg.Resolvable):
    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        return dg.Definitions(jobs=[daily_refresh_schedule], assets=[my_asset()])


@dg.component_instance
def load(context: dg.ComponentLoadContext) -> HnComponent:
    return HnComponent()
