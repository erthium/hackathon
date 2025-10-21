FROM python:3.12-alpine

WORKDIR /sandbox

ARG TEMPLATE_NAME="none/selected/so/far"
ARG COMMAND_NAME="none/selected/so/far"
ARG ARGS="none/selected/so/far"

ENV TEMPLATE_NAME=${TEMPLATE_NAME}
ENV COMMAND_NAME=${COMMAND_NAME}
ENV ARGS=${ARGS}

# https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./templates ./templates
COPY ./sandbox/repo ./repo

RUN apk add --no-cache tree && tree /sandbox

COPY sandbox/entrypoint.sh ./entrypoint.sh
CMD ["sh", "./entrypoint.sh"]
