from os import walk
from os.path import realpath, dirname
from importlib import import_module


PATH = dirname(realpath(__file__))


class Library(object):
    """
    Plugin library
    """
    _instance = None
    _plugins = {}  # Plugin dictonary

    _mandatory_plugin_files = ['__init__.py', 'plugin.py']

    def register(self, plugin):
        """
        Decorator to register plugins
        """
        ins = plugin()
        plugin_slug = ins.__slug__
        if ins not in self._plugins:
            self._plugins[plugin_slug] = plugin
        else:
            raise RuntimeError(
                'Plugin {0} already registered.'.format(plugin_slug))

    def load(self, path):
        plugin_path = path.replace(PATH, '').replace('/', '.')
        plugin_package = 'iosfu.plugin{0}.plugin'.format(plugin_path)
        import_module(plugin_package)

    def discover(self):
        for path, dirs, files in walk(PATH):
            if self._is_plugin(files):
                self.load(path)

    @property
    def plugins(self):
        return self._plugins

    def _is_plugin(self, files):
        for f in self._mandatory_plugin_files:
            if f not in files:
                return False
        return True
