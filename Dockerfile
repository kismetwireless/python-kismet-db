ARG PY_VER=2.7
FROM python:${PY_VER}

RUN apt-get update && apt-get install -y tcpdump xmlstarlet

RUN pip install pytest pytest-coverage

COPY . /src/

WORKDIR /src/

RUN pip install -e .

RUN py.test --cov=kismetdb --cov-report=term-missing

# Test KML script
RUN kismet_log_to_kml --in=./tests/assets/testdata.kismet --out=./out.kml > /dev/null
RUN cat ./out.kml | wc -l
RUN xmlstarlet val ./out.kml

# Test CSV script
RUN kismet_log_to_csv --in=./tests/assets/testdata.kismet --table=devices --out=./devices.csv > /dev/null
RUN cat devices.csv | wc -l

RUN kismet_log_to_csv --in=./tests/assets/testdata.kismet --table=packets --out=packets.csv > /dev/null
RUN cat packets.csv | wc -l

RUN kismet_log_to_csv --in=./tests/assets/testdata.kismet --table=datasources --out=./datasources.csv > /dev/null
RUN cat datasources.csv | wc -l

RUN  kismet_log_to_csv --in=./tests/assets/testdata.kismet --table=alerts --out=./alerts.csv > /dev/null
RUN cat alerts.csv | wc -l

# Test pcap script
RUN kismet_log_to_pcap --in=./tests/assets/testdata.kismet --out=./out.pcap > /dev/null
RUN tcpdump -r ./out.pcap > /dev/null

# Test devices to json script
RUN which kismet_log_devices_to_json

RUN kismet_log_devices_to_json --in=./tests/assets/testdata.kismet --out=./out.json

###### Flush it!
FROM ubuntu:18.04
