from os import listdir, walk
from os.path import join as join_paths, isdir, isfile, realpath, dirname
from importlib import import_module


PATH = dirname(realpath(__file__))


class Library(object):
    """
    Plugin library
    """
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

    def load(self, path):
        plugin_path = path.replace(PATH, '').replace('/', '.')
        plugin_package = 'iosfu.plugin{0}.plugin'.format(plugin_path)
        import_module(plugin_package)

    def discover(self):
        for path, dirs, files in walk(PATH):
            if files == ['__init__.py', 'plugin.py']:
                # print(path)
                # print(dirs)
                # print(files)
                # print('plugin!')
                self.load(path)
        # for dirname in listdir(PATH):
        #     plugin_path = join_paths(PATH, dirname)
        #     plugin_module = join_paths(PATH, dirname, 'plugin.py')
        #     plugin_init = join_paths(PATH, dirname, '__init__.py')
        #     if isdir(plugin_path) and isfile(plugin_module) \
        #         and isfile(plugin_init):
        #         self.load(plugin_path, dirname)
                
