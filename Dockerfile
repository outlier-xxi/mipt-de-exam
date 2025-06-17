# Easier to troubleshoot than python-...
FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PGTZ=UTC

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  python3-pip \
  && rm -rf /var/lib/apt/lists/*

# Download the latest installer
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
# UV_LINK_MODE=copy       Silences warnings about not being able to use hard links
#                         since the cache and sync target are on separate file systems.
ENV UV_LINK_MODE=copy

RUN  mkdir -p           /app
COPY ./pyproject.toml   /app
COPY ./uv.lock          /app
WORKDIR                 /app

# -system               Install python into the system.
# --compile-bytecode    Do compile python bytecode.
# -e                    Installs the current directory as an editable
#                       package, meaning changes to the source code will
#                       immediately affect the installed package.
RUN uv -v pip install --system --compile-bytecode -e . --break-system-packages

ENV PYTHONPATH="${PYTHONPATH}:/app"

COPY ./src/             /app/src

VOLUME [ "/hdd" ]
