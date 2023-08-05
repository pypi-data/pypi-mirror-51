Changelog
=========

0.0.1 (2019-08-19)
-------------------

- Initial release

0.0.2 (2019-08-19)
-------------------

- RegressionSerialiser.compare now returns a message saying why the comparison failed,
  or None if the comparison passed, for better failure messages.

0.0.3 (2019-08-19)
-------------------

- Changed the meta-class for all test classes so that it prevents unittest from trying
  to instantiate abstract test-classes. This way standard base-line tests can be written
  as a base-class and all tests in the base class will be run in the sub-class tests, but
  the base-class itself won't try to run (and fail).
