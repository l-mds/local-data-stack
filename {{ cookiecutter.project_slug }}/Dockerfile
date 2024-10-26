# syntax=docker/dockerfile:1.10.0

# for CUDA support ensure docker is nvidia-docker enabled!
FROM ghcr.io/prefix-dev/pixi:0.34.0-bookworm AS builder_base

FROM builder_base AS build
ENV DAGSTER_HOME=/opt/dagster/dagster_home/
WORKDIR /opt/dagster/dagster_home/
WORKDIR /app
COPY pixi.toml .
COPY pixi.lock .

RUN pixi install --frozen -e dagster-webserver
RUN pixi shell-hook --frozen -e dagster-webserver -s bash > /shell-hook
RUN echo "#!/bin/bash" > /app/entrypoint_dagster-webserver.sh
RUN cat /shell-hook >> /app/entrypoint_dagster-webserver.sh
RUN echo 'exec "$@"' >> /app/entrypoint_dagster-webserver.sh

RUN pixi install --frozen -e dagster-daemon
RUN pixi shell-hook --frozen -e dagster-daemon -s bash > /shell-hook
RUN echo "#!/bin/bash" > /app/entrypoint_dagster-daemon.sh
RUN cat /shell-hook >> /app/entrypoint_dagster-daemon.sh
RUN echo 'exec "$@"' >> /app/entrypoint_dagster-daemon.sh

# TODO analyze if we can move this down / what to change to move this down to later for better copy
# sub package?
COPY src src

RUN pixi install -e codelocation-{{ cookiecutter.project_slug_pixi }} --locked
RUN pixi shell-hook -e codelocation-{{ cookiecutter.project_slug_pixi }} -s bash > /shell-hook
RUN echo "#!/bin/bash" > /app/entrypoint_codelocation-{{ cookiecutter.project_slug_pixi }}.sh
RUN cat /shell-hook >> /app/entrypoint_codelocation-{{ cookiecutter.project_slug_pixi }}.sh
RUN echo 'exec "$@"' >> /app/entrypoint_codelocation-{{ cookiecutter.project_slug_pixi }}.sh

RUN pixi install -e codelocation-foo --locked
RUN pixi shell-hook -e codelocation-foo -s bash > /shell-hook
RUN echo "#!/bin/bash" > /app/entrypoint_codelocation-foo.sh
RUN cat /shell-hook >> /app/entrypoint_codelocation-foo.sh
RUN echo 'exec "$@"' >> /app/entrypoint_codelocation-foo.sh

FROM debian:bookworm-slim AS dagster_basics

