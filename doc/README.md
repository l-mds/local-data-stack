# How to maintain this template

## dependency updates

- use the lockfile to ship only validated working dependencies
- ensure that the lockfile is modified to reference the template variables like:

````
code_location_{{ cookiecutter.project_slug_pixi }}:
code_location_{{ cookiecutter.project_slug }}
```

I.e. replace occurences like:

```
# raw:
- pypi: ./src/code_location_local_data_stack

# replaced:
- pypi: ./src/code_location_{{ cookiecutter.project_slug }}


# raw:
codelocation-local-data-stack:

# replaced:
code_location_{{ cookiecutter.project_slug_pixi }}:
```

To validate dependencies (from the branch/PR) execute:

```bash
# create from the branch
cruft create --checkout <<new-branch>> git@github.com:l-mds/local-data-stack.git


# update from the branch
cruft update --checkout <<<new-branch>> --skip-apply-ask --refresh-private-variables
```