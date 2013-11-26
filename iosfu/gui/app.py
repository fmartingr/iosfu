from flask import Flask

from iosfu.conf import ROOT_PATH
from iosfu.plugin.library import Library
from iosfu.gui.core import GUIController


server = Flask(__name__)

library = Library()
library.discover()

controller = GUIController()
controller.load_from_library(library)


@server.route("/")
def main():
    result = """
        Executed from: {0}<br />
    """.format(ROOT_PATH)
    return result


@server.route("/<panel>/")
def panel(panel_id=None):
    panel = controller.load_panel(panel_id)
    return panel


@server.route("/<panel>/<section>/")
def section(panel_id=None, section_id=None):
    return 'lol'
