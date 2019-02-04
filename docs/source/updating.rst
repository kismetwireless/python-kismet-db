Updating
========

.. toctree::

Over time, we expect that the database schema will change. To make
transitioning to a new schema easier, each object is defined with the expected
database defined as a class variable named ``column_names``, and the bulk data
field (which contains json or raw packet capture) is in a class variable named
``bulk_data_field``. The ``valid_kwargs`` class variable is used in parsing
keyword arguments for filtering in the SQL query. These items tie into
functions that live in the Utility class, and are used for forming the SQL
that's used to query the Kismet DB.

This tool follows semantic versioning and the major version of this tool
should match the version of the installed Kismet DB (found in the ``KISMET``
table, ``db_version`` column). Minor version is incremented for added features
within the current major version (perhaps added scripts or support for
additional tables).

Ideally, if the schema for any table changes, the only required change will be
in the ``column_names`` or ``bulk_data_field`` variables in the class
definition. If more query parameters are required, those can be added via the
``valid_kwargs`` class variable, and tied into the appropriate method in
the Utility class.
