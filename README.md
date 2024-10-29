# local data stack template

- dagster, dbt, duckdb
- pixi
- docker
- ruff, pyright, taplo, pytest
- cruft


## usage

Prerequisites: 

- an installation of cruft `pip install cruft jinja2-ospath`
- an installation of pixi https://pixi.sh/latest/#installation `curl -fsSL https://pixi.sh/install.sh | bash`
- text editor of choice such as vscode
- docker


```bash
pixi run tpl-init-cruft

# alternatively:
cruft create cruft create git@github.com:l-mds/local-data-stack.git

cd <<your project name>>
git init
git add .
git commit -m "initial commit"

pixi update
git commit -m "set dependencies"

git commit -m "reformatting"
pixi run fmt
```

Post install:

- update the secrets in the `.env` files by executing: `openssl rand -base64 32` and setting a suitable secret
- ensure the `.env.enc` can be created by following the instructions in [documentation/secops]