from iosfu.gui.core import GUIController
from iosfu.gui.components.base import Panel, Section
from iosfu.plugin.device_info.plugin import DeviceInfoPlugin


controller = GUIController()


class Main(Section):
    name = 'Main'
    plugin = DeviceInfoPlugin
    template = 'main.jinja'

    def get_device_image(self, product):
        device_map = (
            ('iPhone1,1', 'iphone.png', ),
            ('iPhone1,2', 'iphone3g.png', ),
            ('iPhone2,1', 'iphone3gs.png', ),
            ('iPhone3,', 'iphone4.png', ),
            ('iPhone4,1', 'iphone4s.png', ),
            ('iPhone5,1', 'iphone5.png', ),
            ('iPhone5,2', 'iphone5.png', ),
            ('iPhone1,3', 'iphone5c.png', ),
            ('iPhone1,4', 'iphone5c.png', ),
            ('iPhone6,', 'iphone5s.png', ),

        )

        return device_map[
            [i for i, v in enumerate(device_map) if v[0] in product][0]
        ][1]

    def extra_context(self, ctx):
        extra = {
            'device_image': self.get_device_image(
                ctx['device']['product_type']),
        }

        return extra


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
