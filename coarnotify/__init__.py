"""
This is the base of the `coarnotifypy` module.

In here you will find
a full set of model objects for all the Notify Patterns documented in
https://coar-notify.net/specification/1.0.1/

You will also find a client library that will allow you to send notifications
to an inbox, and a server library that will allow you to write a service
binding to your own systems to receive notifications via an inbox.

There are also unit tests demonstrating the various features of the system,
integration tests which can be run against a remote inbox, and a
stand-alone inbox you can use for local testing.
"""

__version__ = "1.0.1.3"