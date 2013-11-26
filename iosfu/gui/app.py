from flask import Flask, session, render_template, redirect, url_for

from iosfu.plugin.library import Library
from iosfu.gui.core import GUIController
from iosfu.backup import BackupManager


server = Flask(__name__)

# Secret key for sessions
server.secret_key = '123456'  # Local app, simple session ID.

# Plugin library loading
library = Library()
library.discover()

# Gui controller loading
controller = GUIController()
controller.load_from_library(library)

# Backups
backup_manager = BackupManager()
backup_manager.lookup()


@server.context_processor
def backup_list():
    return dict(backups=backup_manager.backups)


#
# ROUTES
#
@server.route("/")
def main():
    """
    Main page
    """
    return render_template('main.jinja')


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


@server.route("/backup/<backup_id>/")
def select_backup(backup_id):
    """
    Backup selection route
    """
    try:
        backup = backup_manager.backups[backup_id]
        if backup.valid:
            session['backup'] = backup_id
        else:
            del session['backup']
    except:
        # Backup is not loaded / do not exist
        # session['backup'] does not exist
        if 'backup' in session:
            del session['backup']

    return redirect(url_for('main'))
