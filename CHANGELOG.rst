Changelog
=========


v2019.03.01
-----------
- Add license file now that it's a submodule. [Mike Kershaw / Dragorn]
- Minor commit to trigger mirror. [Mike Kershaw / Dragorn]


v5.1.0 (2019-02-16)
-------------------

New
~~~
- Include version-specific converters. [Ash Wilson]

  This allows us to, for instance, ensure that all
  GPS coordinates are returned as float-type values,
  across all database versions, no matter how they
  were originally stored in the database.

  Closes #22
- Support v4 as well as v5 Kismet databases. [Ash Wilson]

  Closes #19
- Add ``kismet_log_devices_to_filebeat_json``. [Ash Wilson]

  Closes #17


v5.0.0 (2019-02-12)
-------------------

New
~~~
- Support v5 schema. [Ash Wilson]


v4.0.3 (2019-02-05)
-------------------

Changes
~~~~~~~
- Updated docs, added simplekml requirement. [Ash Wilson]

  Closes #8
  Closes #7
- Adding docs to be built by Sphinx. [Ash Wilson]
- Scripts automatically install with Python package. [Ash Wilson]

  Added generator function yield_rows() to all abstractions.
- Initial working commit. [Ash Wilson]

  In order to run integration tests, you need a
  Kismet db at tests/assets/testdata.kismet.


