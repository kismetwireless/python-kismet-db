ARG PY_VER=2.7
FROM python:${PY_VER}

RUN pip install pytest pytest-coverage

COPY . /src/

WORKDIR /src/

RUN pip install -e .

RUN py.test --cov=kismetdb --cov-report=term-missing

# Install simplekml for tests.
RUN pip install simplekml

# Test KML script
RUN kismet_log_to_kml --in=./tests/assets/testdata.kismet --out=./out.kml

# Test CSV script
RUN kismet_log_to_csv --in=./tests/assets/testdata.kismet --table=devices --out=./devices.csv

RUN kismet_log_to_csv --in=./tests/assets/testdata.kismet --table=packets --out=packets.csv

RUN kismet_log_to_csv --in=./tests/assets/testdata.kismet --table=datasources --out=./datasources.csv

RUN  kismet_log_to_csv --in=./tests/assets/testdata.kismet --table=alerts --out=./alerts.csv

# Test pcap script
RUN kismet_log_to_pcap --in=./tests/assets/testdata.kismet --out=./out.pcap

# Test devices to json script
RUN which kismet_log_devices_to_json

RUN kismet_log_devices_to_json --in=./tests/assets/testdata.kismet --out=./out.json
