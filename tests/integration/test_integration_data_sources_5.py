import os

import kismetdb


class TestIntegrationDataSources(object):
    def test_integration_datasources_instantiate(self):
        here_dir = os.path.dirname(os.path.abspath(__file__))
        test_db = os.path.join(here_dir, "../assets/testdata.kismet_5")
        abstraction = kismetdb.DataSources(test_db)
        assert abstraction

    def test_integration_datasources_get_all(self):
        here_dir = os.path.dirname(os.path.abspath(__file__))
        test_db = os.path.join(here_dir, "../assets/testdata.kismet_5")
        abstraction = kismetdb.DataSources(test_db)
        all_sources = abstraction.get_all()
        for source in all_sources:
            assert isinstance(source["json"], type(""))
