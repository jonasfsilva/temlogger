|Coverage Status|

TemLogger
=========

**Temlogger** is a library to send logs to ELK, StackDriver(Google Cloud
Logging).

Features
--------

Temlogger gives you:

-  Flexibility to send logs to StackDriver(Google Cloud Logging) or ELK
   (Elastic, Logstash and Kibana).
-  Register events handlers(globally and per logger) to update log entry
   before send to providers.
-  98% test coverage.

Logging Providers
-----------------

-  ``logstash`` (ELK)
-  ``stackdriver`` (Google StackDriver)
-  ``default`` (don't send logs)

Requirements
------------

-  python 3.6+
-  python3-logstash == 0.4.80
-  google-cloud-logging>=1.14.0,<2

Instalation
-----------

::

    pip install temlogger

Usage
-----

Using environment variables:

.. code:: bash

    export TEMLOGGER_PROVIDER='logstash'
    export TEMLOGGER_URL='localhost'
    export TEMLOGGER_PORT='5000'
    export TEMLOGGER_ENVIRONMENT='staging'

.. code:: python

    import sys
    import temlogger

    test_logger = temlogger.getLogger('python-logstash-logger')

    test_logger.error('python-logstash: test logstash error message.')
    test_logger.info('python-logstash: test logstash info message.')
    test_logger.warning('python-logstash: test logstash warning message.')

    # add extra field to logstash message
    extra = {
        'test_string': 'python version: ' + repr(sys.version_info),
        'test_boolean': True,
        'test_dict': {'a': 1, 'b': 'c'},
        'test_float': 1.23,
        'test_integer': 123,
        'test_list': [1, 2, '3'],
    }
    test_logger.info('temlogger: test with extra fields', extra=extra)

Example passing parameters directly to temlogger:

.. code:: python

    import sys
    import temlogger

    temlogger.config.set_provider('logstash')
    temlogger.config.set_url('localhost')
    temlogger.config.set_port(5000)
    temlogger.config.set_environment('staging')

    test_logger = temlogger.getLogger('python-logstash-logger')

    test_logger.info('python-logstash: test logstash info message.')

    # add extra field to logstash message
    extra = {
        'test_string': 'python version: ' + repr(sys.version_info),
        'test_boolean': True,
        'test_dict': {'a': 1, 'b': 'c'},
        'test_float': 1.23,
        'test_integer': 123,
        'test_list': [1, 2, '3'],
    }
    test_logger.info('temlogger: test with extra fields', extra=extra)

Example with StackDriver
~~~~~~~~~~~~~~~~~~~~~~~~

`Documentation of how set GOOGLE\_APPLICATION\_CREDENTIALS environment
variable. <https://cloud.google.com/docs/authentication/getting-started>`__

.. code:: bash

    export TEMLOGGER_PROVIDER='stackdriver'
    export GOOGLE_APPLICATION_CREDENTIALS='<path to json>'

.. code:: python

    import sys
    import temlogger

    test_logger = temlogger.getLogger('python-stackdriver-logger')

    test_logger.info('python-stackdriver: test stackdriver info message.')

    # add extra field to stackdriver message
    extra = {
        'test_string': 'python version: ' + repr(sys.version_info),
        'test_boolean': True,
        'test_dict': {'a': 1, 'b': 'c'},
        'test_float': 1.23,
        'test_integer': 123,
        'test_list': [1, 2, '3'],
    }
    test_logger.info('temlogger: test with extra fields', extra=extra)

Using with Django
~~~~~~~~~~~~~~~~~

Modify your ``settings.py`` to integrate temlogger with Django's
logging:

.. code:: python

    import temlogger

    host = 'localhost'

    temlogger.config.set_provider('logstash')
    temlogger.config.set_url('localhost')
    temlogger.config.set_port(5000)
    temlogger.config.set_environment('staging')

Then in others files such as ``views.py``,\ ``models.py`` you can use in
this way:

.. code:: python

    import temlogger

    test_logger = temlogger.getLogger('python-logger')

Event Handlers
--------------

This functionality allow register handlers before send log to Logging
Providers.

Register event handlers globally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Is recommended initialize event handlers early as possible, for example
in ``settings.py`` for django. The below example shows how register a
handler ``add_tracker_id_to_message`` globally.

.. code:: python

    import temlogger

    temlogger.config.set_provider('logstash')
    temlogger.config.setup_event_handlers([
        'temlogger.tests.base.add_tracker_id_to_message',
    ])

    logger = temlogger.getLogger('python-logger')

    extra = {
        'app_name': 'tembici'
    }

    logger.info('test with extra fields', extra=extra)

Register event handlers per logger
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The below example shows how register a handler ``add_user_id_key`` for
one logger.

.. code:: python

    import temlogger

    def add_user_id_key(message):
        message['user_id'] = 'User Id'
        return message

    temlogger.config.set_provider('logstash')

    logger = temlogger.getLogger('python-logger', event_handlers=[
        'temlogger.tests.base.add_tracker_id_to_message',
        add_user_id_key
    ])
    extra = {
        'app_name': 'tembici'
    }

    logger.info('test with extra fields', extra=extra)

.. |Coverage Status| image:: https://codecov.io/gh/tembici/temlogger/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/tembici/temlogger
