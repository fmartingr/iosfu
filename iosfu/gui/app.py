from flask import Flask, session

from iosfu.plugin.library import Library
from iosfu.gui.core import GUIController


server = Flask(__name__)

# Secret key for sessions
server.secret_key = '123456'  # Local app, simple session ID.

# Plugin library loading
library = Library()
library.discover()

# Gui controller loading
controller = GUIController()
controller.load_from_library(library)


#
# ROUTES
#
@server.route("/")
def main():
    """
    Main page
    """
    return 'Main page'


@server.route("/<panel_id>")
def panel(panel_id=None):
    """
    Panel
    """
    panel = controller.load_panel(panel_id)
    return "{}".format(panel().__slug__)


@server.route("/<panel_id>.<section_id>")
def section(panel_id=None, section_id=None):
    """
    Section
    """
    panel = controller.load_panel(panel_id)
    section = panel.get_section(section_id)
    return "{}.{}".format(panel.__slug__, section.__slug__)
