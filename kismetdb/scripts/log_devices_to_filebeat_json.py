"""Simple dumper to extract kismet device records as a json for Filebeat."""

import argparse
import json
import os
import sys

import kismetdb


def main():
    parser = argparse.ArgumentParser(description="Kismet to Filebeat json")
    parser.add_argument("--in", action="store", dest="infile",
                        required=True, help="Input (.kismet) file")
    parser.add_argument("--out", action="store", dest="outfile",
                        help=("Output filename (optional) for appending. If "
                              "unspecified, each record will be printed to "
                              "stdout, one record per line, ideal for piping "
                              "into filebeat."))
    parser.add_argument("--start-time", action="store", dest="starttime",
                        help="Only list devices seen after given time")
    parser.add_argument("--min-signal", action="store", dest="minsignal",
                        help=("Only list devices with a best signal higher "
                              "than min-signal"))

    results = parser.parse_args()
    query_args = {}

    if not os.path.isfile(results.infile):
        print("Could not find input file \"{}\"".format(results.infile))
        sys.exit(1)

    if results.starttime:
        query_args["first_time_gt"] = results.starttime

    if results.minsignal:
        query_args["strongest_signal_gt"] = results.minsignal
    logf = None

    devices_abstraction = kismetdb.Devices(results.infile)

    for device in [json.loads(row["device"]) for row
                   in devices_abstraction.yield_all(**query_args)]:
        stripped_device = strip_old_empty_trees(device)
        if results.outfile:
            logf = open(results.outfile, "a")
            logf.write(json.dumps(stripped_device, sort_keys=True))
        else:
            print(json.dumps(stripped_device, sort_keys=True))


def strip_old_empty_trees(obj):
    """Remove specific fields if they're set to ``0``.

    Borrowed from ``log_tools/elk/kismet_log_to_elk.py`` in Kismet repo.
    """
    empty_trees = [
        "kismet.device.base.location",
        "kismet.device.base.datasize.rrd",
        "kismet.device.base.location_cloud",
        "kismet.device.base.packet.bin.250",
        "kismet.device.base.packet.bin.500",
        "kismet.device.base.packet.bin.1000",
        "kismet.device.base.packet.bin.1500",
        "kismet.device.base.packet.bin.jumbo",
        "kismet.common.signal.signal_rrd",
        "kismet.common.signal.peak_loc",
        "dot11.client.location",
        "client.location",
        "dot11.client.ipdata",
        "dot11.advertisedssid.location",
        "dot11.probedssid.location",
        "kismet.common.seenby.signal"
        ]
    try:
        for k in obj.keys():
            if k in empty_trees and obj[k] == 0:
                obj.pop(k)
            else:
                obj[k] = strip_old_empty_trees(obj[k])
            return obj
    except AttributeError:
        return obj


if __name__ == "__main__":
    main()
