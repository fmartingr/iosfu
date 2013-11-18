from iosfu.utils import slugify


class Library(object):
    _instance = None
    plugins = {}  # Plugin dictonary

    def register(self, plugin):
        """
        Decorator to register plugins
        """
        ins = plugin()
        plugin_slug = ins.__slug__
        if ins not in self.plugins:
            self.plugins[plugin_slug] = plugin
        else:
            raise RuntimeError(
                'Plugin {0} already registered.'.format(plugin_slug))


class BasePlugin(object):
    """
    Base plugin object
    """
    category = 'Base'
    name = 'Base Plugin'
    description = ''

    @property
    def __slug__(self):
        """
        Returns slugified name for identification
        """
        return u"{0}.{1}".format(
            slugify(self.category),
            slugify(self.name)
        )
