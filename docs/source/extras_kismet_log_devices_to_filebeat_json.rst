kismet_log_devices_to_filebeat_json
===================================

.. toctree::

Export from the ``devices`` table to stdout or append a json file.

::

    usage: kismet_log_devices_to_filebeat_json [-h] --in INFILE [--out OUTFILE]
                                               [--start-time STARTTIME]
                                               [--min-signal MINSIGNAL]

    optional arguments:
    -h, --help               show this help message and exit
    --in INFILE              Input (.kismet) file
    --out OUTFILE            Output filename (optional) for appending. If unspecified,
                             each record will be printed to stdout, one record per line,
                             ideal for piping into filebeat.
    --start-time STARTTIME   Only list devices seen after given time
    --min-signal MINSIGNAL   Only list devices with a best signal higher than min-signal
