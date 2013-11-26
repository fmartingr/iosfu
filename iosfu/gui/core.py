from importlib import import_module

from .components.base import GUIPanel


class GUIController(object):
    """
    Object that store and control all the UI compoennts.
    """

    _panels = {}
    _sections = {}

    def register_panel(self, panel_component):
        """
        Decorator to register GUIPanels
        """
        ins = panel_component()
        assert isinstance(ins, GUIPanel)
        self._panels[ins.__slug__] = panel_component

    def load_from_library(self, library):
        for k, plugin in library.plugins.items():
            plugin_module = plugin.__module__
            gui_module = "{0}.{1}".format(
                plugin_module.rsplit('.', 1)[0],
                'gui'
            )
            try:
                import_module(gui_module)
            except ImportError as error:
                # Plugin with no GUI module.
                print(error)

    def load_panel(self, panel_id):
        if panel_id in self._panels:
            return self._panels[panel_id]
