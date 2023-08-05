# wai-test
Python library for unit tests.

## Testing Philosophy
This test library is designed around the testing of an individual `subject`,
where a `subject` is usually either a class or a function. For each `subject`
to be tested, one or more test classes should be written, each of which
derives from the base `AbstractTest` class.

Each test class defines the `subject` it tests, and a number of tests for
that subject to pass. Each test is a method of the test class, configured
with some of the decorators provided by this library. Furthermore, common
configuration between tests can be provided by overriding class methods of
the base `AbstractTest` class.

---

## Test Types
There are 3 types of test currently supported by this library: standard tests,
regression tests, and exception tests.

### Standard Tests
A standard test involves testing the subject against a known value. It is
specified by decorating the test method with the `@Test` decorator. The method
should use the test subject to produce some value, which is then compared
to the expected value with one of the `unittest` assertions via the `self`
reference, e.g. `self.assertEqual(subject_value, expected_value, msg)`.

### Regression Tests
A regression test involves comparing the subject to a previously-produced
version of the subject. A regression test is specified by marking the test
subject with the `@RegressionTest` decorator. The test method should return
a dictionary from regression labels to the tested value for that label. This
way multiple related values can be regression-tested at once.

Because a regression test must have a past value to compare the current value
against, regression results are saved to disk. In order to facilitate this,
result serialisers which can write the result to disk need to be specified.
This can be done either at a test-class level (providing common serialisers
for all tests) and/or at a per-test level, allowing specific serialisation
for certain tests.

### Exception Tests
Exception tests are similar to standard tests, but in that they should not
compare a result via value, instead raising an exception to determine pass/fail
status. Exception tests can be specified by adding the `@ExceptionTest` decorator
to the test method.

---

## Decorators
Decorators are used to define the type of test that a test method performs,
as well as specify test-specific configuration for the test.

### Test Type Decorators
These decorators specify what type of test the decorated method defines.
Only one of these decorators should be applied to each test method.

* **`@Test`** - Specifies a standard test method. Takes no arguments.
* **`@RegressionTest`** - Specifies a regression test method. Takes no
                          arguments.
* **`@ExceptionTest`** - Specifies an exception test method. Takes as
                         argument a series of exception types. The test will
                         pass if any of the given types of exception is thrown,
                         and fail if not.
                         
### Test-Specfic Configuration Decorators
These decorations configure the decorated test in some way.

* **`@Skip`** - Specifies that this test should be skipped.
* **`@SubjectArgs`** - Overrides the default arguments to the test subject
                       for this test. Takes the same arguments as the subject,
                       and forwards them directly. If this decorator is specified
                       multiple times on the same method, only the top-most decorator
                       will apply.
* **`@ExpectedFailure`** - Marks the decorated method as a test that is
                           expected to fail. Inverts the success criteria for
                           this test. I.e. A test that passes under normal
                           conditions is considered to have failed, and a test
                           that fails under normal conditions is considered to
                           have passed.
* **`@WithSerialiser`** - This test sets the serialiser for a given result-type
                          for the decorated test only. Can be used to override
                          the common serialisers for the test class. Takes as
                          arguments the type of result being serialised, and the
                          serialiser to use for serialising that type in this
                          test method.

---

## Common Test Configuration
Defining common configuration for all tests in a given test class is done by
overriding specific class methods of the `AbstractTest` base-class.

* **`subject_type`** - This method specifies the subject being tested by this
                       test-class. It should return a callable to use to
                       instantiate a test-subject, usually the class or the
                       function itself.
* **`common_resources`** - This method should return any common resources that
                           are required by all test methods in the test-class.
                           The resources will be passed to each test method
                           as positional arguments, so can be captured via
                           the `*args` pattern or by unpacking into individual
                           named arguments.
* **`common_serialisers`** - This method should return a dictionary from types
                             to serialisers for those types. This serialiser
                             mapping is added to the basic serialisers for string
                             and bytes (possibly overriding them). Individual tests
                             can override or define additional serialisers with the
                             `@WithSerialiser` decorator.
* **`common_arguments`** - This method should return the positional and keyword
                           arguments that will be supplied to the subject on
                           instantiation for each test. By default no arguments
                           are supplied. Can be overridden on a per-test basis
                           via the `@SubjectArgs` decorator.
                           
