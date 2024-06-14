FROM python:3.12

RUN mkdir /marketplace

WORKDIR /marketplace

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \
    poetry config virtualenvs.create false

RUN poetry install

COPY .. .

