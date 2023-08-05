"""
Module for constants used by the wai.test library.
"""
# Attribute of methods that are to be run as tests
IS_TEST_ATTRIBUTE: str = "__test"

# Attribute of test methods which override the default subject initialiser
SUBJECT_ARGS_ATTRIBUTE: str = "__subject_args"

# Attribute of test methods indicating they should be skipped
SKIP_ATTRIBUTE: str = "__skip"

# Attribute of serialisers that the test method will use
SERIALISERS_ATTRIBUTE: str = "__serialisers"
