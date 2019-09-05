"""Column type float."""

from .utility import Utility


class ColumnString(object):
    """Formatter for string-type columns."""

    @classmethod
    def gen_sql_field(cls, field):
        """Return field name for SQL queries."""
        return field

    @classmethod
    def gen_select_field(cls, field):
        """Return select field for queries."""
        return field

    def gen_sql_query(self, field_name, field_query, value):
        """Return SQL query partial."""
        comparator = field_query.replace("{}_".format(field_name), "")
        gen_field_name = self.gen_sql_field(field_name)
        if comparator == "like":
            if Utility.is_it_a_string(value):
                sql = "{} LIKE '%{}%'".format(gen_field_name, value)
            elif isinstance(value, list):
                vals = []
                for val in value:
                    vals.append("{} LIKE '%{}%'".format(gen_field_name, val))
                sql = "({})".format(" OR ".join(vals))
            else:
                msg = ("Wrong type for value: expected string or list, "
                       "got {}".format(type(value)))
                raise TypeError(msg)
        elif comparator == 'eq':
            if Utility.is_it_a_string(value):
                sql = "{} = '{}'".format(gen_field_name, value)
            elif isinstance(value, list):
                vals = []
                for val in value:
                    vals.append("{} = '{}'".format(gen_field_name, val))
                sql = "({})".format(" OR ".join(vals))
            else:
                msg = ("Wrong type for value: expected string or list, "
                       "got {}".format(type(value)))
                raise TypeError(msg)
        else:
            raise ValueError("Invalid comparator {}".format(field_query))
        return sql
