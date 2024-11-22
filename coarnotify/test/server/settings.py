STORE_DIR = "/your/store/dir"
"""The directory on the local machine to use to store incoming JSON files"""

HOST = "localhost"
"""Host where the app will run"""

PORT = 5005
"""Port to start the app on"""

RESPONSE_STATUS = 201
"""HTTP Response to provide to any incoming reqeusts.  201 and 202 are the specification compliant values"""

VALIDATE_INCOMING = True
"""Should the server attempt to validate the incoming notifications"""

DEBUG = True
"""Put flask into debug mode for developer convenience"""

DEBUG_PYCHARM = False
"""Put the app into PyCharm debug mode.  This turns off ``DEBUG`` and starts the PyCharm debugger.  You can set this here, or you can start the test server with the ``-d`` option"""

DEBUG_PYCHARM_SERVER = "localhost"
"""The host to connect to for PyCharm debugging"""

DEBUG_PYCHARM_PORT = 6000
"""The port to connect to for PyCharm debugging"""