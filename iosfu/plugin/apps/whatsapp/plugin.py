from iosfu.plugin.base import BasePlugin
from iosfu.plugin.library import Library


plugin_library = Library()


@plugin_library.register
class WhatsappPlugin(BasePlugin):
    category = 'Apps'
    name = 'Whatsapp'
    description = 'Whatsapp.'
