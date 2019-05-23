"""General utility functions that are shared between other classes."""
import datetime
import json
import sys

from dateutil import parser as dateparser


class Utility(object):
    @classmethod
    def timestamp_to_iso(cls, timestamp):
        """Return an ISO-formatted timestamp for unix ``timestamp``."""
        if not isinstance(timestamp, int):
            raise ValueError("Integer required for timestamp conversion.")
        return datetime.datetime.fromtimestamp(timestamp).isoformat()

    @classmethod
    def timestamp_to_dbtime(cls, timestamp):
        """Return a tuple containing Unix epoch seconds and microseconds.

        Args:
            timestamp (datetime, str, or tuple): If this is a string, we
                attempt to parse as such. If this is a tuple, we
                expect a tuple of length 2 and both items should be type:
                `int`.

        Returns:
            tuple: (secs, u_secs)
        """
        t_tup = (0, 0)
        d_type = type(timestamp)
        err = ("Wrong type for timestamp. Got {}. We expect a tuple (int, "
               "int), string, or datetime.datetime object.").format(d_type)
        if isinstance(timestamp, tuple):
            err = cls.timestamp_tuple_validates(timestamp)
            if not err:
                t_tup = timestamp
        elif cls.is_it_a_string(timestamp):
            t_tup, err = cls.timestamp_string_to_tuple(timestamp)
        elif isinstance(timestamp, datetime.datetime):
            t_tup = cls.datetime_to_tuple(timestamp)
            err = ""
        elif isinstance(timestamp, int):
            t_tup = (timestamp, 0)
            err = ""
        if err:
            raise ValueError(err)
        return t_tup

    @classmethod
    def datetime_to_tuple(cls, timestamp):
        """Return a timestamp tuple.

        Args:
            timestamp (datetime.datetime): Python datetime.datetime object.

        Returns:
            tup: (seconds, u_seconds)
        """
        epoch = datetime.datetime.utcfromtimestamp(0)
        secs = str((timestamp - epoch).total_seconds())
        seconds = int(secs.split(".")[0])
        u_seconds = int(secs.split(".")[1]) if len(secs.split(".")) > 1 else 0
        return (seconds, u_seconds)

    @classmethod
    def timestamp_string_to_tuple(cls, timestamp):
        """Return a timestamp tuple if possible, and a reason for failure.
        Args:
            timestamp (str): String-formatted timestamp.

        Returns:
            tup: (t_tuple, err). t_tuple is a pair of integers for seconds
                and u_seconds. err is a string describing errors in
                parsing, if any. Successful parsing means that err is an
                empty string.
        """
        err = ""
        ts = datetime.datetime.utcfromtimestamp(0)
        epoch = datetime.datetime.utcfromtimestamp(0)
        try:
            ts = dateparser.parse(timestamp, fuzzy=True)
        except ValueError as e:
            err = ("Could not extract a date/time from start-time "
                   "argument: {}".format(e))
        secs = str((ts - epoch).total_seconds())
        seconds = int(secs.split(".")[0])
        u_seconds = int(secs.split(".")[1]) if len(secs.split(".")) > 1 else 0
        result = (seconds, u_seconds)
        return (result, err)

    @classmethod
    def timestamp_tuple_validates(cls, timestamp):
        """Return empty string if valid, reason if otherwise."""
        err = ""
        if len(timestamp) != 2:
            err = ("Badly-formatted timestamp tuple. We expect a tuple of "
                   "length 2")
        elif [x for x in timestamp if not isinstance(x, int)]:
            err = ("Badly-formatted timestamp tuple. We expect two "
                   "integers.")
        return err

    @classmethod
    def format_tstamp_secs(cls, tstamp):
        """Return epoch seconds only from timestamp."""
        t_tup = cls.timestamp_to_dbtime(tstamp)
        return str(t_tup[0])

    @classmethod
    def format_string_match(cls, in_str):
        """This just returns a string-type for the argument.

        This is more or less a placeholder where we may have an opportunity
        to sanitize data at a later date.
        """
        return str(in_str)

    @classmethod
    def format_int_match(cls, in_str):
        """This just returns an integer-type representation for the argument.

        This is more or less a placeholder where we may decide to do some
        sanitization at a later date.
        """
        return int(in_str)

    @classmethod
    def format_latlon_as_integer(cls, lat_or_lon):
        """Return integer for input lat or lon str or float.

        This is used to get our lat/lon into the same format used in the DB.
        """
        in_val = float(lat_or_lon)
        result = in_val * 100000
        return int(result)

    @classmethod
    def format_int_as_latlon(cls, lat_or_lon):
        """Return float for input lat or lon str or int.

        This is used to get the lat or lon from the DB into the form other
        tools will more readily accept.
        """
        result = int(lat_or_lon) / 100000.0
        return result

    @classmethod
    def generate_single_string_sql_eq(cls, column_name, filter_value):
        """Return tuple with sql and replacement.

        This function builds the sql partial and replacement dict for
        an equivalency match for one value against a single column in
        the database.

        Args:
            column_name (str): Name of column in DB.
            filter_value (str): This is what we look for in the column.

        Returns:
            tuple: Item 0 contains the SQL partial string. Item 1 contains
                the replacement dictionary.

        """
        sql = "{} = :{}".format(column_name, column_name)
        replacement = {column_name: str(filter_value)}
        return (sql, replacement)

    @classmethod
    def generate_multi_string_sql_eq(cls, column_name, filter_values):
        """Return tuple with sql and replacement.

        This function builds the sql partial and replacement dict for
        an equivalency match for multiple values (OR) against a single
        column in the database.

        Args:
        column_name (str): Name of column in DB.
        filter_values (list or str): This is what we look for in the column.
            If a string-type object is used for this argument, this function
            behaves as a wrapper for `Utility.generate_single_string_sql_eq()`

        Returns:
            tuple: Item 0 contains the SQL partial string. Item 1 contains
                the replacement dictionary.

        """
        if not isinstance(filter_values, list):
            return cls.generate_single_string_sql_eq(column_name,
                                                     filter_values)
        sql_parts = []
        replacement = {}
        increment = 1
        for filter_value in filter_values:
            colref = "{}{}".format(column_name, str(increment))
            sql_parts.append("{} = :{}".format(column_name, colref))
            replacement[colref] = str(filter_value)
            increment += 1
        sql = "( {} )".format(" OR ".join(sql_parts))
        return (sql, replacement)

    @classmethod
    def generate_single_string_sql_includes(cls, column_name, filter_value):
        """Return tuple with sql and replacement.

        This function builds the sql partial and replacement dict for
        an inclusion (LIKE %VALUE%) match for one value against a single 
        column in the database.

        Args:
            column_name (str): Name of column in DB.
            filter_value (str): This is what we look for in the column.

        Returns:
            tuple: Item 0 contains the SQL partial string. Item 1 contains
                the replacement dictionary.

        """
        sql = "{} LIKE :{}".format(column_name, column_name)
        replacement = {column_name: '%{}%'.format(str(filter_value))}
        return (sql, replacement)

    @classmethod
    def generate_multi_string_sql_includes(cls, column_name, filter_values):
        """Return tuple with sql and replacement.

        This function builds the sql partial and replacement dict for
        an inclusion (LIKE %VALUE%) match for multiple values (OR) against 
        a single column in the database.

        Args:
        column_name (str): Name of column in DB.
        filter_values (list or str): This is what we look for in the column.
            If a string-type object is used for this argument, this function
            behaves as a wrapper for 
            `Utility.generate_single_string_sql_includes()`

        Returns:
            tuple: Item 0 contains the SQL partial string. Item 1 contains
                the replacement dictionary.

        """
        if not isinstance(filter_values, list):
            return cls.generate_single_string_sql_eq(column_name,
                                                     filter_values)
        sql_parts = []
        replacement = {}
        increment = 1
        for filter_value in filter_values:
            colref = "{}{}".format(column_name, str(increment))
            sql_parts.append("{} LIKE :{}".format(column_name, colref))
            replacement[colref] = '%{}%'.format(str(filter_value))
            increment += 1
        sql = "( {} )".format(" OR ".join(sql_parts))
        return (sql, replacement)

    @classmethod
    def generate_single_int_sql_eq(cls, column_name, filter_value):
        """Return tuple with sql and replacement.

        This function builds the sql partial and replacement dict for
        an equivalency match for a single integer against a single
        column in the database.

        Args:
            column_name (str): Name of column in DB.
            filter_value (str or int): This is what we look for in the column.
                Coerced to integer.

        Returns:
            tuple: Item 0 contains the SQL partial string. Item 1 contains
                the replacement dictionary.


        """
        sql = "{} = :{}".format(column_name, column_name)
        replacement = {column_name: int(filter_value)}
        return (sql, replacement)

    @classmethod
    def generate_single_int_sql_gt(cls, column_name, filter_value):
        """Return tuple with sql and replacement.

        This function builds the sql partial and replacement dict for
        a greater-than match for a single integer against a single
        column in the database.

        Args:
            column_name (str): Name of column in DB.
            filter_value (str or int): This is what we look for in the column.
                Coerced to integer.

        Returns:
            tuple: Item 0 contains the SQL partial string. Item 1 contains
                the replacement dictionary.

        """
        column_name_corrected = column_name.replace("_gt", "")
        sql = "{} > :{}".format(column_name_corrected, column_name_corrected)
        replacement = {column_name_corrected: int(filter_value)}
        return (sql, replacement)

    @classmethod
    def generate_single_int_sql_lt(cls, column_name, filter_value):
        """Return tuple with sql and replacement.

        This function builds the sql partial and replacement dict for
        a less-than match for a single integer against a single
        column in the database.

        Args:
            column_name (str): Name of column in DB.
            filter_value (str or int): This is what we look for in the column.
                Coerced to integer.

        Returns:
            tuple: Item 0 contains the SQL partial string. Item 1 contains
                the replacement dictionary.
        """
        column_name_corrected = column_name.replace("_lt", "")
        sql = "{} < :{}".format(column_name_corrected, column_name_corrected)
        replacement = {column_name_corrected: int(filter_value)}
        return (sql, replacement)

    @classmethod
    def generate_single_float_sql_eq(cls, column_name, filter_value):
        """Return tuple with sql and replacement.

        This function builds the sql partial and replacement dict for
        an equivalency match for a single float against a single
        column in the database.

        Args:
            column_name (str): Name of column in DB.
            filter_value (str or float): This is what we look for in the column.
                Coerced to float.

        Returns:
            tuple: Item 0 contains the SQL partial string. Item 1 contains
                the replacement dictionary.


        """
        sql = "{} = :{}".format(column_name, column_name)
        replacement = {column_name: float(filter_value)}
        return (sql, replacement)

    @classmethod
    def generate_single_float_sql_gt(cls, column_name, filter_value):
        """Return tuple with sql and replacement.

        This function builds the sql partial and replacement dict for
        a greater-than match for a single float against a single
        column in the database.

        Args:
            column_name (str): Name of column in DB.
            filter_value (str or float): This is what we look for in the column.
                Coerced to float.

        Returns:
            tuple: Item 0 contains the SQL partial string. Item 1 contains
                the replacement dictionary.

        """
        column_name_corrected = column_name.replace("_gt", "")
        sql = "{} > :{}".format(column_name_corrected, column_name_corrected)
        replacement = {column_name_corrected: float(filter_value)}
        return (sql, replacement)

    @classmethod
    def generate_single_float_sql_lt(cls, column_name, filter_value):
        """Return tuple with sql and replacement.

        This function builds the sql partial and replacement dict for
        a less-than match for a single integer against a single
        column in the database.

        Args:
            column_name (str): Name of column in DB.
            filter_value (str or float): This is what we look for in the column.
                Coerced to float.

        Returns:
            tuple: Item 0 contains the SQL partial string. Item 1 contains
                the replacement dictionary.
        """
        column_name_corrected = column_name.replace("_lt", "")
        sql = "{} < :{}".format(column_name_corrected, column_name_corrected)
        replacement = {column_name_corrected: float(filter_value)}
        return (sql, replacement)

    @classmethod
    def generate_single_tstamp_secs_gt(cls, column_name, filter_value):
        """Return tuple with sql and replacement.

        This function wraps other functions to build the sql partial
        and replacement dict for a greater-than match for a timestamp
        against a single column in the database.

        Args:
            column_name (str): Name of column in DB.
            filter_value (str or int or datetime.datetime): This is what
                 we look for in the column. Sanitized to Unix epoch for DB
                 compatibility.

        Returns:
            tuple: Item 0 contains the SQL partial string. Item 1 contains
                the replacement dictionary.

        """
        mod_filter_value = cls.timestamp_to_dbtime(filter_value)[0]
        return cls.generate_single_int_sql_gt(column_name, mod_filter_value)

    @classmethod
    def generate_single_tstamp_secs_lt(cls, column_name, filter_value):
        """Return tuple with sql and replacement.

        This function wraps other functions to build the sql partial
        and replacement dict for a less-than match for a timestamp
        against a single column in the database.

        Args:
            column_name (str): Name of column in DB.
            filter_value (str or int or datetime.datetime): This is what
                 we look for in the column. Sanitized to Unix epoch for DB
                 compatibility.

        Returns:
            tuple: Item 0 contains the SQL partial string. Item 1 contains
                the replacement dictionary.

        """
        mod_filter_value = cls.timestamp_to_dbtime(filter_value)[0]
        return cls.generate_single_int_sql_lt(column_name, mod_filter_value)

    @classmethod
    def generate_single_tstamp_secs_eq(cls, column_name, filter_value):
        """Return tuple with sql and replacement.

        This function wraps other functions to build the sql partial
        and replacement dict for an equivalency match for a timestamp
        against a single column in the database.

        Args:
            column_name (str): Name of column in DB.
            filter_value (str or int or datetime.datetime): This is what
                 we look for in the column. Sanitized to Unix epoch for DB
                 compatibility.

        Returns:
            tuple: Item 0 contains the SQL partial string. Item 1 contains
                the replacement dictionary.

        """
        mod_filter_value = cls.timestamp_to_dbtime(filter_value)[0]
        return cls.generate_single_int_sql_eq(column_name, mod_filter_value)

    @classmethod
    def is_it_a_string(cls, target):
        """Return boolean True if target is a string, else return False."""

        if sys.version_info < (3, 0):
            result = True if isinstance(target, basestring) else False  # NOQA
        else:
            result = True if isinstance(target, (str, bytes)) else False
        return result

    @classmethod
    def device_field_parser(cls, device):
        """We ensure that a json-parseable string gets passed up the stack."""
        retval = device
        retval = json.dumps(json.loads(device))
        return retval
