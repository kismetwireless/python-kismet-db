"""Data abstraction."""
from .base_interface import BaseInterface
from .utility import Utility


class DataPackets(BaseInterface):
    """This object covers non-packet data stored in the Kismet DB.


    The actual packet is stored in the `json` field of the dictionary
    returned for every row. This can be a very expensive abstraction to
    use if you don't employ some sort of filtering on your query. Consider
    using the `Packets.get_meta()` method to retrieve only the metadata
    (not the actual packet capture), which will preserve performance.
    The ``Keyword Arguments`` section below applies only to methods which
    support them (as noted below), not to object instantiation.


    Args:
        file_location (str): Path to Kismet log file.

    Keyword args:
        ts_sec_lt (str, datetime.datetime): Match packets where the timestamp
            is before this.
        ts_sec_gt (str, datetime.datetime): Match packets where the timestamp
            is after this.
        phyname (str or list): Exact match against phy type
        devmac (str or list): Exact match against device mac.
        datasource (str or list): Exact match against datasource UUID.
        type (str or list): Exact match against reported data type

    """

    table_name = "data"
    bulk_data_field = "json"
    field_defaults = {4: {"alt": 0,
                          "speed": 0,
                          "heading": 0},
                      5: {},
                      6: {}}
    converters_reference = {4: {"lat": Utility.format_int_as_latlon,
                                "lon": Utility.format_int_as_latlon,
                                "json": Utility.device_field_parser},
                            5: {"json": Utility.device_field_parser},
                            6: {"json": Utility.device_field_parser}}
    column_reference = {4: ["ts_sec", "ts_usec", "phyname", "devmac",
                            "lat", "lon", 
                            "datasource", "type", "json"],
                        5: ["ts_sec", "ts_usec", "phyname", "devmac",
                            "lat", "lon", "alt", "speed", "heading",
                            "datasource", "type", "json"],
                        6: ["ts_sec", "ts_usec", "phyname", "devmac",
                            "lat", "lon", "alt", "speed", "heading",
                            "datasource", "type", "json"]}
    valid_kwargs = {"ts_sec_lt": Utility.generate_single_tstamp_secs_lt,
                    "ts_sec_gt": Utility.generate_single_tstamp_secs_gt,
                    "phyname": Utility.generate_multi_string_sql_eq,
                    "devmac": Utility.generate_multi_string_sql_eq,
                    "datasource": Utility.generate_multi_string_sql_eq,
                    "type": Utility.generate_multi_string_sql_eq}
