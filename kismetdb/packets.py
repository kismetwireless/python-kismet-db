"""Packets abstraction."""
from .base_interface import BaseInterface
from .utility import Utility


class Packets(BaseInterface):
    """This object covers packets stored in the Kismet DB.


    The actual packet is stored in the `packet` field of the dictionary
    returned for every row. This can be a very expensive abstraction to
    use if you don't employ some sort of filtering on your query. Consider
    using the `Packets.get_meta()` method to retrieve only the metadata
    (not the actual packet capture), which will preserve performance.


    Args:
        file_location (str): Path to Kismet log file.

    Keyword args:
        ts_sec_lt (str, datetime.datetime): Match packets where the timestamp
            is before this.
        ts_sec_gt (str, datetime.datetime): Match packets where the timestamp
            is after this.
        phyname (str or list): Exact match against PHY name.
        sourcemac (str or list): Exact match against source MAC address.
        destmac (str or list): Exact match against destination MAC address.
        transmac (str or list): Exact match against trans mac.
        devkey (str or list): Exact match against devkey.
        datasource (str or list): Exact match against datasource.
        min_signal (str or int): Minimum signal.
        dlt_gt (str or int): Minimum DLT.


    Attributes:
        bulk_data_field (str): Field containing bulk data (typically stored
            as a blob in the DB). This allows the `get_meta()` method to
            exclude information which may have a performance impact. This
            is especially true for the retrieval of packet captures.
        column_names (str): Name of columns expected to be in table represented
            by this abstraction. Used for validation against columns in
            DB on instanitation. This is constructed on instantiation, based
            on the version of DB that's detected.
        table_name (str): Name of the table this abstraction represents.
        valid_kwargs (str): This is a dictionary where the key is the name
            of a keyword argument and the value is a reference to the function
            which builds the SQL partial and replacement dictionary.
        field_defaults (dict): Statically set these column defaults by DB
            version.
        converters_reference (dict): This provides a reference for converters
            to use on data coming from the DB on a version by version basis.
        full_query_column_names (list): Processed column names for full query
            of kismet DB. Created on instantiation.
        meta_query_column_names (list): Processed column names for meta query
            of kismet DB. Created on instantiation.

    """

    table_name = "packets"
    bulk_data_field = "packet"
    field_defaults = {4: {"alt": 0,
                          "speed": 0,
                          "heading": 0},
                      5: {}}
    converters_reference = {4: {"lat": Utility.format_int_as_latlon,
                                "lon": Utility.format_int_as_latlon},
                            5: {}}
    column_reference = {4: ["ts_sec", "ts_usec", "phyname", "sourcemac",
                            "destmac", "transmac", "frequency", "devkey",
                            "lat", "lon", "packet_len", "signal", "datasource",
                            "dlt", "packet", "error"],
                        5: ["ts_sec", "ts_usec", "phyname", "sourcemac",
                            "destmac", "transmac", "frequency", "devkey",
                            "lat", "lon", "alt", "speed", "heading",
                            "packet_len", "signal", "datasource", "dlt",
                            "packet", "error"]}
    valid_kwargs = {"ts_sec_lt": Utility.generate_single_tstamp_secs_lt,
                    "ts_sec_gt": Utility.generate_single_tstamp_secs_gt,
                    "devkey": Utility.generate_multi_string_sql_eq,
                    "phyname": Utility.generate_multi_string_sql_eq,
                    "sourcemac": Utility.generate_multi_string_sql_eq,
                    "destmac": Utility.generate_multi_string_sql_eq,
                    "transmac": Utility.generate_multi_string_sql_eq,
                    "devmac": Utility.generate_multi_string_sql_eq,
                    "datasource": Utility.generate_multi_string_sql_eq,
                    "min_signal": Utility.generate_single_int_sql_gt,
                    "dlt_gt": Utility.generate_single_int_sql_gt}
