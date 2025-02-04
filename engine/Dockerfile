FROM docker:27-dind

# Take the ENGINE_PORT arg passed from compose.yaml,
# and set the environment variable to use in CMD
ARG ENGINE_PORT
ENV ENGINE_PORT=$ENGINE_PORT

WORKDIR /engine

# Install python and pip (default version is 3.12.8 in alpine 3.21)
RUN apk add --no-cache python3 py3-pip

# Set up virtual environment
# https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements.txt and install the requirements
COPY ./engine/requirements.txt .
RUN pip install -r requirements.txt

# Copy the templates into the sandbox folder
COPY ./templates ./sandbox/templates

# https://www.reddit.com/r/docker/comments/1chhie6/whats_up_with_the_dockerfiles_that_use_copy_twice/
COPY ./engine .

EXPOSE $ENGINE_PORT

# dockerd-entrypoint.sh & -> Run dockerd in background (unless, docker won't work)
# Then run the engine
CMD dockerd-entrypoint.sh & \
    fastapi \
    run \
    --host 0.0.0.0 \
    --port $ENGINE_PORT
