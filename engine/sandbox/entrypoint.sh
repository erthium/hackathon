#!/bin/sh
set -e

echo "Running entrypoint with:"
echo "TEMPLATE_NAME=${TEMPLATE_NAME}"
echo "COMMAND_NAME=${COMMAND_NAME}"
echo "ARGS=${ARGS}"


# go to /sandbox/templates directory
cd /sandbox/templates || exit 1

GENERAL_REQUIREMENTS_FILE="/sandbox/templates/requirements.txt"
if [ -f "${GENERAL_REQUIREMENTS_FILE}" ]; then
  echo "Installing general requirements from ${GENERAL_REQUIREMENTS_FILE}"
  pip install -r "${GENERAL_REQUIREMENTS_FILE}"
else
  echo "No general requirements file found at ${GENERAL_REQUIREMENTS_FILE}"
fi

# Venv is in /opt/venv
if [ -d "/opt/venv" ]; then
  echo "Activating virtual environment at /opt/venv"
else
  echo "No virtual environment found at /opt/venv"
fi

python3 template_runner.py \
  --template-name "${TEMPLATE_NAME}" \
  --command-name "${COMMAND_NAME}" \
  --args "${ARGS}"
