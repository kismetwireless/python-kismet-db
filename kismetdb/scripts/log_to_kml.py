"""Write device records from Kismet DB to KML."""

import argparse
import json
import pprint
import sys
import re

import simplekml

import kismetdb


def main():
    parser = argparse.ArgumentParser(description="Kismet to KML Log Converter")
    parser.add_argument("--in", action="store", dest="infile",
                        help="Input (.kismet) file")
    parser.add_argument("--out", action="store", dest="outfile",
                        help="Output filename (optional)")
    parser.add_argument("--start-time", action="store", dest="starttime",
                        help="Only list devices seen after given time")
    parser.add_argument("--min-signal", action="store", dest="minsignal",
                        help=("Only list devices with a best signal higher "
                              "than min-signal"))
    parser.add_argument("--strongest-point", action="store_true",
                        dest="strongest", default=False,
                        help="Plot points based on strongest signal")
    parser.add_argument("--title", action="store", dest="title",
                        default="Kismet", help="Title embedded in KML file")
    parser.add_argument("--ssid", action="store", dest="ssid",
                        help=("Only plot networks which match the SSID "
                              "(or SSID regex)"))

    results = parser.parse_args()

    query_args = {}

    if results.infile is None:
        print("Expected --in [file]")
        sys.exit(1)

    if results.starttime:
        query_args["first_time_gt"] = results.starttime

    if results.minsignal:
        query_args["strongest_signal_gt"] = results.minsignal

    kml = simplekml.Kml()

    kml.document.name = results.title

    num_plotted = 0

    devices = kismetdb.Devices(results.infile)

    for device in devices.yield_all(**query_args):
        try:
            dev = json.loads(device["device"])
            # Check for the SSID if we"re doing that; allow it to trip
            # a KeyError and jump out of processing this device
            if results.ssid is not None:
                matched = False
                for s in dev["dot11.device"]["dot11.device.advertised_ssid_map"]:  # NOQA
                    adv_ssid = dev["dot11.device"]["dot11.device.advertised_ssid_map"][s]["dot11.advertisedssid.ssid"]  # NOQA
                    if re.match(results.ssid, adv_ssid):
                        matched = True
                        break

                if not matched:
                    print("Not a match on SSID!")
                    continue

            loc = None

            if results.strongest:
                loc = dev["kismet.device.base.signal"]["kismet.common.signal.peak_loc"]  # NOQA
            else:
                loc = dev["kismet.device.base.location"]["kismet.common.location.avg_loc"]  # NOQA

            if loc == 0:
                print("Null island...")
                continue

            mac = dev["kismet.device.base.macaddr"]

            title = ""

            if "kismet.device.base.name" in dev:
                title = dev["kismet.device.base.name"]

            if title == "":
                if "dot11.device" in dev:
                    if "dot11.device.last_beaconed_ssid" in dev["dot11.device"]:  # NOQA
                        title = dev["dot11.device"]["dot11.device.last_beaconed_ssid"]  # NOQA

            if title == "":
                title = mac

            kml.newpoint(name=title,
                         coords=[(loc["kismet.common.location.lon"],
                                  loc["kismet.common.location.lat"],
                                  loc["kismet.common.location.alt"])])

            num_plotted = num_plotted + 1
        except TypeError:
            continue
        except KeyError:
            continue
    kml.save(results.outfile)
    print("Exported {} devices to {}".format(num_plotted, results.outfile))


if __name__ == "__main__":
    main()
