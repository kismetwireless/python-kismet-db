import os

import kismetdb


class TestIntegrationPackets(object):
    def test_integration_packets_instantiate(self):
        here_dir = os.path.dirname(os.path.abspath(__file__))
        test_db = os.path.join(here_dir, "../assets/testdata.kismet_4")
        abstraction = kismetdb.Packets(test_db)
        assert abstraction

    def test_integration_packets_yield_all_date_phy_filter(self):
        here_dir = os.path.dirname(os.path.abspath(__file__))
        test_db = os.path.join(here_dir, "../assets/testdata.kismet_4")
        abstraction = kismetdb.Packets(test_db)
        for packet in abstraction.yield_meta(first_time_gt="2018-01-01"):
            assert packet
            assert "packet" not in packet
            assert packet["alt"] == 0
            assert packet["speed"] == 0
            assert packet["heading"] == 0
            assert isinstance(packet["lat"], float)
            assert isinstance(packet["lon"], float)

    def test_integration_packets_yield_meta(self):
        here_dir = os.path.dirname(os.path.abspath(__file__))
        test_db = os.path.join(here_dir, "../assets/testdata.kismet_4")
        abstraction = kismetdb.Packets(test_db)
        for packet in abstraction.yield_meta():
            assert packet
            assert "packet" not in packet
            assert packet["alt"] == 0
            assert packet["speed"] == 0
            assert packet["heading"] == 0
            assert packet["ts_sec"] != 0
            assert isinstance(packet["lat"], float)
            assert isinstance(packet["lon"], float)

    def test_integration_packets_yield_meta_supercol_ts(self):
        here_dir = os.path.dirname(os.path.abspath(__file__))
        test_db = os.path.join(here_dir, "../assets/testdata.kismet_4")
        abstraction = kismetdb.Packets(test_db)
        for packet in abstraction.yield_meta(ts_gt=1):
            assert packet
            assert "packet" not in packet
            assert packet["alt"] == 0
            assert packet["speed"] == 0
            assert packet["heading"] == 0
            assert packet["ts_sec"] != 0
            assert isinstance(packet["ts"], float)
            assert isinstance(packet["lat"], float)
            assert isinstance(packet["lon"], float)
