import os

import kismetdb


class TestIntegrationDevices(object):
    def test_integration_devices_instantiate(self):
        here_dir = os.path.dirname(os.path.abspath(__file__))
        test_db = os.path.join(here_dir, "../assets/testdata.kismet")
        abstraction = kismetdb.Devices(test_db)
        assert abstraction

    def test_integration_devices_get_all(self):
        here_dir = os.path.dirname(os.path.abspath(__file__))
        test_db = os.path.join(here_dir, "../assets/testdata.kismet")
        abstraction = kismetdb.Devices(test_db)
        all_alerts = abstraction.get_all()
        assert all_alerts

    def test_integration_devices_get_all_date_filter(self):
        here_dir = os.path.dirname(os.path.abspath(__file__))
        test_db = os.path.join(here_dir, "../assets/testdata.kismet")
        abstraction = kismetdb.Devices(test_db)
        all_alerts = abstraction.get_all(first_time_gt="2018-01-01")
        assert all_alerts

    def test_integration_devices_get_all_date_phy_filter(self):
        here_dir = os.path.dirname(os.path.abspath(__file__))
        test_db = os.path.join(here_dir, "../assets/testdata.kismet")
        abstraction = kismetdb.Devices(test_db)
        all_alerts = abstraction.get_all(first_time_gt="2018-01-01",
                                         phyname=["Bluetooth",
                                                  "IEEE802.11"])
        assert all_alerts

    def test_integration_devices_get_meta(self):
        here_dir = os.path.dirname(os.path.abspath(__file__))
        test_db = os.path.join(here_dir, "../assets/testdata.kismet")
        abstraction = kismetdb.Devices(test_db)
        all_alerts = abstraction.get_meta()
        assert all_alerts
        assert "json" not in all_alerts[0]

    def test_integration_devices_get_all_date_phy_filter(self):
        here_dir = os.path.dirname(os.path.abspath(__file__))
        test_db = os.path.join(here_dir, "../assets/testdata.kismet")
        abstraction = kismetdb.Devices(test_db)
        for alert in abstraction.yield_meta(first_time_gt="2018-01-01",
                                            phyname=["Bluetooth",
                                                     "IEEE802.11"]):
            assert alert
            assert "device" not in alert

    def test_integration_devices_yield_meta(self):
        here_dir = os.path.dirname(os.path.abspath(__file__))
        test_db = os.path.join(here_dir, "../assets/testdata.kismet")
        abstraction = kismetdb.Devices(test_db)
        for alert in abstraction.yield_meta():
            assert alert
            assert "device" not in alert
