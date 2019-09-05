"""Column type float."""


class ColumnFloat(object):
    """Formatter for float-type columns."""

    @classmethod
    def gen_sql_query(cls, field_name, field_query, value):
        """Return SQL query partial for column, including comparator."""
        comparator_reference = {"lt": "<",
                                "gt": ">",
                                "eq": "="}
        comparator = field_query.replace("{}_".format(field_name), "")
        if comparator == "":
            comparator = "="
        try:
            query = "{} {} {}".format(field_name,
                                      comparator_reference[comparator],
                                      value)
            return query
        except KeyError:
            raise ValueError("Invalid comparator {}".format(field_query))
