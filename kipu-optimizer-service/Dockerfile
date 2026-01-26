FROM registry.gitlab.com/planqk-foss/planqk-python-template:latest

COPY . ${USER_CODE_DIR}

RUN cp ${USER_CODE_DIR}/.python-version /.python-version || true
RUN uv venv
RUN uv sync --frozen
RUN uv pip install -r ${USER_CODE_DIR}/requirements.txt
