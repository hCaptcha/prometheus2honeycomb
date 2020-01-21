FROM python:3-alpine
WORKDIR /app

ENV PATH "$PATH:/app/bin"

RUN apk update \
    && apk add curl gcc musl-dev \
    && pip install --upgrade pipenv pip

COPY Pipfile* /app/
RUN pipenv install --deploy --system --dev

COPY . /app/
RUN /app/bin/get_prom2json


CMD ["python3", "prometheus2honeycomb.py"]
