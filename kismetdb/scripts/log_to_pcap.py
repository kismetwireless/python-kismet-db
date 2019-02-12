"""Write packet captures from Kismet DB to pcap file."""
import argparse
import struct
import sys

import kismetdb


def main():

    # Write a raw pcap file header
    def write_pcap_header(f, dlt):
        hdr = struct.pack("IHHiIII",
                          0xa1b2c3d4,  # magic
                          2, 4,  # version
                          0,  # offset
                          0,  # sigfigs
                          8192,  # max packet len
                          int(dlt)  # packet type
                          )

        f.write(hdr)

    # Write a specific frame
    def write_pcap_packet(f, timeval_s, timeval_us, packet_bytes):
        packet_len = len(packet_bytes)
        pkt = struct.pack("IIII",
                          timeval_s,
                          timeval_us,
                          packet_len,
                          packet_len
                          )
        f.write(pkt)
        f.write(packet_bytes)

    parser = argparse.ArgumentParser(description=("Kismet to Pcap "
                                                  "Log Converter"))
    parser.add_argument("--in", action="store", dest="infile",
                        help="Input (.kismet) file")
    parser.add_argument("--out", action="store", dest="outfile",
                        help="Output filename (when exporting all packets)")
    parser.add_argument("--outtitle", action="store", dest="outtitle",
                        help="Output title (when limiting packets per file)")
    parser.add_argument("--limit-packets", action="store", dest="limitpackets",
                        help=("Generate multiple pcap files, limiting the "
                              "number of packets per file"))
    parser.add_argument("--source-uuid", action="append", dest="uuid",
                        help=("Limit packets to a specific data source "
                              "(multiple --source-uuid options will match "
                              "multiple datasources)"))
    parser.add_argument("--start-time", action="store", dest="starttime",
                        help="Only convert packets recorded after start-time")
    parser.add_argument("--end-time", action="store", dest="endtime",
                        help="Only convert packets recorded before end-time")
    parser.add_argument("--silent", action="store", dest="silent",
                        help="Silent operation (no status output)")
    parser.add_argument("--min-signal", action="store", dest="minsignal",
                        help=("Only convert packets with a signal greater "
                              "than min-signal"))
    parser.add_argument("--device-key", action="append", dest="devicekey",
                        help=("Only convert packets which are linked to the "
                              "specified device key (multiple --device-key "
                              "options will match multiple devices)"))
    results = parser.parse_args()

    log_to_single = True

    if results.infile is None:
        print("Expected --in [file]")
        sys.exit(1)

    if results.limitpackets is not None and results.outtitle is None:
        print("Expected --outtitle when using --limit-packets")
        sys.exit(1)
    elif results.limitpackets is None and results.outfile is None:
        print("Expected --out [file]")
        sys.exit(1)
    elif results.limitpackets and results.outtitle:
        print(("Limiting to {} packets per file in "
               "{}-X.pcap").format(results.limitpackets, results.outtitle))

    query_args = {"dlt_gt": 0}

    if results.uuid is not None:
        query_args["datasource"] = results.uuid

    if results.starttime:
        query_args["ts_sec_gt"] = results.starttime

    if results.endtime:
        query_args["ts_sec_lt"] = results.endtime

    if results.minsignal:
        query_args["min_signal"] = results.minsignal

    logf = None
    lognum = 0

    packet_store = kismetdb.Packets(results.infile)

    npackets = 0
    file_mode = "wb"
    for result in packet_store.yield_all(**query_args):
        if logf is None:
            if results.silent is None:
                print("DLT {} for all packets".format(query_args["dlt_gt"]))
            if log_to_single:
                if results.silent is None:
                    print("Logging to {}".format(results.outfile))
                logf = open(results.outfile, file_mode)
                write_pcap_header(logf, result["dlt"])
            else:
                if results.silent is None:
                    print("Logging to {}-{}.pcap".format(results.outtitle,
                                                         lognum))
                logf = open("{}-{}.pcap".format(results.outtitle,
                                                lognum), file_mode)
                lognum = lognum + 1
                print("Writing PCAP header with DLT {}".format(result["dlt"]))
                write_pcap_header(logf, result["dlt"])

        write_pcap_packet(logf, int(result["ts_sec"]), int(result["ts_usec"]),
                          result["packet"])
        npackets = npackets + 1

        if not log_to_single:
            if npackets % results.limitpackets == 0:
                logf.close()
                logf = None
        elif results.silent is None:
            if npackets % 1000 == 0:
                print("Converted {} packets...".format(npackets))

    if results.silent is None:
        print("Done! Converted {} packets.".format(npackets))


if __name__ == "__main__":
    main()
