Test Server
===========

This library comes bundled with an extremely basic test server (using Flask) to allow you to send notifications as if they
were going to a real inbox.

The test server is available in ``coarnotify/test/server`` in the source code.

In order to use the test server you will need to install the ``test`` dependencies

.. code-block:: console

    pip install .[test]

Configuring the Test Server
---------------------------

The test server's default settings are in ``coarnotify/test/server/settings.py``.

You can see the module documentation for this in :py:mod:`coarnotify.test.server.settings`.

Default configuration can be overridden by providing your own settings file as an environment variable ``COARNOTIFY_SETTINGS``.

The main things to override are:

* STORE_DIR: the directory to store the notifications.  You MUST supply your own path
* PORT: the port to run the server on.  Default is 5005

Create a local config file called something like ``local.cfg`` containing those properties

.. code-block:: python

    STORE_DIR = '/path/to/store/notifications'
    PORT = 5005

The other properties you may want to override are:

* RESPONSE_STATUS: which HTTP status code to respond with.  Valid values are `201` (Created) and `202` (Accepted)
* VALIDATE_INCOMING: should the inbox attempt to validate incoming notifications.  Default is `True`


Running and using the Test Server
---------------------------------

Start the server with the following command:

.. code-block:: console

    COARNOTIFY_SETTINGS=local.cfg; python coarnotify/test/server/inbox.py

You can then send notifications to the server using the client library, and set the target inbox
to ``http://localhost:5005/inbox``.

The server will store the notifications in the directory you specified in the settings.

Notifications are stored as JSON files in the directory, with the following naming scheme

``{datestamp}_{time}_{uuid}.json``

Where the ``uuid`` is the server's id, not the id supplied in the notification.  If you have the server set to
create notifications (as opposed to accept) then this id will be returned to you in the ``Location`` header of
the server response.

.. code-block:: python

    client = COARNotifyClient("http://localhost:5005/inbox")
    notification = RequestReview(data)
    resp = client.send(ae)
    print(resp.action)
    print(resp.location)

PyCharm Debugging
^^^^^^^^^^^^^^^^^

The test server can quickly be set up in debug mode for PyCharm by adding ``-d`` to the startup command

.. code-block:: console

    COARNOTIFY_SETTINGS=local.cfg; python coarnotify/test/server/inbox.py -d