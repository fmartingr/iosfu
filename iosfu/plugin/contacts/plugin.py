from iosfu.plugin import BasePlugin, Library


plugin_library = Library()


@plugin_library.register
class ContactsPlugin(BasePlugin):
    category = 'Base'
    name = 'Contacts'
    description = 'Contacts.'
