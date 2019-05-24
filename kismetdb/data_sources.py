"""DataSources abstraction."""
from .base_interface import BaseInterface
from .utility import Utility


class DataSources(BaseInterface):
    """This object covers data sources stored in the Kismet DB.

    The ``Keyword Arguments`` section below applies only to methods which
    support them (as noted below), not to object instantiation.

    Args:
        file_location (str): Path to Kismet log file.

    Keyword args:
        uuid (str, list): UUID of data source.
        typestring (str, list): Type of data source.
        definition (str, list): Data source definition.
        name (str, list): Name of data source.
        interface (str, list): Interface associated with data source.
    """

    table_name = "datasources"
    bulk_data_field = "json"
    field_defaults = {4: {},
                      5: {},
                      6: {}}
    converters_reference = {4: {},
                            5: {},
                            6: {}}
    column_reference = {4: ["uuid", "typestring", "definition", "name",
                            "interface", "json"],
                        5: ["uuid", "typestring", "definition", "name",
                            "interface", "json"],
                        6: ["uuid", "typestring", "definition", "name",
                            "interface", "json"]}
    valid_kwargs = {"uuid": Utility.generate_multi_string_sql_eq,
                    "typestring": Utility.generate_multi_string_sql_eq,
                    "definition": Utility.generate_multi_string_sql_eq,
                    "name": Utility.generate_multi_string_sql_eq,
                    "interface": Utility.generate_multi_string_sql_eq}
