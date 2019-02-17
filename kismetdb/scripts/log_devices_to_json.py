"""Simple dumper to extract kismet records and export them as a json array."""

import argparse
import json
import os
import sys

import kismetdb


def main():
    parser = argparse.ArgumentParser(description="Kismet devices to json")
    parser.add_argument("--in", action="store", dest="infile",
                        help="Input (.kismet) file")
    parser.add_argument("--out", action="store", dest="outfile",
                        help=("Output filename (optional). If omitted, logs "
                              "multi-line and indented (human-readable) "
                              "to stdout."))
    parser.add_argument("--start-time", action="store", dest="starttime",
                        help="Only list devices seen after given time")
    parser.add_argument("--min-signal", action="store", dest="minsignal",
                        help=("Only list devices with a best signal higher "
                              "than min-signal"))

    results = parser.parse_args()
    query_args = {}

    if results.infile is None:
        print("Expected --in [file]")
        sys.exit(1)

    if not os.path.isfile(results.infile):
        print("Could not find input file \"{}\"".format(results.infile))
        sys.exit(1)

    if results.starttime:
        query_args["first_time_gt"] = results.starttime

    if results.minsignal:
        query_args["strongest_signal_gt"] = results.minsignal
    logf = None

    devices_abstraction = kismetdb.Devices(results.infile)

    devs = [row["device"] for row in devices_abstraction.get_all(**query_args)]

    if results.outfile:
        logf = open(results.outfile, "w")
        logf.write(json.dumps(devs, sort_keys=True, indent=4,
                              separators=(",", ": ")))
    else:
        print(json.dumps(devs, sort_keys=True, indent=4,
                         separators=(",", ": ")))


if __name__ == "__main__":
    main()
