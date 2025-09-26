import dagster as dg

@dg.asset(
    compute_kind="python",
    group_name="logistics",
    deps=[dg.AssetKey(["analytics_database_dev", "bar_dev", "my_first_dbt_model_v1"])],
)
def logistics_example():
    return 1
