"""Alerts abstraction."""
from .base_interface import BaseInterface
from .utility import Utility


class Alerts(BaseInterface):
    """This object covers alerts stored in the Kismet DB.

    Args:
        file_location (str): Path to Kismet log file.

    Keyword args:
        ts_sec_gt (str, datetime, or (secs, u_secs)): Timestamp for starting
            query.
        phyname (str, list): Restrict results to this PHY.
        devmac (str, list): Restrict results to this MAC address.
        header (str, list): Restrict results to alerts of this type.

    Attributes:
        bulk_data_field (str): Field containing bulk data (typically stored
            as a blob in the DB). This allows the `get_meta()` method to
            exclude information which may have a performance impact. This
            is especially true for the retrieval of packet captures.
        column_names (str): Name of columns expected to be in table represented
            by this abstraction. Used for validation against columns in
            DB on instanitation.
        table_name (str): Name of the table this abstraction represents.
        valid_kwargs (str): This is a dictionary where the key is the name
            of a keyword argument and the value is a reference to the function
            which builds the SQL partial and replacement dictionary.

    """

    table_name = "alerts"
    bulk_data_field = "json"
    column_names = ["ts_sec", "ts_usec", "phyname", "devmac", "lat", "lon",
                    "header", "json"]
    valid_kwargs = {"ts_sec_gt": Utility.generate_single_tstamp_secs_gt,
                    "devmac": Utility.generate_multi_string_sql_eq,
                    "header": Utility.generate_multi_string_sql_eq,
                    "phyname": Utility.generate_multi_string_sql_eq}
