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
