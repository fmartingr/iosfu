from flask import Flask, session, render_template, redirect, url_for, flash, \
    render_template_string

from iosfu.plugin.library import Library
from iosfu.gui.core import GUIController
from iosfu.backup import BackupManager


server = Flask('iosfu.gui.app')

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


#
# CONTEXT
#
@server.context_processor
def backup_list():
    return dict(backups=backup_manager.backups)


@server.context_processor
def category_list():
    return dict(categories=controller._categories)


@server.context_processor
def current_section():
    # Empty so jinja can stop yelling at me
    return dict(current=dict(category=None, panel=None, section=None))


#
# ROUTES
#
@server.route("/")
def main():
    """
    Main page
    """
    return render_template('_layout.jinja')


@server.route("/<category>/")
def category(category):
    """
    Category
    """
    panels = controller._categories[category]
    go = redirect(
        url_for('panel', category=category, panel_id=panels[0].id))
    return go


@server.route("/<category>/<panel_id>/")
def panel(category, panel_id):
    """
    Panel
    """
    panel = controller.load_panel(panel_id)
    try:
        default_section = panel.sections[0]()
        return redirect(
            url_for(
                'section',
                category=category, panel_id=panel_id,
                section_id=default_section.id))
    except IndexError:
        ctx = {
            'current': {
                'category': category,
                'panel': panel
                },
            'error_message': 'Panel does not have sections!'
        }
        return render_template(
            'error.jinja', **ctx)


@server.route("/<category>/<panel_id>/<section_id>/")
def section(category, panel_id, section_id):
    """
    Section
    """
    panel = controller.load_panel(panel_id)
    section = panel.get_section(
        section_id, backup_manager.get(session['backup']))
    ctx = {'current': {
        'category': category, 'panel': panel, 'section': section}}
    template, context = section.render(ctx=ctx)
    return render_template_string(template, **context)


@server.route("/backup/<backup_id>/")
def select_backup(backup_id):
    """
    Backup selection route
    """
    try:
        backup = backup_manager.backups[backup_id]
        if backup.valid:
            session['backup'] = backup_id
            flash('Changed to backup {}'.format(backup_id), 'success')
        else:
            flash('The backup you selected is invalid.', 'danger')
            # Delete current selected backup -if any
            if 'backup' in session:
                del session['backup']
    except:
        # Backup is not loaded / do not exist
        # Delete current selected backup -if any
        if 'backup' in session:
            del session['backup']
        flash('The backup you selected was not found.', 'danger')

    return redirect(url_for('main'))
