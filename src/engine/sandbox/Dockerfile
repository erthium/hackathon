FROM python:3.12-alpine

WORKDIR /repo

# https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./templates/rpg/requirements.txt rpg/requirements.txt

RUN pip install -r rpg/requirements.txt

COPY ./templates/rpg rpg

CMD python3 rpg/libs/test_runner.py