kismet_log_to_kml
=================

.. toctree::

Export contents of the ``devices`` table to KML.

::

    usage: kismet_log_to_kml [-h] [--in INFILE] [--out OUTFILE]
                             [--start-time STARTTIME] [--min-signal MINSIGNAL]
                             [--strongest-point] [--title TITLE] [--ssid SSID]


    optional arguments:
      -h, --help              show this help message and exit
      --in INFILE             Input (.kismet) file
      --out OUTFILE           Output filename (optional)
      --start-time STARTTIME  Only list devices seen after given time
      --min-signal MINSIGNAL  Only list devices with a best signal higher than min-signal
      --strongest-point       Plot points based on strongest signal
      --title TITLE           Title embedded in KML file
      --ssid SSID             Only plot networks which match the SSID (or SSID regex)
