"""Write packet captures from Kismet DB to pcap file."""
import argparse
import struct
import sys

import kismetdb


def write_pcap_header(file_obj, dlt):
    """Write a raw pcap file header."""
    hdr = struct.pack("IHHiIII",
                      0xa1b2c3d4,  # magic
                      2, 4,  # version
                      0,  # offset
                      0,  # sigfigs
                      8192,  # max packet len
                      int(dlt)  # packet type
                      )

    file_obj.write(hdr)


def write_pcap_packet(file_obj, timeval_s, timeval_us, packet_bytes):
    """Write a specific frame."""
    packet_len = len(packet_bytes)
    pkt = struct.pack("IIII",
                      timeval_s,
                      timeval_us,
                      packet_len,
                      packet_len
                      )
    file_obj.write(pkt)
    file_obj.write(packet_bytes)


def log_message(silent, message):
    """Log a message to the console."""
    if silent:
        pass
    else:
        print(message)


def get_args():
    """Return parsed args."""
    parser = argparse.ArgumentParser(description=("Kismet to Pcap "
                                                  "Log Converter"))
    parser.add_argument("--in", action="store", dest="infile",
                        help="Input (.kismet) file")
    parser.add_argument("--out", action="store", dest="outfile",
                        help="Output filename (when exporting all packets)")
    parser.add_argument("--outtitle", action="store", dest="outtitle",
                        help="Output title (when limiting packets per file)")
    parser.add_argument("--limit-packets", action="store", dest="limitpackets",
                        type=int,
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
    return parser.parse_args()


def main():
    """Parse args and write pcaps."""
    run_args = get_args()

    log_to_single = True

    if run_args.infile is None:
        log_message(False, "Expected --in [file]")
        sys.exit(1)

    if run_args.limitpackets is not None and run_args.outtitle is None:
        log_message(False, "Expected --outtitle when using --limit-packets")
        sys.exit(1)
    elif run_args.limitpackets is None and run_args.outfile is None:
        log_message(False, "Expected --out [file]")
        sys.exit(1)
    elif run_args.limitpackets and run_args.outtitle:
        log_message(False, ("Limiting to {} packets per file in "
                            "{}-X.pcap").format(run_args.limitpackets,
                                                run_args.outtitle))
        log_to_single = False

    query_args = {"dlt_gt": 0}

    if run_args.uuid is not None:
        query_args["datasource"] = run_args.uuid

    if run_args.starttime:
        query_args["ts_sec_gt"] = run_args.starttime

    if run_args.endtime:
        query_args["ts_sec_lt"] = run_args.endtime

    if run_args.minsignal:
        query_args["min_signal"] = run_args.minsignal

    logf = None
    lognum = 0

    packet_store = kismetdb.Packets(run_args.infile)

    npackets = 0
    file_mode = "wb"
    for result in packet_store.yield_all(**query_args):
        if logf is None:
            msg = "DLT {} for all packets".format(query_args["dlt_gt"])
            log_message(run_args.silent, msg)
            if log_to_single:
                msg = "Logging to {}".format(run_args.outfile)
                log_message(run_args.silent, msg)
                logf = open(run_args.outfile, file_mode)
                write_pcap_header(logf, result["dlt"])
            else:
                log_message(run_args.silent,
                            "Logging to {}-{}.pcap".format(run_args.outtitle,
                                                           lognum))
                logf = open("{}-{}.pcap".format(run_args.outtitle,
                                                lognum), file_mode)
                lognum = lognum + 1
                msg = "Writing PCAP header with DLT {}".format(result["dlt"])
                log_message(False, msg)
                write_pcap_header(logf, result["dlt"])

        write_pcap_packet(logf, int(result["ts_sec"]), int(result["ts_usec"]),
                          result["packet"])
        npackets = npackets + 1

        if not log_to_single:
            if npackets % run_args.limitpackets == 0:
                logf.close()
                logf = None
        elif run_args.silent is None:
            if npackets % 1000 == 0:
                log_message(False, "Converted {} packets...".format(npackets))

    if run_args.silent is None:
        log_message(False, "Done! Converted {} packets.".format(npackets))


if __name__ == "__main__":
    main()
