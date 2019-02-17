Kismet database wrapper
_______________________


.. image:: https://readthedocs.org/projects/kismetdb/badge/?version=latest
   :target: https://kismetdb.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


Quickstart
----------

Install with `pip install .`

In the Python interpreter:

::

    import json
    import kismetdb
    kismet_log_file = "kismet/database.here"
    alerts = kismetdb.Alerts(kismet_log_file)

    # Get alert metadata
    all_alerts_meta = alerts.get_meta()
    for alert in all_alerts_meta:
        print(alert["header"])

    # Get payload from all alerts
    all_alerts = alerts.get_all()
    for alert in all_alerts:
        print(json.loads(alert["json"])["kismet.alert.text"])


Included scripts
----------------

Alongside the Python library, several commands are installed:

* ``kismet_log_devices_to_json``
* ``kismet_log_to_csv``
* ``kismet_log_to_kml``
* ``kismet_log_to_pcap``
* ``kismet_log_devices_to_filebeat_json``

Following any of the prior commands with ``--help`` will provide details on
usage.


Testing
-------

In order to test, you must place a kismet sqlite log file at
``tests/assets/testdata.kismet_4`` and ``tests/assets/testdata.kismet_5``,
which are Kismet version 4 and 5 databases, respectively.

Testing happens in a Docker build process:

Testing for Python 2.7:

``docker build .``

Testing for Python 3.6:

``docker build --build-arg PY_VER=3.6 .``

Testing for Python 3.7:

``docker build --build-arg PY_VER=3.7 .``

