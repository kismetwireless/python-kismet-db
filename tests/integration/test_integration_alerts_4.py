import os

import kismetdb


class TestIntegrationAlerts(object):
    def test_integration_alerts_instantiate(self):
        here_dir = os.path.dirname(os.path.abspath(__file__))
        test_db = os.path.join(here_dir, "../assets/testdata.kismet_4")
        abstraction = kismetdb.Alerts(test_db)
        assert abstraction

    def test_integration_alerts_get_all(self):
        here_dir = os.path.dirname(os.path.abspath(__file__))
        test_db = os.path.join(here_dir, "../assets/testdata.kismet_4")
        abstraction = kismetdb.Alerts(test_db)
        all_alerts = abstraction.get_all()
        assert all_alerts

    def test_integration_alerts_get_all_date_filter(self):
        here_dir = os.path.dirname(os.path.abspath(__file__))
        test_db = os.path.join(here_dir, "../assets/testdata.kismet_4")
        abstraction = kismetdb.Alerts(test_db)
        all_alerts = abstraction.get_all(ts_sec_gt="2018-01-01")
        assert all_alerts

    def test_integration_alerts_get_all_date_phy_filter(self):
        here_dir = os.path.dirname(os.path.abspath(__file__))
        test_db = os.path.join(here_dir, "../assets/testdata.kismet_4")
        abstraction = kismetdb.Alerts(test_db)
        all_alerts = abstraction.get_all(ts_sec_gt="2018-01-01",
                                         phyname=["Bluetooth",
                                                  "IEEE802.11",
                                                  "UNKNOWN"])
        assert all_alerts

    def test_integration_alerts_get_meta(self):
        here_dir = os.path.dirname(os.path.abspath(__file__))
        test_db = os.path.join(here_dir, "../assets/testdata.kismet_4")
        abstraction = kismetdb.Alerts(test_db)
        all_alerts = abstraction.get_meta()
        assert all_alerts
        assert "json" not in all_alerts[0]
