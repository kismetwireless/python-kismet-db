Kismet DB abstraction
=====================

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


Testing
-------

In order to test, you must place a kismet sqlite log file at
``tests/assets/testdata.kismet``.

Testing happens in a Docker build process:

Testing for Python 2.7:

``docker build .``

Testing for Python 3.6:

``docker build --build-arg PY_VER=3.6 .``

Testing for Python 3.7:

``docker build --build-arg PY_VER=3.7 .``
