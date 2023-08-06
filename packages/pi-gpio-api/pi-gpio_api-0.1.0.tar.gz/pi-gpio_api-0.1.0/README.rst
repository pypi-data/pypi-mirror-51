Raspberry Pi GPIO Api
=====================

API to access Raspberry Pi GPIO based on Python, Flask & Rpi.GPIO library. The software launches an web API that controls IO pins using the `Rpi.GPIO` library.

This was meant to be used to remotely control relays, thus, it only sets the outputs as high or low.

The pins are referenced through their number printed in the board. Further information about pins can be found `here <https://pinout.xyz/>`_.


API
---

+--------------------------+---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Route                    | Request | Description                                                                                                                                                                                                                                       |
+==========================+=========+===================================================================================================================================================================================================================================================+
| `/api/gpio/`             | GET     | Returns a json object with the status of all pins                                                                                                                                                                                                 |
+--------------------------+---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| `/api/gpio/power/<PIN>`  | GET     | Returns a json object with the power pins position and description (5V, 3V3, GND)                                                                                                                                                                 |
+--------------------------+---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| `/api/gpio/io/<PIN>`     | GET     | Returns a json object with de description and status for a pin. If no pin number is given, returns the status of all io pins.                                                                                                                     |
+--------------------------+---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| `/api/gpio/io/<PIN>`     | POST    | Sets up a particular pin. Receives a json object that must have the keys `type` and `value`. `type`  must be a string with either `input` or `output` and `value` must be a boolean, with the status to write to the channel of the request.      |
+--------------------------+---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+


Sample response
---------------

.. code-block:: sh

    {
        "io": [
            {
                "pin": 3,
                "pin_function": "IO",
                "pin_state": 1
            },
           ...],

        "power_pins": [
            {
                "pin": 1,
                "pin_function": "3V3 Power"
            },
           ...]
    }


Installation
------------

Latest release through PyPI:

.. code-block:: sh

    $ pip install pi_gpio_api

Development version:

.. code-block:: sh

    $ git clone git@github.com:jcapona/pi-gpio-api.git
    $ cd pi-gpio-api
    $ pip install -e .


CLI
---

The api can be run as a daemon using the `gpioapi` command in the Raspberry Pi shell.

.. code-block:: sh

    $ gpioapi -h
    usage: gpioapi [-h] [-H HOST] [-p PORT] command

    GPIO web API controller
    
    positional arguments:
      command               Control process: start, stop, restart, status
    
    optional arguments:
      -h, --help            show this help message and exit
      -H HOST, --host HOST  host where the web server will be listening
      -p PORT, --port PORT  port where the web server will be listening

This way, the API can be launched through `gpioapi start` and stopped through `gpioapi stop`.


Use as a library
----------------

In a python shell:

.. code-block:: python

    >>> import pi_gpio_api
    >>> pi_gpio_api.app.run(host='0.0.0.0', port=5000)

This will launch a server that listens requests on the given host & port.


Contribution
------------

Feel free to open issues, report bugs or open pull requests.
