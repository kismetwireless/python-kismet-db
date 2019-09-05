ARG PY_VER=2.7
FROM python:${PY_VER}

RUN apt-get update && apt-get install -y tcpdump xmlstarlet

RUN pip install pytest pytest-coverage

COPY . /src/

WORKDIR /src/

RUN pip install -e .

RUN py.test --cov=kismetdb --cov-report=term-missing

###
# Test v4

# Test KML script
RUN kismet_log_to_kml --in=./tests/assets/testdata.kismet_4 --out=./out.kml > /dev/null
RUN cat ./out.kml | wc -l
RUN xmlstarlet val ./out.kml

# Test CSV script
RUN kismet_log_to_csv --in=./tests/assets/testdata.kismet_4 --table=devices --out=./devices.csv > /dev/null
RUN cat devices.csv | wc -l

RUN kismet_log_to_csv --in=./tests/assets/testdata.kismet_4 --table=packets --out=packets.csv > /dev/null
RUN cat packets.csv | wc -l

RUN kismet_log_to_csv --in=./tests/assets/testdata.kismet_4 --table=datasources --out=./datasources.csv > /dev/null
RUN cat datasources.csv | wc -l

RUN  kismet_log_to_csv --in=./tests/assets/testdata.kismet_4 --table=alerts --out=./alerts.csv > /dev/null
RUN cat alerts.csv | wc -l

# Test pcap script (single file)
RUN kismet_log_to_pcap --in=./tests/assets/testdata.kismet_4 --out=./out.pcap > /dev/null
RUN tcpdump -r ./out.pcap > /dev/null

# Test pcap script (multiple files)
RUN kismet_log_to_pcap --in=./tests/assets/testdata.kismet_4 --outtitle=./outpcap --limit-packets=1000  > /dev/null
RUN tcpdump -r ./out.pcap > /dev/null

RUN kismet_log_devices_to_json --in=./tests/assets/testdata.kismet_4 --out=./out.json
RUN cat ./out.json | wc -l

RUN kismet_log_devices_to_filebeat_json --in=./tests/assets/testdata.kismet_4 | wc -l


###
# Test v5

# Test KML script
RUN kismet_log_to_kml --in=./tests/assets/testdata.kismet_5 --out=./out.kml > /dev/null
RUN cat ./out.kml | wc -l
RUN xmlstarlet val ./out.kml

# Test CSV script
RUN kismet_log_to_csv --in=./tests/assets/testdata.kismet_5 --table=devices --out=./devices.csv > /dev/null
RUN cat devices.csv | wc -l

RUN kismet_log_to_csv --in=./tests/assets/testdata.kismet_5 --table=packets --out=packets.csv > /dev/null
RUN cat packets.csv | wc -l

RUN kismet_log_to_csv --in=./tests/assets/testdata.kismet_5 --table=datasources --out=./datasources.csv > /dev/null
RUN cat datasources.csv | wc -l

RUN  kismet_log_to_csv --in=./tests/assets/testdata.kismet_5 --table=alerts --out=./alerts.csv > /dev/null
RUN cat alerts.csv | wc -l

# Test pcap script
RUN kismet_log_to_pcap --in=./tests/assets/testdata.kismet_5 --out=./out.pcap > /dev/null
RUN tcpdump -r ./out.pcap > /dev/null

RUN kismet_log_devices_to_json --in=./tests/assets/testdata.kismet_5 --out=./out.json
RUN cat ./out.json | wc -l

RUN kismet_log_devices_to_filebeat_json --in=./tests/assets/testdata.kismet_5 | wc -l


###### Flush it!
FROM ubuntu:18.04
