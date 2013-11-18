from iosfu.plugin.base import BasePlugin
from iosfu.plugin.library import Library


plugin_library = Library()


@plugin_library.register
class ContactsPlugin(BasePlugin):
    category = 'Base'
    name = 'Contacts'
    description = 'Contacts.'
