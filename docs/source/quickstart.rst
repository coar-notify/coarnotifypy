Quickstart
==========

Construct and send a notification
---------------------------------

We can combine the general object models for the notify patterns with the client module to construct
and then send a notification.

The following code example constructs an ``Announce Review`` notification with some basic information.
See https://coar-notify.net/specification/1.0.0/announce-review/ for the specification of this
notification.

We create the ``AnnounceReview`` object, and then create the ``NotifyActor``, ``NotifyObject``, ``NotifyService`` objects
for the key parts of the notification, and attach them to the ``AnnounceReview`` object.

Finally, we create a ``COARNotifyClient`` object and send the notification to the target inbox.

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

Parse a raw notification
------------------------

We can receive and parse a raw notification using the object factory :py:mod:`coarnotify.factory`.

Suppose we have a basic notification which consists of the following string:

.. code-block:: json

    {
      "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://coar-notify.net"
      ],
      "id": "urn:uuid:0370c0fb-bb78-4a9b-87f5-bed307a509dd",
      "object": {
        "id": "https://research-organisation.org/repository/preprint/201203/421/",
        "ietf:item": {
          "id": "https://research-organisation.org/repository/preprint/201203/421/content.pdf",
          "mediaType": "application/pdf",
          "type": [
            "Article",
            "sorg:ScholarlyArticle"
          ]
        },
        "type": [
          "Page",
          "sorg:AboutPage"
        ]
      },
      "origin": {
        "id": "https://research-organisation.org/repository",
        "inbox": "https://research-organisation.org/inbox/",
        "type": "Service"
      },
      "target": {
        "id": "https://overlay-journal.com/system",
        "inbox": "https://overlay-journal.com/inbox/",
        "type": "Service"
      },
      "type": [
        "Offer",
        "coar-notify:EndorsementAction"
      ]
    }

We can parse this notification as follows

.. code-block:: python

    import json
    from coarnotify.factory import COARNotifyFactory

    raw = "{@context  ...}" # the raw payload shown above
    data = json.loads(raw)
    notification = COARNotifyFactory.get_by_object(data)

    # confirm that the payload has been parsed into the correct object
    from coarnotify.models import RequestEndorsement
    assert isinstance(notification, RequestEndorsement)

We can also access the correct model objects via the type of the notification and construct it ourselves:

.. code-block:: python

    import json
    from coarnotify.factory import COARNotifyFactory

    raw = "{@context  ...}" # the raw payload shown above
    data = json.loads(raw)
    klazz = COARNotifyFactory.get_by_type(data['type'])
    notification = klazz(data)

    # confirm that the detected class is the correct one
    from coarnotify.models import RequestEndorsement
    assert klazz == RequestEndorsement