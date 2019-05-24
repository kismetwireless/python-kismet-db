"""Alerts abstraction."""
from .base_interface import BaseInterface
from .utility import Utility


class Alerts(BaseInterface):
    """This object covers alerts stored in the Kismet DB.

    The ``Keyword Arguments`` section below applies only to methods which
    support them (as noted below), not to object instantiation.

    Args:
        file_location (str): Path to Kismet log file.

    Keyword args:
        ts_sec_gt (str, datetime, or (secs, u_secs)): Timestamp for starting
            query.
        phyname (str, list): Restrict results to this PHY.
        devmac (str, list): Restrict results to this MAC address.
        header (str, list): Restrict results to alerts of this type.

    """

    table_name = "alerts"
    bulk_data_field = "json"
    field_defaults = {4: {},
                      5: {},
                      6: {}}
    converters_reference = {4: {"lat": Utility.format_int_as_latlon,
                                "lon": Utility.format_int_as_latlon},
                            5: {},
                            6: {}}
    column_reference = {4: ["ts_sec", "ts_usec", "phyname", "devmac", "lat",
                            "lon", "header", "json"],
                        5: ["ts_sec", "ts_usec", "phyname", "devmac", "lat",
                            "lon", "header", "json"],
                        6: ["ts_sec", "ts_usec", "phyname", "devmac", "lat",
                            "lon", "header", "json"]}
    valid_kwargs = {"ts_sec_gt": Utility.generate_single_tstamp_secs_gt,
                    "devmac": Utility.generate_multi_string_sql_eq,
                    "header": Utility.generate_multi_string_sql_eq,
                    "phyname": Utility.generate_multi_string_sql_eq}
