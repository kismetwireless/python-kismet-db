from kismetdb.column_string import ColumnString


class TestUnitColumnString(object):
    def test_unit_column_string_gen_sql_query_like(self):
        parser = ColumnString()
        parsed = parser.gen_sql_query("fieldname", "fieldname_like", "val")
        expected = "fieldname LIKE '%val%'"
        assert parsed == expected

    def test_unit_column_string_gen_sql_query_single(self):
        parser = ColumnString()
        parsed = parser.gen_sql_query("fieldname", "fieldname_like", "nobody")
        expected = "fieldname LIKE '%nobody%'"
        assert parsed == expected

    def test_unit_column_string_gen_sql_query_multi(self):
        parser = ColumnString()
        parsed = parser.gen_sql_query("fieldname", "fieldname_like",
                                      ["whatever", "nobody"])
        expected = "(fieldname LIKE '%whatever%' OR fieldname LIKE '%nobody%')"
        assert parsed == expected

    def test_unit_column_string_gen_sql_query_multi_eq(self):
        parser = ColumnString()
        parsed = parser.gen_sql_query("fieldname", "fieldname_eq",
                                      ["whatever", "nobody"])
        expected = "(fieldname = 'whatever' OR fieldname = 'nobody')"
        assert parsed == expected
