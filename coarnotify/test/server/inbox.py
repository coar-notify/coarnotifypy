from flask import Flask, request, make_response
from coarnotify.test.server import settings
from coarnotify.server import COARNotifyServer
from coarnotify.common import COARNotifyFactory
import uuid, json, sys, os
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    return app


app = create_app()


@app.route("/inbox", methods=["POST"])
def inbox():
    notification = request.json
    obj = COARNotifyFactory.get_by_object(notification)

    store = app.config.get("STORE_DIR")
    if not os.path.exists(store):
        print(f"Store directory {store} does not exist, you must create it manually")
        return make_response("Store directory does not exist", 500)

    now = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    fn = now + "_" + uuid.uuid4().hex

    with open(f"{store}/{fn}.json", "w") as f:
        f.write(json.dumps(obj.to_dict()))

    rstatus = app.config.get("RESPONSE_STATUS", 201)

    resp = make_response()
    resp.status_code = rstatus
    if rstatus == 201:
        resp.headers["Location"] = f"{request.url_root}inbox/{fn}"
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

    run_kwargs = {}
    if fake_https:
        run_kwargs['ssl_context'] = 'adhoc'

    host = host or app.config['HOST']
    port = port or app.config['PORT']
    app.run(host=host, debug=app.config['DEBUG'], port=port,
            **run_kwargs)


if __name__ == "__main__":
    run_server()