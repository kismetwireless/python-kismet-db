kismet_log_to_pcap
==================

.. toctree::

Export captures from the ``packets`` table to .pcap file.

::

    usage: kismet_log_to_pcap [-h] [--in INFILE] [--out OUTFILE]
                              [--outtitle OUTTITLE] [--limit-packets LIMITPACKETS]
                              [--source-uuid UUID] [--start-time STARTTIME]
                              [--end-time ENDTIME] [--silent SILENT]
                              [--min-signal MINSIGNAL] [--device-key DEVICEKEY]

    optional arguments:
        -h, --help                    show this help message and exit
        --in INFILE                   Input (.kismet) file
        --out OUTFILE                 Output filename (when exporting all packets)
        --outtitle OUTTITLE           Output title (when limiting packets per file)
        --limit-packets LIMITPACKETS  Generate multiple pcap files, limiting the number
                                      of packets per file
        --source-uuid UUID            Limit packets to a specific data source (multiple
                                      --source-uuid options will match multiple datasources)
        --start-time STARTTIME        Only convert packets recorded after start-time
        --end-time ENDTIME            Only convert packets recorded before end-time
        --silent SILENT               Silent operation (no status output)
        --min-signal MINSIGNAL        Only convert packets with a signal greater than min-signal
        --device-key DEVICEKEY        Only convert packets which are linked to the specified device
                                      key (multiple --device-key options will match multiple devices)
