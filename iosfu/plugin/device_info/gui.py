from iosfu.gui.core import GUIController
from iosfu.gui.components.base import GUIPanel, GUISection


controller = GUIController()


class Main(GUISection):
    name = 'Main'


class VersionInfo(GUISection):
    name = 'Version Info'


@controller.register_panel
class DeviceInfoPanel(GUIPanel):
    id = 'device-info'

    name = 'Device info'

    category = 'Base'

    sections = [
        Main,
        VersionInfo
    ]

    def render(self, context):
        return 'main.jinja', context
