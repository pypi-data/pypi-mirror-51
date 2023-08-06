Release history and notes
=========================
`Sequence based identifiers
<http://en.wikipedia.org/wiki/Software_versioning#Sequence-based_identifiers>`_
are used for versioning (schema follows below):

.. code-block:: text

    major.minor[.revision]

- It's always safe to upgrade within the same minor version (for example, from
  0.3 to 0.3.4).
- Minor version changes might be backwards incompatible. Read the
  release notes carefully before upgrading (for example, when upgrading from
  0.3.4 to 0.4).
- All backwards incompatible changes are mentioned in this document.

0.0.5
-----
2019-08-30

- Implemented custom lookups in favour of a single ``lookup`` attribute.
- Updated tests.

0.0.4
-----
2019-08-28

- Fixed travis config (moved to elasticsearch 6.x on travis, since 7.x was
  causing problems).
- Fixes in setup.py.

0.0.3
-----
2019-08-26

- Documentation fixes.
- Add test suite and initial tests for filter backend and search backend.

0.0.2
-----
2019-08-25

- Added dynamic lookup generation for the filter backend.
- Working lookup param argument handling on the schema (filter backend).

0.0.1
-----
2019-08-24

- Initial alpha release.
