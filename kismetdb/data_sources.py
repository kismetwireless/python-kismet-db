"""DataSources abstraction."""
from .base_interface import BaseInterface
from .utility import Utility

class DataSources(BaseInterface):
    """This object covers data sources stored in the Kismet DB.

    Args:
        file_location (str): Path to Kismet log file.

    Keyword args:
        uuid (str, list): UUID of data source.
        typestring (str, list): Type of data source.
        definition (str, list): Data source definition.
        name (str, list): Name of data source.
        interface (str, list): Interface associated with data source.

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

    table_name = "datasources"
    bulk_data_field = "json"
    column_names = ["uuid", "typestring", "definition", "name", "interface",
                    "json"]
    valid_kwargs = {"uuid": Utility.generate_multi_string_sql_eq,
                    "typestring": Utility.generate_multi_string_sql_eq,
                    "definition": Utility.generate_multi_string_sql_eq,
                    "name": Utility.generate_multi_string_sql_eq,
                    "interface": Utility.generate_multi_string_sql_eq}
