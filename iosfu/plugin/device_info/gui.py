from iosfu.gui.core import GUIController, GUIPanel


controller = GUIController()


@controller.register
class DeviceInfoPanel(GUIPanel):
    id = 'device-info'

    name = 'Device info'
