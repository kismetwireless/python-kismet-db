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
        column_reference (dict): Top-level keys in this dictionary are version
            numbers, and are used to easily extend the schema for new versions.
            The ``column_names`` attribute is populated from this during
            instantiation.
        column_names (list): Name of columns expected to be in this object's
            table by this abstraction. Used for validation against columns in
            DB on instanitation.
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
    table_name = "KISMET"
    bulk_data_field = ""
    field_defaults = {4: {},
                      5: {},
                      6: {}}
    converters_reference = {4: {},
                            5: {},
                            6: {}}
    column_reference = {4: ["kismet_version", "db_version", "db_module"],
                        5: ["kismet_version", "db_version", "db_module"],
                        6: ["kismet_version", "db_version", "db_module"]}
    valid_kwargs = {}

    def __init__(self, file_location):
        self.check_db_exists(file_location)
        self.db_file = file_location
        self.db_version = self.get_db_version()
        self.column_names = self.column_reference[self.db_version]
        self.check_column_names(file_location)
        self.full_query_column_names = self.get_query_column_names()
        self.meta_query_column_names = self.get_meta_query_column_names()

    def get_db_version(self):
        sql = "SELECT db_version from KISMET"
        db = sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_COLNAMES)
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        result = row["db_version"]
        db.close()
        return int(result)

    def get_query_column_names(self):
        """Build query columns, which incorporate converters for bulk fields.

        This allows us to set query columns that may be different from the
        actual columns used in the database. This is necessary to incorporate
        some of the data massaging as it comes out of the database, so
        higher-level logic can parse it more easily.

        """
        result = []
        converter_reference = self.converters_reference[self.db_version]
        column_reference = self.column_reference[self.db_version]
        for col in column_reference:
            if col in converter_reference.keys():
                result.append("{} as \"{} [{}]\"".format(col, col, col))
            else:
                result.append(col)
        return result

    def get_meta_query_column_names(self):
        """Build query columns, which incorporate converters for bulk fields.

        This allows us to set query columns that may be different from the
        actual columns used in the database. This is necessary to incorporate
        some of the data massaging as it comes out of the database, so
        higher-level logic can parse it more easily.

        """
        result = []
        converter_reference = self.converters_reference[self.db_version]
        column_reference = self.column_reference[self.db_version]
        for col in column_reference:
            if col == self.bulk_data_field:
                continue
            elif col in converter_reference.keys():
                result.append("{} as \"{} [{}]\"".format(col, col, col))
            else:
                result.append(col)
        return result

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

        Keyword arguments are described above, near the beginning of
        the class documentation.

        Returns:
            list: List of each json object from all rows returned from query.
        """

        if kwargs:
            query_parts, replacements = self.generate_parts_and_replacements(kwargs)  # NOQA
        else:
            query_parts = []
            replacements = {}

        sql = "SELECT {} FROM {}".format(", ".join(self.full_query_column_names),  # NOQA
                                         self.table_name)
        if query_parts:
            sql = sql + " WHERE " + " AND ".join(query_parts)
        return self.get_rows(self.column_names, sql, replacements)

    def get_meta(self, **kwargs):
        """Get metadata columns from DB, excluding bulk data columns.

        Keyword arguments are described above, near the beginning of
        the class documentation.

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

        sql = "SELECT {} FROM {}".format(", ".join(self.meta_query_column_names),  # NOQA
                                         self.table_name)
        if query_parts:
            sql = sql + " WHERE " + " AND ".join(query_parts)
        return self.get_rows(columns, sql, replacements)

    def yield_all(self, **kwargs):
        """Get all objects represented by this class from Kismet DB.

        Yields one row at a time. Keyword arguments are described above,
        near the beginning of the class documentation.

        Yields:
            dict: Dict representing one row from query.
        """

        if kwargs:
            query_parts, replacements = self.generate_parts_and_replacements(kwargs)  # NOQA
        else:
            query_parts = []
            replacements = {}

        sql = "SELECT {} FROM {}".format(", ".join(self.full_query_column_names),  # NOQA
                                         self.table_name)
        if query_parts:
            sql = sql + " WHERE " + " AND ".join(query_parts)
        for row in self.yield_rows(self.column_names, sql, replacements):
            yield row

    def yield_meta(self, **kwargs):
        """Yield metadata from DB, excluding bulk data columns.

        Yields one row at a time. Keyword arguments are described above, near
        the beginning of the class documentation.

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

        sql = "SELECT {} FROM {}".format(", ".join(self.meta_query_column_names),  # NOQA
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
            err = "Could not find input file \"{}\"".format(log_file)
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
                   "{}. Expected {}, got {}".format(self.table_name, log_file,
                                                    self.column_names,
                                                    column_names))
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
        static_fields = self.field_defaults[self.db_version]
        results = []
        db = sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_COLNAMES)
        db.row_factory = sqlite3.Row
        for field_name, converter in list(self.converters_reference[self.db_version].items()):  # NOQA
            sqlite3.register_converter(field_name, converter)
        cur = db.cursor()
        cur.execute(sql, replacements)
        for row in cur.fetchall():
            result = {x: row[x] for x in column_names}
            result.update(static_fields)
            results.append(result.copy())  # NOQA
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
        static_fields = self.field_defaults[self.db_version]
        db = sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_COLNAMES)
        db.row_factory = sqlite3.Row
        for field_name, converter in list(self.converters_reference[self.db_version].items()):  # NOQA
            sqlite3.register_converter(field_name, converter)
        cur = db.cursor()
        cur.execute(sql, replacements)
        moar_rows = True
        while moar_rows:
            try:
                row = cur.fetchone()
                if row is None:
                    moar_rows = False
                else:
                    result = {x: row[x] for x in column_names}
                    result.update(static_fields)
                    yield result.copy()  # NOQA
            except KeyboardInterrupt:
                moar_rows = False
                print("Caught keyboard interrupt, exiting gracefully!")
        db.close()
        return
