Changelog
=========

v2019.05.05
-----------
- Handle missing SYSTEM snapshots during Kismet processing [Mike Kershaw / Dragorn]

v2019.05.04
-----------
- Add DataPackets handler [Mike Kershaw / Dragorn]

v2019.05.03
-----------
- Fix JSON blob type extractor for DataSources [Ash Wilson]

  Closes #3
- Add JSON blob type extractor for Snapshots [Mike Kershaw / Dragorn]

v2019.05.02
-----------
- Make RST doc levels happy. [Mike Kershaw / Dragorn]
- Hopefully make docs happy. [Mike Kershaw / Dragorn]
- Add self to docs. [Mike Kershaw / Dragorn]
- Fix changelog. [Mike Kershaw / Dragorn]
- Fix RST? [Mike Kershaw / Dragorn]
- Docs. [Mike Kershaw / Dragorn]
- Ignore vim. [Mike Kershaw / Dragorn]
- Enable classes Bump version Add integer version. [Mike Kershaw /
  Dragorn]
- Add snapshots class Add kismet class for server info derived from
  snapshots. [Mike Kershaw / Dragorn]
- Add float comparators Add string LIKE comparators. [Mike Kershaw /
  Dragorn]
- Add defaults for db6. [Mike Kershaw / Dragorn]
- Add support for database version 6. [Mike Kershaw / Dragorn]
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


