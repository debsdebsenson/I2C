# Notes about the tests

## Run the tests

* The tests can be run from the I2C/ folder by typing:

```Python
pytest
```

or:

```Python
pytest test/
```

## Other

* To be able to run these tests the *app/* folders name had to be changed to *appI2C/*. Otherwise it would be stated that app is not a module.

* Also an __init__.py file had to be placed to the I2C/test/ folder. To make the import within the test_xyz.py file possible.