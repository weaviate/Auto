ARG BASE_IMAGE=substratusai/base:latest
FROM nvidia/cuda:12.2.0-devel-ubuntu22.04 as build

RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
    apt-get update && \
    apt-get -y --no-install-recommends install \
      python3 python3-pip python3-venv git build-essential gcc wget && \
    rm -rf /var/lib/apt/lists/*
# Ensures that the python and pip executables used
# in the image will be those from our virtualenv.
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install depencencies
RUN /venv/bin/python3 -m pip install --upgrade pip wheel packaging ninja papermill jupyterlab ipywidgets
COPY requirements.txt .
RUN /venv/bin/python3 -m pip install -r requirements.txt
RUN /venv/bin/python3 -m pip install flash-attn --no-build-isolation

FROM ${BASE_IMAGE}
ENV PATH="/venv/bin:$PATH"
COPY --from=build /venv /venv
COPY eval.ipynb .
COPY eval.py .