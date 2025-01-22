FROM python:3.12-alpine
WORKDIR /backend
RUN apk add --no-cache gcc musl-dev linux-headers
EXPOSE 8000
COPY ./backend/requirements.txt .

# https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# https://stackoverflow.com/questions/78093369/installing-psycopg-in-alpine-docker-image
RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev && \
    apk add postgresql-dev

RUN pip install -r requirements.txt
COPY ./common ./common
COPY ./backend .
CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]
