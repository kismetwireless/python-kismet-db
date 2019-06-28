"""Base interface."""
import os
import sqlite3


class BaseInterface(object):
    """Initialize with a path to a valid Kismet log file.

    Args:
        file_location (str): Path to Kismet log file.

    Attribute:
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
        column_map (dict): The keys are column names, and the values are
            special handlers which allow enhanced filtering in database
            queries.
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
        super_columns (dict): Pseudo-columns and relative queries are defined
            here using objects like ``ColumnConplexTimestamp``.
    """

    table_name = "KISMET"
    bulk_data_field = ""
    column_map = {}
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
    super_columns = {}

    def __init__(self, file_location):
        """Initialize with ``file_location``."""
        self.check_db_exists(file_location)
        self.db_file = file_location
        self.db_version = self.get_db_version()
        self.column_names = self.column_reference[self.db_version]
        self.check_column_names(file_location)
        self.full_query_column_names = self.get_query_column_names()
        self.meta_query_column_names = self.get_meta_query_column_names()
        self.mapped_columns = list(self.column_map.keys())

    def get_db_version(self):
        """Return the database version."""
        sql = "SELECT db_version from KISMET"
        dbase = sqlite3.connect(self.db_file,
                                detect_types=sqlite3.PARSE_COLNAMES)
        dbase.row_factory = sqlite3.Row
        cur = dbase.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        result = row["db_version"]
        dbase.close()
        return int(result)

    def get_query_column_names(self):
        """Build query columns, which incorporate converters for bulk fields.

        This allows us to set query columns that may be different from the
        actual columns used in the database. This is necessary to incorporate
        some of the data massaging as it comes out of the database, so
        higher-level logic can parse it more easily.

        """
        result = []
        converters_reference = self.converters_reference[self.db_version]
        column_reference = self.column_reference[self.db_version]
        for col in column_reference:
            if col in converters_reference.keys():
                result.append("{col} as \"{col} [{col}]\"".format(col=col))
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
        converters_reference = self.converters_reference[self.db_version]
        column_reference = self.column_reference[self.db_version]
        for col in column_reference:
            if col == self.bulk_data_field:
                continue
            elif col in converters_reference.keys():
                result.append("{col} as \"{col} [{col}]\"".format(col=col))
            else:
                result.append(col)
        return result

    def generate_cols_parts_and_replacements(self, filters, columns):
        """Return tuple with sql parts and replacements."""
        cols = columns
        query_parts = []
        replacements = {}
        for key, val in list(filters.items()):
            if key not in self.valid_kwargs and key not in self.super_columns:
                continue
            if key in self.super_columns:
                super_column = self.super_columns[key]
                col_name = super_column.gen_select_field(key)
                if col_name not in cols:
                    cols.append(col_name)
                query_part = super_column.gen_sql_query(key)
                if query_part not in query_parts:
                    query_parts.append(query_part)
                replacements.update({key.split("_")[0]: val})
            else:
                results = self.valid_kwargs[key](key, val)
                query_parts.append(results[0])
                replacements.update(results[1])
        return (cols, query_parts, replacements)

    def get_all(self, **kwargs):
        """Get all objects represented by this class from Kismet DB.

        Keyword arguments are described above, near the beginning of
        the class documentation.

        Return:
            list: List of each json object from all rows returned from query.
        """
        if kwargs:
            cols, query_parts, replacements = self.generate_cols_parts_and_replacements(kwargs, self.full_query_column_names)  # NOQA
        else:
            cols = self.full_query_column_names
            query_parts = []
            replacements = {}

        sql = "SELECT {} FROM {}".format(", ".join(cols), self.table_name)
        if query_parts:
            sql = sql + " WHERE " + " AND ".join(query_parts)
        return self.get_rows(self.column_names, sql, replacements)

    def get_meta(self, **kwargs):
        """Get metadata columns from DB, excluding bulk data columns.

        Keyword arguments are described above, near the beginning of
        the class documentation.

        Return:
            list: List of each json object from all rows returned from query.
        """
        query_parts = []
        replacements = {}
        columns = list(self.column_names)
        columns.remove(self.bulk_data_field)

        if kwargs:
            cols, query_parts, replacements = self.generate_cols_parts_and_replacements(kwargs, self.meta_query_column_names)  # NOQA
        else:
            cols = self.meta_query_column_names
            query_parts = []
            replacements = {}

        sql = "SELECT {} FROM {}".format(", ".join(cols), self.table_name)
        if query_parts:
            sql = sql + " WHERE " + " AND ".join(query_parts)
        return self.get_rows(columns, sql, replacements)

    def yield_all(self, **kwargs):
        """Get all objects represented by this class from Kismet DB.

        Yields one row at a time. Keyword arguments are described above,
        near the beginning of the class documentation.

        Yield:
            dict: Dict representing one row from query.
        """
        if kwargs:
            cols, query_parts, replacements = self.generate_cols_parts_and_replacements(kwargs, self.full_query_column_names)  # NOQA
        else:
            cols = self.full_query_column_names
            query_parts = []
            replacements = {}

        sql = "SELECT {} FROM {}".format(", ".join(cols), self.table_name)
        if query_parts:
            sql = sql + " WHERE " + " AND ".join(query_parts)
        for row in self.yield_rows(self.column_names, sql, replacements):
            yield row

    def yield_meta(self, **kwargs):
        """Yield metadata from DB, excluding bulk data columns.

        Yields one row at a time. Keyword arguments are described above, near
        the beginning of the class documentation.

        Return:
            dict: Dict representing one row from query.
        """
        query_parts = []
        replacements = {}
        columns = list(self.column_names)
        columns.remove(self.bulk_data_field)
        if kwargs:
            cols, query_parts, replacements = self.generate_cols_parts_and_replacements(kwargs, self.meta_query_column_names)  # NOQA
        else:
            cols = self.meta_query_column_names
            query_parts = []
            replacements = {}

        sql = "SELECT {} FROM {}".format(", ".join(cols), self.table_name)
        if query_parts:
            sql = sql + " WHERE " + " AND ".join(query_parts)
        for row in self.yield_rows(columns, sql, replacements):
            yield row

    @classmethod
    def check_db_exists(cls, log_file):
        """Return None if able to open DB file, otherwise raise exception.

        Args:
            db_file (str): path to Kismet log file.

        Return:
            None

        Raise:
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

    @classmethod
    def get_column_names(cls, log_file, table_name):
        """Return a list of column names for `table_name` in `log_file`.

        Args:
            log_file (str): Path to Kismet log file.
            table_name (str): Name of table.

        Return:
            list: List of column names.
        """
        dbase = sqlite3.connect(log_file)
        dbase.row_factory = sqlite3.Row
        cur = dbase.cursor()
        cur.execute("SELECT * from {} LIMIT 1".format(table_name))
        cols = [d[0] for d in cur.description]
        dbase.close()
        return cols

    def check_column_names(self, log_file):
        """Check that schema is correct.

        Compares column names in DB to expected columns for abstraction.

        Return:
            None

        Raise:
            ValueError: Column names are not what we expect them to be.
        """
        column_names = self.get_column_names(log_file, self.table_name)
        if column_names != self.column_names:
            err = ("Schema mismatch in {} table, in file "
                   "{}. Expected {}, got {}".format(self.table_name, log_file,
                                                    self.column_names,
                                                    column_names))
            raise ValueError(err)

    def get_rows(self, column_names, sql, replacements):
        """Return rows from query results as a list of dictionary objects.

        Args:
            column_names (list): List of column names. Used in constructing
                row dictionary (these are the dictionary keys).
            sql (str): SQL statement.
            replacements (dict): Replacements for SQL query.

        Return:
            list: List of dictionary items.
        """
        static_fields = self.field_defaults[self.db_version]
        results = []
        dbase = sqlite3.connect(self.db_file,
                                detect_types=sqlite3.PARSE_COLNAMES)
        dbase.row_factory = sqlite3.Row
        for field_name, converter in list(self.converters_reference[self.db_version].items()):  # NOQA
            sqlite3.register_converter(field_name, converter)
        cur = dbase.cursor()
        cur.execute(sql, replacements)
        for row in cur.fetchall():
            result = {x: row[x] for x in column_names}
            result.update(static_fields)
            results.append(result.copy())  # NOQA
        dbase.close()
        return results

    def yield_rows(self, column_names, sql, replacements):
        """Yield rows from query results as a list of dictionary objects.

        Args:
            column_names (list): List of column names. Used in constructing
                row dictionary (these are the dictionary keys).
            sql (str): SQL statement.
            replacements (dict): Replacements for SQL query.

        Yield:
            dict: Dictionary object representing one row in result of SQL
                query.
        """
        static_fields = self.field_defaults[self.db_version]
        dbase = sqlite3.connect(self.db_file,
                                detect_types=sqlite3.PARSE_COLNAMES)
        dbase.row_factory = sqlite3.Row
        for field_name, converter in list(self.converters_reference[self.db_version].items()):  # NOQA
            sqlite3.register_converter(field_name, converter)
        cur = dbase.cursor()
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
        dbase.close()
