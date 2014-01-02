from iosfu.gui.core import GUIController
from iosfu.gui.components.base import Panel, Section
from iosfu.plugin.device_info.plugin import DeviceInfoPlugin


controller = GUIController()


class Main(Section):
    name = 'Main'
    plugin = DeviceInfoPlugin
    template = 'main.jinja'


class VersionInfo(Section):
    name = 'Version Info'
    plugin = DeviceInfoPlugin
    template = 'device_info.jinja'


@controller.register_panel
class DeviceInfoPanel(Panel):
    id = 'device-info'

    name = 'Device info'

    category = 'Base'

    sections = [
        Main,  # First one is default
        VersionInfo
    ]
