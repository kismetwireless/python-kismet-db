import os
import sqlite3


class BaseInterface(object):
    """Initialize with a path to a valid Kismet log file.

    Args:
        file_location (str): Path to Kismet log file.

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
        bulk_parser (None or str): This is the name of the custom converter
            used for converting bulk data coming from the DB into something
            predictable for the user.

    """
    table_name = "KISMET"
    bulk_data_field = ""
    column_names = ["kismet_version", "db_version", "db_module"]
    valid_kwargs = {}
    bulk_parser = None
    query_column_names = []

    def __init__(self, file_location):
        self.check_db_exists(file_location)
        self.check_column_names(file_location)
        self.db_file = file_location
        self.set_query_column_names()

    def set_query_column_names(self):
        """Build query columns, which incorporate converters for bulk fields.

        This allows us to set query columns that may be different from the
        actual columns used in the database. This is necessary to incorporate
        some of the data massaging as it comes out of the database, so
        higher-level logic can parse it more easily.

        """
        result = []
        for col in self.column_names:
            if (self.bulk_parser is not None and col == self.bulk_data_field):
                result.append("{} as \"{} [{}]\"".format(col, col, col))
            else:
                result.append(col)
        self.query_column_names = result

    def generate_parts_and_replacements(self, filters):
        """Return tuple with sql parts and replacements."""
        query_parts = []
        replacements = {}
        for k, v in list(filters.items()):
            if k not in self.valid_kwargs:
                continue
            results = self.valid_kwargs[k](k, v)
            query_parts.append(results[0])
            replacements.update(results[1])
        return (query_parts, replacements)

    def get_all(self, **kwargs):
        """Get all objects represented by this class from Kismet DB.

        Keyword Args:
            See class documentation!

        Returns:
            list: List of each json object from all rows returned from query.
        """

        if kwargs:
            query_parts, replacements = self.generate_parts_and_replacements(kwargs)  # NOQA
        else:
            query_parts = []
            replacements = {}

        sql = "SELECT {} FROM {}".format(", ".join(self.query_column_names),
                                         self.table_name)
        if query_parts:
            sql = sql + " WHERE " + " AND ".join(query_parts)
        return self.get_rows(self.column_names, sql, replacements)

    def get_meta(self, **kwargs):
        """Get metadata columns from DB, excluding bulk data columns.

        For large queries, this will save memory overhead, especially when
        targeting packet captures.

        Keyword Args:
            See class documentation!

        Returns:
            list: List of each json object from all rows returned from query.
        """

        query_parts = []
        replacements = {}
        columns = list(self.column_names)
        columns.remove(self.bulk_data_field)

        if kwargs:
            query_parts, replacements = self.generate_parts_and_replacements(kwargs)  # NOQA
        else:
            query_parts = []
            replacements = {}

        sql = "SELECT {} FROM {}".format(", ".join(columns),
                                         self.table_name)
        if query_parts:
            sql = sql + " WHERE " + " AND ".join(query_parts)
        return self.get_rows(columns, sql, replacements)

    def yield_all(self, **kwargs):
        """Get all objects represented by this class from Kismet DB.

        Yields one row at a time.

        Keyword Args:
            See class documentation!

        Yields:
            dict: Dict representing one row from query.
        """

        if kwargs:
            query_parts, replacements = self.generate_parts_and_replacements(kwargs)  # NOQA
        else:
            query_parts = []
            replacements = {}

        sql = "SELECT {} FROM {}".format(", ".join(self.query_column_names),
                                         self.table_name)
        if query_parts:
            sql = sql + " WHERE " + " AND ".join(query_parts)
        for row in self.yield_rows(self.column_names, sql, replacements):
            yield row

    def yield_meta(self, **kwargs):
        """Yield metadata from DB, excluding bulk data columns.

        Yields one row at a time.

        Keyword Args:
            See class documentation!

        Returns:
            dict: Dict representing one row from query.
        """

        query_parts = []
        replacements = {}
        columns = list(self.column_names)
        columns.remove(self.bulk_data_field)

        if kwargs:
            query_parts, replacements = self.generate_parts_and_replacements(kwargs)  # NOQA
        else:
            query_parts = []
            replacements = {}

        sql = "SELECT {} FROM {}".format(", ".join(columns),
                                         self.table_name)
        if query_parts:
            sql = sql + " WHERE " + " AND ".join(query_parts)
        for row in self.yield_rows(columns, sql, replacements):
            yield row

    @classmethod
    def check_db_exists(cls, log_file):
        """Return None if able to open DB file, otherwise raise exception.

        Args:
            db_file (str): path to Kismet log file.

        Returns:
            None

        Raises:
            ValueError: File either does not exist, is not in sqlite3 format,
                or file is not a valid Kismet log file.
        """
        if not os.path.isfile(log_file):
            err = "Could not find input file '{}'".format(log_file)
            raise ValueError(err)
        try:
            cls.get_column_names(log_file, "KISMET")
        except sqlite3.DatabaseError:
            err = "This is not a valid database file: {}".format(log_file)
            raise ValueError(err)
        except sqlite3.OperationalError:
            err = ("This is a valid sqlite3 file, but it does not appear to "
                   "be a valid Kismet log file: {}".format(log_file))
            raise ValueError(err)
        return

    @classmethod
    def get_column_names(cls, log_file, table_name):
        """Return a list of column names for `table_name` in `log_file`.

        Args:
            log_file (str): Path to Kismet log file.
            table_name (str): Name of table.

        Returns:
            list: List of column names.
        """
        db = sqlite3.connect(log_file)
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT * from {} LIMIT 1".format(table_name))
        cols = [d[0] for d in cur.description]
        db.close()
        return cols

    def check_column_names(self, log_file):
        """Check that schema is correct.

        Compares column names in DB to expected columns for abstraction.

        Returns:
            None

        Raises:
            ValueError: Column names are not what we expect them to be.
        """
        column_names = self.get_column_names(log_file, self.table_name)
        if column_names != self.column_names:
            err = ("Schema mismatch in {} table, in file "
                   "{}".format(self.table_name, log_file))
            raise ValueError(err)
        return

    def get_rows(self, column_names, sql, replacements):
        """Return rows from query results as a list of dictionary objects.

        Args:
            column_names (list): List of column names. Used in constructing
                row dictionary (these are the dictionary keys).
            sql (str): SQL statement.
            replacements (dict): Replacements for SQL query.

        Returns:
            list: List of dictionary items.
        """
        results = []
        db = sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_COLNAMES)
        db.row_factory = sqlite3.Row
        if self.bulk_parser:
            sqlite3.register_converter(self.bulk_data_field,
                                       getattr(self, self.bulk_parser))
        cur = db.cursor()
        cur.execute(sql, replacements)
        for row in cur.fetchall():
            results.append({x: row[x] for x in column_names}.copy())
        db.close()
        return results

    def yield_rows(self, column_names, sql, replacements):
        """Yield rows from query results as a list of dictionary objects.

        Args:
            column_names (list): List of column names. Used in constructing
                row dictionary (these are the dictionary keys).
            sql (str): SQL statement.
            replacements (dict): Replacements for SQL query.

        Yields:
            dict: Dictionary object representing one row in result of SQL
                query.
        """
        db = sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_COLNAMES)
        db.row_factory = sqlite3.Row
        if self.bulk_parser:
            sqlite3.register_converter(self.bulk_data_field,
                                       getattr(self, self.bulk_parser))
        cur = db.cursor()
        cur.execute(sql, replacements)
        moar_rows = True
        while moar_rows:
            try:
                row = cur.fetchone()
                if row is None:
                    moar_rows = False
                else:
                    yield {x: row[x] for x in column_names}.copy()
            except KeyboardInterrupt:
                moar_rows = False
                print("Caught keyboard interrupt, exiting gracefully!")
        db.close()
        return