---
## Serialisers
Serialisers are used by regression tests to save a regression reference to disk, and
to load it again in future to compare to the results of future runs of the test. Two
basic serialisers are provided with the library, `StringSerialiser` and
`BytesSerialiser`. Custom serialisers can be defined by sub-classing the
`RegressionSerialiser` base-class. Serialisers can also define their own notion of
equality between the result of the current test and the reference value by overriding
the `compare` method.

---

## Test Method Signatures
All tests in a test-class should have one of the following signatures.

### Standard Test
```python
@Test
... additional decorators ...
def standard_test_name(self,
                       subject,
                       named_resource_1, named_resource_2,
                       *unnamed_resources):
    ... test code ...
    
    self.assertSomething(some_value)

```

### Regression Test
```python
@RegressionTest
... additional decorators ...
def regression_test_name(self,
                         subject,
                         named_resource_1, named_resource_2,
                         *unnamed_resources):
    ... test code ...
    
    return {
        "regression_name_1": regression_value_1,
        "regression_name_2": regression_value_2,
        ... additional regressions ...
    }

```

### Exception Test
```python
@ExceptionTest(ExceptionType1, ExceptionType2, ...)
... additional decorators ...
def exception_test_name(self,
                        subject,
                        named_resource_1, named_resource_2,
                        *unnamed_resources):
    ... test code ...
    
    if condition1:
        raise ExceptionType1(msg)
        
    ... more test code ..
    
    if condition2:
        raise ExceptionType2(msg)
        
    ...

```

---

## Example
The following is an example of a basic class and the setup that will test it.

The class being tested:
```python
class MyClass:
    def __init__(self, value: int = 0):
        self.value = value

    def transform(self, x: int, y: int) -> int:
        if y < 0:
            raise ValueError("y can't be less than 0")

        return x + y + self.value


```

A couple of different serialiser for integers:
```python
class IntSerialiser(RegressionSerialiser[int]):
    @classmethod
    def binary(cls) -> bool:
        return False

    @classmethod
    def extension(cls) -> str:
        return "int"

    @classmethod
    def serialise(cls, result: int, file: IO[str]):
        file.write(str(result))

    @classmethod
    def deserialise(cls, file: IO[str]) -> int:
        return int(file.read())
        
        
class IntSerialiser2(IntSerialiser):
    @classmethod
    def serialise(cls, result: int, file: IO[str]):
        super().serialise(result + 1, file)

    @classmethod
    def deserialise(cls, file: IO[str]) -> int:
        return super().deserialise(file) - 1

```

The test class:
```python
class MyClassTest(AbstractTest):
    @classmethod
    def subject_type(cls):
        return MyClass  # Testing the MyClass class

    @classmethod
    def common_resources(cls):
        return 1,  # All tests take an initial value of 1

    @classmethod
    def common_serialisers(cls):
        return {
            int: IntSerialiser  # Default serialiser for int values
        }

    @classmethod
    def common_arguments(cls):
        return (15,), {}  # Most tests will initialise MyClass with 15

    # Standard test with no additional decorators
    @Test
    def standard_test(self, subject: MyClass, x: int):
        self.assertEqual(subject.transform(x, 2),
                         18)

    # Same as above, but with the wrong result value
    # so we expect it to fail
    @Test
    @ExpectedFailure
    def standard_test_failure(self, subject: MyClass, x: int):
        self.assertEqual(subject.transform(x, 2),
                         17)

    # Same as above, but overriding subject arguments
    @Test
    @SubjectArgs(10)
    def standard_test_with_10(self, subject: MyClass, x: int):
        self.assertEqual(subject.transform(x, 2),
                         13)

    # Exception test, make sure MyClass raises ValueError
    # on negative y
    @ExceptionTest(ValueError)
    def exception_test(self, subject: MyClass, x: int):
        return subject.transform(x, -1)

    # Regression test with two regression outputs
    @RegressionTest
    def regression_test(self, subject: MyClass, x: int):
        return {
            "transform5": subject.transform(x, 5),
            "transform2": subject.transform(x, 2)
        }

    # Same as above, but overriding the serialiser
    @RegressionTest
    @WithSerialiser(int, IntSerialiser2)
    def regression_test_2(self, subject: MyClass, x: int):
        return {
            "transform5": subject.transform(x, 5),
            "transform2": subject.transform(x, 2)
        }

```