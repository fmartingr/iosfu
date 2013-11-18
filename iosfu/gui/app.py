from flask import Flask
from iosfu.conf import ROOT_PATH

server = Flask(__name__)


@server.route("/")
def main():
    result = """
        Executed from: {0}<br />
        Path for GUI module: {1}
    """.format(ROOT_PATH)
    return result
