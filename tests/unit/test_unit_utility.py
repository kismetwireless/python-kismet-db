import datetime

import kismetdb


class TestUnitUtility(object):
    def test_unit_utility_datetime_to_tuple(self):
        now_tup = datetime.datetime.now()
        result = kismetdb.Utility.datetime_to_tuple(now_tup)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert result != (0, 0)

    def test_unit_utility_timestamp_string_to_tuple(self):
        timestamps = ["2018-05-23T12:05:45.3001", "2018-01-01"]
        for timestamp in timestamps:
            result, err = kismetdb.Utility.timestamp_string_to_tuple(timestamp)
            assert isinstance(result, tuple)
            assert err == ""
            assert result != (0, 0)

    def test_unit_utility_timestamp_datatime_to_tuple(self):
        timestamp = datetime.datetime(year=2018, month=1, day=1)
        result = kismetdb.Utility.timestamp_to_dbtime(timestamp)
        assert isinstance(result, tuple)
        assert result == (1514764800, 0)

    def test_unit_utility_timestamp_int_to_tuple(self):
        timestamp = 1514764800
        result = kismetdb.Utility.timestamp_to_dbtime(timestamp)
        assert isinstance(result, tuple)
        assert result == (1514764800, 0)

    def test_unit_utility_timestamp_string_to_tuple_2(self):
        timestamps = ["nonsense", "nevermind", "2018-02-31"]
        for timestamp in timestamps:
            result, err = kismetdb.Utility.timestamp_string_to_tuple(timestamp)
            assert isinstance(result, tuple)
            assert err != ""
            assert result == (0, 0)

    def test_unit_utility_timestamp_tuple_validates_true(self):
        all_things_that_are_good = [(123, 456), (0, 0), (555, 100)]
        for thing in all_things_that_are_good:
            assert kismetdb.Utility.timestamp_tuple_validates(thing) == ""

    def test_unit_utility_timestamp_tuple_validates_false(self):
        will_fail_validation = [(123.1, "abcde"), (-10.5, 0), (None, 100)]
        for thing in will_fail_validation:
            assert kismetdb.Utility.timestamp_tuple_validates(thing) != ""

    def test_unit_utility_generate_single_tstamp_secs_eq_str(self):
        column_name = "tstamp_abc"
        filter_value = "2018-01-01"
        result = kismetdb.Utility.generate_single_tstamp_secs_eq(column_name,
                                                                 filter_value)
        assert result[0] == "tstamp_abc = :tstamp_abc"
        assert result[1] == {"tstamp_abc": 1514764800}

    def test_unit_utility_generate_single_tstamp_secs_eq_tup(self):
        column_name = "tstamp_abc"
        filter_value = (1514764800, 1000)
        result = kismetdb.Utility.generate_single_tstamp_secs_eq(column_name,
                                                                 filter_value)
        assert result[0] == "tstamp_abc = :tstamp_abc"
        assert result[1] == {"tstamp_abc": 1514764800}
