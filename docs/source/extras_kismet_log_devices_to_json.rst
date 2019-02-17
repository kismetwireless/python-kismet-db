kismet_log_devices_to_json
==========================

.. toctree::

Export contents of devices table in Kismet DB to json file.

::

    usage: kismet_log_devices_to_json [-h] [--in INFILE] [--out OUTFILE]
                                      [--start-time STARTTIME]
                                      [--min-signal MINSIGNAL]

    optional arguments:
      -h, --help             show this help message and exit
      --in INFILE            Input (.kismet) file
      --out OUTFILE          Output filename (optional). If omitted, logs multi-
                             line and indented (human-readable) to stdout.
      --start-time STARTTIME Only list devices seen after given time
      --min-signal MINSIGNAL Only list devices with a best signal higher than min-signal
