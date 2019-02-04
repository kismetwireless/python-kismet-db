Quickstart
==========

.. toctree::

In the Python interpreter, after installing the kismetdb package via pip:

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