RUN apt-get update && \
    apt-get upgrade -y && \
    export DEBIAN_FRONTEND=noninteractive && apt-get install -y --no-install-recommends ca-certificates  && \
    rm -rf /var/lib/apt/lists/*

ENV DAGSTER_HOME=/opt/dagster/dagster_home/
WORKDIR /opt/dagster/dagster_home/
COPY dagster.yaml /opt/dagster/dagster_home/dagster.yaml
COPY workspace_docker.yaml /opt/dagster/dagster_home/workspace.yaml
WORKDIR /app
RUN groupadd -r dagster && useradd -m -r -g dagster dagster && \
    chown -R dagster:dagster $DAGSTER_HOME
ENTRYPOINT [ "/app/entrypoint.sh" ]


FROM dagster_basics AS dagster-webserver
EXPOSE 3000
WORKDIR /opt/dagster/dagster_home/
COPY --from=build /app/.pixi/envs/dagster-webserver /app/.pixi/envs/dagster-webserver
COPY --from=build --chmod=0755 /app/entrypoint_dagster-webserver.sh /app/entrypoint.sh
CMD ["dagster-webserver", "-h", "0.0.0.0", "--port", "3000", "-w", "/opt/dagster/dagster_home/workspace.yaml"]


FROM dagster_basics AS dagster-daemon
COPY --from=build /app/.pixi/envs/dagster-daemon /app/.pixi/envs/dagster-daemon
COPY --from=build --chmod=0755 /app/entrypoint_dagster-daemon.sh /app/entrypoint.sh
WORKDIR /opt/dagster/dagster_home/
CMD ["dagster-daemon", "run"]


FROM dagster_basics AS codelocation-foo
ENV DO_NOT_TRACK=1
COPY --from=build /app/.pixi/envs/codelocation-foo /app/.pixi/envs/codelocation-foo
COPY --from=build --chmod=0755 /app/entrypoint_codelocation-foo.sh /app/entrypoint.sh
COPY --from=build /app/src/code_location_foo /app/src/code_location_foo
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "--package-name", "quickstart_etl"]


FROM dagster_basics AS codelocation-{{ cookiecutter.project_slug_pixi }}
#RUN apt-get update && \
#    apt-get upgrade -y && \
#    export DEBIAN_FRONTEND=noninteractive && apt-get install -y --no-install-recommends osmctools osm2pgrouting wget vim  git osm2pgsql  && \
#    rm -rf /var/lib/apt/lists/*
ENV DO_NOT_TRACK=1
COPY --from=build /app/.pixi/envs/codelocation-{{ cookiecutter.project_slug_pixi }} /app/.pixi/envs/codelocation-{{ cookiecutter.project_slug_pixi }}
COPY --from=build --chmod=0755 /app/entrypoint_codelocation-{{ cookiecutter.project_slug_pixi }}.sh /app/entrypoint.sh
COPY --from=build /app/src/code_location_{{ cookiecutter.project_slug }} /app/src/code_location_{{ cookiecutter.project_slug }}
COPY --from=build /app/src/shared_library /app/src/shared_library
RUN cd src/code_location_{{ cookiecutter.project_slug }}/code_location_{{ cookiecutter.project_slug }}_dbt && /app/.pixi/envs/codelocation-{{ cookiecutter.project_slug_pixi }}/bin/dbt deps && /app/.pixi/envs/codelocation-{{ cookiecutter.project_slug_pixi }}/bin/dbt parse
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "--package-name", "code_location_{{ cookiecutter.project_slug }}"]


FROM builder_base AS all_codelocations_ci
ENV DAGSTER_HOME=/opt/dagster/dagster_home/
ENV DO_NOT_TRACK=1
WORKDIR /opt/dagster/dagster_home/
COPY ./dagster.yaml /opt/dagster/dagster_home/dagster.yaml
COPY ./workspace_docker.yaml /opt/dagster/dagster_home/workspace.yaml
WORKDIR /app
RUN groupadd -r dagster && useradd -m -r -g dagster dagster && \
    chown -R dagster:dagster $DAGSTER_HOME
ENTRYPOINT [ "/app/entrypoint.sh" ]

COPY yamllintconfig.yaml .
COPY pyproject.toml .
COPY taplo.toml .

COPY pixi.toml .
COPY pixi.lock .
COPY src src
RUN pixi install -e ci-validation --locked
RUN pixi shell-hook -e ci-validation -s bash > /shell-hook
RUN echo "#!/bin/bash" > /app/entrypoint.sh
RUN cat /shell-hook >> /app/entrypoint.sh
RUN echo 'exec "$@"' >> /app/entrypoint.sh
RUN chmod 0755 /app/entrypoint.sh

RUN cd src/{{ cookiecutter.project_slug_pixi }}/code_location_{{ cookiecutter.project_slug_pixi }}_dbt && /app/.pixi/envs/ci-validation/bin/dbt deps && /app/.pixi/envs/ci-validation/bin/dbt parse

# docker buildx build --target build --platform=linux/amd64 -t build:x86 -f Dockerfile .
# docker buildx build --target build -t build:arm -f Dockerfile .
# --progress=plain --no-cache
# docker buildx build --target build --platform=linux/amd64 -t foo:build --no-cache -f Dockerfile .
# docker buildx build --target build --platform=linux/amd64 -t foo:build -f Dockerfile .
# docker run --platform=linux/amd64 --rm -ti foo:build bash
# docker buildx build --target dagster-webserver --platform=linux/amd64 -t foo:server -f Dockerfile .
# docker run --rm -ti foo:server
# docker buildx build --target dagster-daemon --platform=linux/amd64 -t foo:daemon -f Dockerfile .
# docker run --rm -ti foo:daemon
# docker buildx build --target codelocation-{{ cookiecutter.project_slug }} --platform=linux/amd64 -t foo:codelocation-{{ cookiecutter.project_slug }} -f Dockerfile .
# docker buildx build --target codelocation-{{ cookiecutter.project_slug_pixi }} --platform=linux/amd64 -t bar:latest -f Dockerfile .
# docker buildx build --target codelocation-foo --platform=linux/amd64 -t foo:latest -f Dockerfile .
# docker buildx build --target codelocation-foo -t foo:latest -f Dockerfile .

# docker buildx build --target all_codelocations_ci --platform=linux/amd64 -t foo:all_codelocations_ci -f Dockerfile .
