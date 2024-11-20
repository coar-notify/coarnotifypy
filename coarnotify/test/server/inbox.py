from flask import Flask, request, make_response
from coarnotify.test.server import settings
from coarnotify.server import COARNotifyServer, COARNotifyServiceBinding, COARNotifyReceipt, COARNotifyServerError
import uuid, json, sys, os
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    app.config.from_envvar("COARNOTIFY_SETTINGS", silent=True)
    return app

app = create_app()


class COARNotifyServiceTestImpl(COARNotifyServiceBinding):
    def notification_received(self, notification):
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
    :param host:
    :param port:
    :param fake_https:
        if fake_https is True, develop can use https:// to access the server
        that can help for debugging Plausible
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