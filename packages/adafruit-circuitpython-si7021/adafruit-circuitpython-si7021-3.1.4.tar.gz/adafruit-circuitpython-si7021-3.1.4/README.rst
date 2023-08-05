Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-si7021/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/si7021/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://travis-ci.com/adafruit/Adafruit_CircuitPython_SI7021.svg?branch=master
    :target: https://travis-ci.com/adafruit/Adafruit_CircuitPython_SI7021
    :alt: Build Status

CircuitPython module for use with the SI7021 Temperature and Humidity Sensor.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Notes
===========

Of course, you must import the library to use it:

.. code:: python

    import adafruit_si7021

This driver takes an instantiated and active I2C object (from the ``busio`` or
the ``bitbangio`` library) as an argument to its constructor.  The way to create
an I2C object depends on the board you are using. For boards with labeled SCL
and SDA pins, you can:

.. code:: python

    from busio import I2C
    from board import SCL, SDA

    i2c = I2C(SCL, SDA)

Once you have created the I2C interface object, you can use it to instantiate
the sensor object:

.. code:: python

    sensor = adafruit_si7021.SI7021(i2c)


And then you can start measuring the temperature and humidity:

.. code:: python

    print(sensor.temperature)
    print(sensor.relative_humidity)


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_SI7021/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Building locally
================

To build this library locally you'll need to install the
`circuitpython-build-tools <https://github.com/adafruit/circuitpython-build-tools>`_ package.

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install circuitpython-build-tools

Once installed, make sure you are in the virtual environment:

.. code-block:: shell

    source .env/bin/activate

Then run the build:

.. code-block:: shell

    circuitpython-build-bundles --filename_prefix adafruit-circuitpython-si7021 --library_location .

Sphinx documentation
-----------------------

Sphinx is used to build the documentation based on rST files and comments in the code. First,
install dependencies (feel free to reuse the virtual environment from above):

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install Sphinx sphinx-rtd-theme

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.