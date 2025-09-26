from dagster import asset

@asset(
    compute_kind="python",
    group_name="logistics",
    deps=["my_first_dbt_model"],
)
def logistics_example():
    return 1
