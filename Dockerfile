ARG PY_VER=2.7
FROM python:${PY_VER}

RUN pip install pytest pytest-coverage

COPY . /src/

WORKDIR /src/

RUN pip install -e .

RUN py.test --cov=kismetdb --cov-report=term-missing
