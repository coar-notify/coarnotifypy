"""
This module contains all the test infrastructure.

For the purposes of conciseness, the test code is mostly excluded from the auto-documentation.

The test code is structured as follows:

- `fixtures` contains test fixtures and factories for generating fixtures
- `integration` contains integration tests for the library.  These depend on a running server, and there is a test server provided
- `mocks` contains mock objects for testing
- `server` contains the test server, and documentation for this is generated and available on the docsite
- `unit` contains unit tests for the library

For information on running the integration and unit tests, see :doc:`/dev`.
"""