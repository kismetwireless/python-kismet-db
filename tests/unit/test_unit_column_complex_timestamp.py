from kismetdb.column_complex_timestamp import ColumnComplexTimestamp


class TestUnitColumnComplexTimestamp(object):
    def unit_column_string_gen_sel_field(self):
        cct_parser = ColumnComplexTimestamp("seconds", "useconds")
        parsed = cct_parser.gen_select_field("fieldname")
        expected = "(seconds + (useconds / 1000000.0)) AS fieldname"
        assert parsed == expected

    def unit_column_string_gen_sql_query(self):
        cct_parser = ColumnComplexTimestamp("seconds", "useconds")
        parsed = cct_parser.gen_sql_query("fieldname", "fieldname_gt", "14.12")
        expected = "fieldname < 14.12"
        assert parsed == expected
