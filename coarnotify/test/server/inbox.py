"""
Single file implementation of a test server, showing all the layers of the general
solution in one place.
"""
from flask import Flask, request, make_response
from coarnotify.test.server import settings
from coarnotify.server import COARNotifyServer, COARNotifyServiceBinding, COARNotifyReceipt, COARNotifyServerError
from coarnotify.core.notify import NotifyPattern
import uuid, json, sys, os
from datetime import datetime

def create_app():
    """
    Create the flask app, pulling config from ``settings.py`` then any supplied local config
    in environment variable ``COARNOTIFY_SETTINGS``.

    :return:
    """
    app = Flask(__name__)
    app.config.from_object(settings)
    app.config.from_envvar("COARNOTIFY_SETTINGS", silent=True)
    return app

app = create_app()
"""The global flask app for the test server"""


class COARNotifyServiceTestImpl(COARNotifyServiceBinding):
    """
    Test server implementation of the main service binding
    """
    def notification_received(self, notification: NotifyPattern) -> COARNotifyReceipt:
        """
        Process an incoming notification object in the following way:

        1. Generate a name for the notification based on the timestamp and a random UUID
        2. Write the notification JSON-LD  to a file in the store directory
        3. Return a receipt for the notification using the configured response status and a location pointing to the file

        :param notification:
        :return:
        """
        store = app.config.get("STORE_DIR")
        if not os.path.exists(store):
            print(f"Store directory {store} does not exist, you must create it manually")
            raise COARNotifyServerError(500, "Store directory does not exist")

        now = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        fn = now + "_" + uuid.uuid4().hex

        with open(f"{store}/{fn}.json", "w") as f:
            f.write(json.dumps(notification.to_jsonld()))

        rstatus = app.config.get("RESPONSE_STATUS", COARNotifyReceipt.CREATED)
        location = f"{request.url_root}inbox/{fn}"

        return COARNotifyReceipt(rstatus, location)


@app.route("/inbox", methods=["POST"])
def inbox():
    """
    Main web entry point.  POST to /inbox to trigger it

    This pulls the notification out of the request as JSON, and sends it to the server
    which will parse it and send it on to the service binding implementation

    When it gets the receipt it will return a blank HTTP response with the appropriate
    status code and Location header

    :return:
    """
    notification = request.json
    server = COARNotifyServer(COARNotifyServiceTestImpl())

    try:
        result = server.receive(notification, validate=app.config.get("VALIDATE_INCOMING", True))
    except COARNotifyServerError as e:
        return make_response(e.message, e.status)

    resp = make_response()
    resp.status_code = result.status
    if result.status == result.CREATED:
        resp.headers["Location"] = result.location
    return resp


def run_server(host=None, port=None, fake_https=False):
    """
    Start the web server using the flask built in server

    :param host:
    :param port:
    :param fake_https:
        if fake_https is True, developer can use https:// to access the server
    :return:
    """
    pycharm_debug = app.config.get('DEBUG_PYCHARM', False)
    if len(sys.argv) > 1:
        if sys.argv[1] == '-d':
            pycharm_debug = True

    if pycharm_debug:
        app.config['DEBUG'] = False
        import pydevd
        pydevd.settrace(app.config.get('DEBUG_PYCHARM_SERVER', 'localhost'),
                        port=app.config.get('DEBUG_PYCHARM_PORT', 6000),
                        stdoutToServer=True, stderrToServer=True)

    # check the store directory exists
    store = app.config.get("STORE_DIR")
    if not os.path.exists(store):
        print(f"Store directory {store} does not exist, you must create it manually")
        exit(1)
    else:
        print(f"Store directory: {store}")

    run_kwargs = {}
    if fake_https:
        run_kwargs['ssl_context'] = 'adhoc'

    host = host or app.config['HOST']
    port = port or app.config['PORT']
    app.run(host=host, debug=app.config['DEBUG'], port=port,
            **run_kwargs)


if __name__ == "__main__":
    run_server()