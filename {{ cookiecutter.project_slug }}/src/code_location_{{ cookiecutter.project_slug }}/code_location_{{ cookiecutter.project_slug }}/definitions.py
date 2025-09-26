# ruff: noqa: E402
import warnings

import dagster as dg
from dagster._utils import warnings as dagster_warnings

warnings.filterwarnings("ignore", category=dagster_warnings.BetaWarning)
warnings.filterwarnings("ignore", category=dagster_warnings.PreviewWarning)
from pathlib import Path

@dg.definitions
def defs():
    root_dir = __file__
    base = dg.load_from_defs_folder(path_within_project=Path(root_dir).parent.parent)

    materializable = [a for a in base.assets if isinstance(a, dg.AssetsDefinition)]  # type: ignore
    passthrough = [
        a
        for a in base.assets  # type: ignore
        if not isinstance(a, dg.AssetsDefinition)
    ]  # SourceAsset

    with_refs = dg.with_source_code_references(materializable)

    linked = dg.link_code_references_to_git(
        assets_defs=with_refs,
        git_url="https://github.com/{{ cookiecutter.organization }}/{{ cookiecutter.project_slug }}/",
        git_branch="main",
        file_path_mapping=dg.AnchorBasedFilePathMapping(
            local_file_anchor=Path(root_dir).parent,
            file_anchor_path_in_repository="src/code_location_{{ cookiecutter.project_slug }}",
        ),
    )

    return dg.Definitions(
        assets=[*linked, *passthrough],
        jobs=base.jobs,
        schedules=base.schedules,
        sensors=base.sensors,
        resources=base.resources,
        asset_checks=base.asset_checks,
    )
