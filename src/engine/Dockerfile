FROM python:3.12-alpine

ARG ENGINE_PORT
ENV ENGINE_PORT=$ENGINE_PORT

WORKDIR /engine

COPY requirements.txt .

RUN apk add --no-cache gcc musl-dev linux-headers

# https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt

# https://www.reddit.com/r/docker/comments/1chhie6/whats_up_with_the_dockerfiles_that_use_copy_twice/
COPY . .

EXPOSE $ENGINE_PORT

CMD fastapi \
    dev \
    --host 0.0.0.0 \
    --port $ENGINE_PORT
