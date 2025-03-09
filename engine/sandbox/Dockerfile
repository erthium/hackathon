FROM python:3.12-alpine

WORKDIR /sandbox

ARG TEMPLATE_NAME=/none/selected/so/far

# https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ../templates/${TEMPLATE_NAME} ${TEMPLATE_NAME}
COPY ../templates/*.py .
COPY repo repo

CMD python3 tempalte_runner.py
