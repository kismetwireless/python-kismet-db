Updating
========

.. toctree::

Over time, we expect that the database schema will change. To make
transitioning to a new schema easier, each object is defined with the expected
database columns defined in a class variable named ``column_names``. The bulk
data field (which contains json or raw packet capture) is in a class variable
named ``bulk_data_field``. The ``valid_kwargs`` class variable is used in
parsing keyword arguments for filtering in the SQL query. These items tie into
functions that live in the Utility class, and are used for forming the SQL
that's used to query the Kismet DB.

This tool follows calendar versioning, and new versions support DB schemas as
far back as v4.

As the database schema changes, the changes required to support a new version
of the db will be required on a per-object basis. The following object
attributes are used to contain version-specific schema information:

* ``field_defaults``: This is used to force a default value for fields that \
are not found in older-than-current versions of the Kismet DB.
* ``converters_reference``: This allows us to specify a converter so that if \
the data type changes between schema versions, we can force the older DB type \
to match the current DB version's type.
* ``column_reference``: This describes the expected columns for each supported \
version of the kismet DB
