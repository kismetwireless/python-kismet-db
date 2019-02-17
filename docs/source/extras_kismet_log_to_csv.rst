kismet_log_to_csv
=================

.. toctree::

Export contents of various tables in Kismet DB to csv file.

::

    usage: kismet_log_to_csv [-h] [--in INFILE] [--out OUTFILE] [--table SRCTABLE]

    optional arguments:
        -h, --help        show this help message and exit
        --in INFILE       Input (.kismet) file
        --out OUTFILE     Output CSV filename
        --table SRCTABLE  Select the table to export. The ``packets``, ``datasources``,
                          and ``alerts`` tables are supported. Defaults to ``devices`` table.
