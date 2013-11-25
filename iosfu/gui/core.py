from importlib import import_module


class GUIController(object):
    """
    Object that store and control all the UI compoennts.
    """

    _panels = {}
    _sections = {}

    def register(self, component):
        """
        Decorator to register plugins
        """
        ins = component()

        print(ins)

        if ins._type == 'panel':
            self.register_panel(component)

        if ins._type == 'section':
            self.register_section(component)

    def register_panel(self, panel_component):
        self._panels['a'] = panel_component
        pass

    def register_section(self, section_component):
        print('register section')
        pass

    def load_from_library(self, library):
        for k, plugin in library.plugins.items():
            plugin_module = plugin.__module__
            gui_module = "{0}.{1}".format(
                plugin_module.rstrip('.plugin'),
                'gui'
            )
            try:
                import_module(gui_module)
            except ImportError as error:
                # Plugin with no GUI module.
                print(error)
