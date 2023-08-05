Heartbeat module for Flask applications and OAREPO Invenio repository
========================================================================

A heartbeat module for flask and OAREPO Invenio. It provides 3 endpoints:

* ``.well-known/heartbeat/readiness``

* ``.well-known/heartbeat/liveliness``

* ``.well-known/heartbeat/environ``



``.well-known/heartbeat/readiness``
------------------------------------

This endpoint returns HTTP status 200 if the server is ready for user requests or 500
if the server is not yet ready.

At the same time, it returns a payload explaining what is not yet ready/what went wrong:

.. code:: json

    {
        "status": false,
        "checks": {
            "Database": {
                "status": false,
                "message": "Error accessing database"
            }
        }
    }

This endpoint should be called as Kubernetes readiness probe

*Note:* the result is extensible, ignore unknown keys

**Signals:**

A ``oarepo_heartbeat.readiness_probe`` signal (with name ``oarepo.probe.readiness``)
is called during the readiness processing. Signal handler should return a response
in the form of a tuple ``(name, status, data)``. The ``status`` is the ``logical and``
of returned statuses and data are passed inside the element. The following section
will be added to the response:

.. code:: python

    "checks": {
        "returned_name": {
            "status": "returned_status",
            **returned_data
        }
    }


**Initial implementation:**

When no signals are attached, the probe always returns HTTP 200, thus checking
if the server is running.

``.well-known/heartbeat/liveliness``
------------------------------------

This endpoint returns HTTP status 200 if the server is functioning correctly or 500
if the server has a problem.

At the same time, it returns a payload explaining what went wrong in the same format as in
readiness probe:

.. code:: json

    {
        "status": false,
        "checks": {
            "Database": {
                "status": false,
                "message": "Error accessing database"
            }
        }
    }

This endpoint should be called as Kubernetes liveliness probe

*Note:* the result is extensible, ignore unknown keys

**Signals:**

A ``oarepo_heartbeat.liveliness_probe`` signal (with name ``oarepo.probe.liveliness``)
is called during the readiness processing. Signal handler should return a response
in the form of a tuple ``(name, status, data)``. The ``status`` is the ``logical and``
of returned statuses and data are passed inside the element.

**Initial implementation:**

When no signals are attached, the probe always returns HTTP 200, thus checking
if the server is running.

``.well-known/heartbeat/environ``
------------------------------------

Endpoint returning the runtime environment of the server. The result contains at least
a set of libraries present in the virtualenv and their versions.

.. code:: json

    {
        "status": true,
        "libraries": {
            "oarepo": {
                "conflicts": null,
                "version": "3.1.1"
            }
        },
        "python": [3, 6, 1]
    }

*Note:* the result is extensible, ignore unknown keys

**Signals:**

A ``oarepo_heartbeat.environ_probe`` signal (with name ``oarepo.probe.environ``)
is called during the readiness processing. Signal handler should return a response
as a tuple ``(status, {data})``. The ``status`` is the ``logical and`` of returned statuses
and the data are merged into one dictionary.

**Initial implementation:**

When no signals are attached, the probe always returns HTTP 200 with json containing
``libraries`` and ``python`` elements as shown above.

Invenio usage:
==============

To use this library on invenio, do not forget to add it to setup's blueprints
and define your own readiness & liveliness signal handlers as needed (for example,
checking database, ES connectivity):

.. code:: python

    'invenio_base.blueprints': [
        'oarepo-heartbeat = oarepo_heartbeat.views:blueprint',
    ],


Flask usage:
==============

Register the ``oarepo_heartbeat.views:blueprint`` blueprint to your flask
application and write your own readiness and liveliness signals as needed.
