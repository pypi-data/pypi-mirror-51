Control error handler
=====================

Error handler for flask with sending exceptions to control service.

Installing
----------

From pypi: ::

    $ pip install control_error_handler

or from source: ::

    $ python setup.py install

Quick start
-----------

**Add to flask app.configs:** ::

    CONTROL_EXCEPTION_URL = 'http://localhost:5000/api/monitoring/send-exception/'
    SEND_EXCEPTION_TO_CONTROL = True


Init control handler in `__init__.py` on flask project: ::

    from flask import Flask
    from control_error_handler.error_handler import ControlHandler

    app = Flask(__name__)

    ControlHandler(app)

**Use ES54Exception:** ::

    from control_error_handler.exceptions import ES54Exception

    raise ES54Exception('Some error...', ext_data={'any_action': True})


Build package
-------------
::

    $ python setup.py bdist_wheel

Upload to PYPI
--------------
::

    $ twine upload dist/*