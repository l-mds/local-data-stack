from dagster import ConfigurableResource


class DuckDBPathResource(ConfigurableResource):
    file_path: str
