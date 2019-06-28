"""Column type float."""


class ColumnComplexTimestamp(object):
    """Formatter for complex timestamp columns."""

    def __init__(self, sec, usec):
        """Initialize with names for seconds and useconds columns."""
        self.sec_field = sec
        self.usec_field = usec

    @classmethod
    def gen_sql_field(cls, field):
        """Return field name for SQL query."""
        return field

    def gen_select_field(self, field):
        """Return the select SQL select partial for complex timestamp."""
        field_name = field.split("_")[0]
        return "({} + ({} / 1000000.0)) AS {}".format(self.sec_field,
                                                      self.usec_field,
                                                      field_name)

    @classmethod
    def gen_sql_query(cls, field_name):
        """Return SQL query with comparators."""
        comparator_reference = {"lt": ">",
                                "gt": "<",
                                "eq": "="}
        column, comparator = field_name.split("_")
        if comparator == "":
            comparator = "="
        try:
            replacements = {"comparator": comparator_reference[comparator],
                            "column": column}
            query = "{column} {comparator} :{column}".format(**replacements)
            return query
        except KeyError:
            raise ValueError("Invalid comparator {}".format(field_name))
