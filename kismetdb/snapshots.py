"""Snapshots abstraction."""
from .base_interface import BaseInterface
from .utility import Utility


class Snapshots(BaseInterface):
    """This object covers snapshots stored in the Kismet DB.

    The ``Keyword Arguments`` section below applies only to methods which
    support them (as noted below), not to object instantiation.

    Args:
        file_location (str): Path to Kismet log file.

    Keyword args:
        ts_sec_gt (str, datetime, or (secs, u_secs)): Timestamp for starting
            query.
        ts_sec_lt (str, datetime, or (secs, usecs)): Timestamp for ending
            query.
        lat_gt (str, float): Bounding minimum latitude
        lat_lt (str, float): Bounding maximum latitude
        lon_gt (str, float): Bounding minimum longitude
        lon_lt (str, float): Bounding maximum longitude
        snaptype (str): Snapshot type
    """

    table_name = "snapshots"
    bulk_data_field = "json"
    field_defaults = {4: {},
                      5: {},
                      6: {}}
    converters_reference = {4: {"lat": Utility.format_int_as_latlon,
                                "lon": Utility.format_int_as_latlon},
                            5: {},
                            6: {}}
    column_reference = {4: ["ts_sec", "ts_usec", "snaptype", "json"],
                        5: ["ts_sec", "ts_usec", "lat", "lon", "snaptype", "json"],
                        6: ["ts_sec", "ts_usec", "lat", "lon", "snaptype", "json"],
                        }
    valid_kwargs = {"ts_sec_gt": Utility.generate_single_tstamp_secs_gt,
                    "ts_sec_lt": Utility.generate_single_tstamp_secs_lt,
                    "lat_gt": Utility.generate_single_float_sql_gt,
                    "lon_gt": Utility.generate_single_float_sql_gt,
                    "lat_lt": Utility.generate_single_float_sql_lt,
                    "lon_lt": Utility.generate_single_float_sql_lt,
                    "snaptype": Utility.generate_single_string_sql_eq,
                    }
