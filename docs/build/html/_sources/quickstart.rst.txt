Quickstart
==========

Construct and send a notification
---------------------------------

We can combine the general object models for the notify patterns with the client module to construct
and then send a notification.

The following code example constructs an `Announce Review` notification with some basic information.
See https://coar-notify.net/specification/1.0.0/announce-review/ for the specification of this
notification.

We create the `AnnounceReview` object, and then create the `NotifyActor`, `NotifyObject`, `NotifyService` objects
for the key parts of the notification, and attach them to the `AnnounceReview` object.

Finally, we create a `COARNotifyClient` object and send the notification to the target inbox.

.. code-block:: python

    from coarnotify.client import COARNotifyClient
    from coarnotify.models import (
        AnnounceReview,
        NotifyActor,
        NotifyObject,
        NotifyService
    )
    from coarnotify.activitystreams2 import ActivityStreamsTypes

    announcement = AnnounceReview()

    actor = NotifyActor()
    actor.id = "https://cottagelabs.com/"
    actor.name = "My Review Service"

    obj = NotifyObject()
    obj.type = ActivityStreamsTypes.DOCUMENT
    obj.cite_as = "https://dx.doi.org/10.12345/6789"

    origin = NotifyService()
    origin.id = "https://cottagelabs.com/"
    origin.inbox = "https://cottagelabs.com/inbox"

    target = NotifyService()
    target.id = "https://example.com/"
    target.inbox = "https://example.com/inbox"

    announcement.actor = actor
    announcement.object = obj
    announcement.origin = origin
    announcement.target = target

    client = COARNotifyClient()
    response = client.send(announcement, target.inbox)