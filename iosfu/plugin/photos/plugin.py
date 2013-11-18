from iosfu.plugin import BasePlugin, Library


plugin_library = Library()


@plugin_library.register
class PhotosPlugin(BasePlugin):
    category = 'Base'
    name = 'Photos'
    description = 'Photos.'
