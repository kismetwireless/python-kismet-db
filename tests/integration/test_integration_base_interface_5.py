import os

import pytest

import kismetdb


class TestIntegrationBaseInterface(object):
    def test_integration_base_interface_instantiate_success(self):
        here_dir = os.path.dirname(os.path.abspath(__file__))
        test_db = os.path.join(here_dir, "../assets/testdata.kismet_5")
        base_interface = kismetdb.BaseInterface(test_db)
        assert base_interface

    def test_integration_base_interface_instantiate_file_noexist(self):
        here_dir = os.path.dirname(os.path.abspath(__file__))
        test_db = os.path.join(here_dir, "./testdata.kismet_5")
        with pytest.raises(ValueError) as e:
            kismetdb.BaseInterface(test_db)
        errtext = str(e.value)
        assert "testdata.kismet" in errtext
        assert "Could not find" in errtext
