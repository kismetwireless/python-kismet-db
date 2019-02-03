"""Upload Kismet DB to Wigle."""

import argparse
import csv
import datetime
import json
import os
import pprint
import requests
from requests.auth import HTTPBasicAuth
import sys
import socket
import tempfile


import kismetdb


def main():
    parser = argparse.ArgumentParser(description="Kismet to CSV Log Converter")
    parser.add_argument("--in", action="store", dest="infile",
                        help="Input (.kismet) file")
    parser.add_argument("--wigle-user", action="store", dest="user",
                        required=True, help="Wigle API user name.")
    parser.add_argument("--wigle-token", action="store", dest="token",
                        required=True, help="API token for Wigle upload.")
    parser.add_argument("--start-time", action="store", dest="starting",
                        help="Timestamp for first observation of network.")
    parser.add_argument("--upload-name", action="store", dest="upload_name",
                        help="Name for Wigle upload. Default: host__date.csv")
    parser.add_argument("--donate", dest="donate", action="store_true",
                        help="Donate data?")
    parser.set_defaults(donate=False)

    results = parser.parse_args()
    replacements = {}

    if results.infile is None:
        print("Expected --in [file]")
        sys.exit(1)

    if not os.path.isfile(results.infile):
        print("Could not find input file '{}'".format(results.infile))
        sys.exit(1)

    # Set the upload name
    if results.upload_name is None:
        hostname = socket.gethostname()
        tstamp = datetime.datetime.now().isoformat().split(".")[0].replace(":","-")  # NOQA
        results.upload_name = "{}-{}.csv".format(hostname, tstamp)

    # Set up the drop dir for the CSV file
    temp_dir = tempfile.mkdtemp()
    csv_file_path = os.path.join(temp_dir, "out.csv")
    print("Writing CSV to {}".format(csv_file_path))

    # Create the CSV
    generate_csv(results.infile, csv_file_path, results.starting)

    # Upload the CSV
    upload_file(results.upload_name, csv_file_path, results.user,
                results.token, results.donate)


def upload_file(upload_name, csv_file, user, token, donate):
    """Upload a CSV file to Wigle.

    Args:
        upload_name (str): Name for upload.
        csv_file (str): Absolute path to CSV file.
        user (str): Username for API.
        token (str): API token for Wigle.
        donate (bool): Donate data.

    Returns:
        None

    """
    url = "https://api.wigle.net/api/v2/file/upload"
    data = {"donate": str(donate).lower()}
    files = {"file": (upload_name, open(csv_file, "rb"), "text/csv")}
    response = requests.post(url, data=data, files=files,
                             auth=HTTPBasicAuth(user, token))
    pprint.pprint(response.text)


# files = { 'file': ('13.jpg', open('/Users/dave/Downloads/13.jpg', 'rb'), 'image/jpeg')}
# data = dict(name='barca', country='spain')
# response = requests.post(url, files=files, data=data)

def generate_csv(infile, file_path, start_time):
    """Write the upload CSV to ``file_path``.

    Args:
        infile (str): Absolute path to Kismet DB file.
        file_path (str): Absolute path to CSV file. If the file already exists,
            it will be overwritten. The directory path must exist!
        field_mapping (dict): Each key is a field in the output CSV, and
            the value is the field in the source dataset.
    Raises:
        ValueError: ValueError is raised if the directory for ``file_path``
            does not exist.
    Returns:
        None
    """

    table_abstraction = kismetdb.Devices(infile)
    bulk_data_field = table_abstraction.bulk_data_field
    kwargs = {"type": "Wi-Fi AP"}
    if start_time:
        kwargs["first_time_gt"] = start_time
    # column_names = ["MAC", "SSID", "AuthMode", "FirstSeen", "Channel",
    #                 "RSSI", "CurrentLatitude", "CurrentLongitude",
    #                 "AltitudeMeters", "AccuracyMeters", "Type"]
    column_names = ["BSSID", "SSID", "LAT", "LON", "ALT", "SPEED", "FIX",
                    "QUALITY", "POWER", "NOISE", "TIME"]
    with open(file_path, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, extrasaction="ignore",
                                fieldnames=column_names)
        nrows = 0
        writer.writeheader()
        for row in table_abstraction.yield_all(**kwargs):
            rows_translated = translate_row(json.loads(row[bulk_data_field]))
            for row_translated in rows_translated:
                writer.writerow(row_translated)
                nrows = nrows + 1
                if nrows % 1000 == 0:
                    print("Wrote {} rows".format(nrows))


def translate_row(row):
    """Return a row with translated keys, ready for Wigle."""
    rows_translated = []
    # for _k, ssid in row["dot11.device"]["dot11.device.advertised_ssid_map"].items():
    #    device = {"MAC": row["kismet.device.base.macaddr"],
    #              "SSID": ssid["dot11.advertisedssid.ssid"],
    #              "AuthMode": row["kismet.device.base.crypt"],
    #              "FirstSeen": kismetdb.Utility.timestamp_to_iso(row["kismet.device.base.first_time"]),  # NOQA
    #              "Channel": row["kismet.device.base.channel"],
    #              "RSSI": row["kismet.device.base.signal"]["kismet.common.signal.max_signal"],  # NOQA
    #              "CurrentLatitude": row["kismet.device.base.location"]["kismet.common.location.avg_loc"]["kismet.common.location.lat"],  # NOQA
    #              "CurrentLongitude": row["kismet.device.base.location"]["kismet.common.location.avg_loc"]["kismet.common.location.lon"],  # NOQA
    #              "AltitudeMeters": row["kismet.device.base.location"]["kismet.common.location.avg_loc"]["kismet.common.location.alt"],  # NOQA
    #              "AccuracyMeters": "1",
    #              "Type": "WIFI"}
    #    rows_translated.append(device.copy())
    for _k, ssid in row["dot11.device"]["dot11.device.advertised_ssid_map"].items():
        device = {"BSSID": row["dot11.device"]["dot11.device.last_bssid"],
                  "SSID": ssid["dot11.advertisedssid.ssid"],
                  "TIME":  kismetdb.Utility.timestamp_to_iso(row["kismet.device.base.last_time"]),
                  "LAT": row["kismet.device.base.location"]["kismet.common.location.avg_loc"]["kismet.common.location.lat"],
                  "LON": row["kismet.device.base.location"]["kismet.common.location.avg_loc"]["kismet.common.location.lon"],
                  "ALT": row["kismet.device.base.location"]["kismet.common.location.avg_loc"]["kismet.common.location.alt"],
                  "SPEED": row["kismet.device.base.location"]["kismet.common.location.avg_loc"]["kismet.common.location.speed"],
                  "FIX": row["kismet.device.base.location"]["kismet.common.location.avg_loc"]["kismet.common.location.fix"],
                  "QUALITY": "",
                  "POWER": row["kismet.device.base.signal"]["kismet.common.signal.max_signal"],
                  "NOISE": row["kismet.device.base.signal"]["kismet.common.signal.max_noise"]}
        rows_translated.append(device.copy())
    return rows_translated


if __name__ == "__main__":
    main()
