from iosfu.plugin.base import BasePlugin
from iosfu.plugin.library import Library


plugin_library = Library()


@plugin_library.register
class DeviceInfoPlugin(BasePlugin):
    category = 'Base'
    name = 'Device info'
    description = 'Basic information about the device/backup'

    requires = {
        'files': ['Info.plist'],
    }

    _plist = None

    def parse_device_info(self):
        keys = [
            ('build_version', 'Build Version'),
            ('device_name', 'Device Name'),
            ('display_name', 'Display Name'),
            ('guid', 'GUID'),
            ('iccid', 'ICCID'),
            ('imei', 'IMEI'),
            ('installed_apps', 'Installed Applications'),
            ('phone_number', 'Phone Number'),
            ('product_type', 'Product Type'),
            ('product_version', 'Product Version'),
            ('serial_number', 'Serial Number'),
            ('itunes_version', 'iTunes Version')
        ]

        device_info = dict()
        for key in keys:
            device_info[key[0]] = self.get_value_from_plist(key[1])

        return device_info

    def parse_backup_info(self):
        keys = [
            ('backup_date', 'Last Backup Date'),
        ]

        backup_info = dict()
        for key in keys:
            backup_info[key[0]] = self.get_value_from_plist(key[1])

        return backup_info

    def get_value_from_plist(self, key):
        value = '--'
        try:
            value = self._plist[key]
        except:
            pass
        return value

    def __do__(self):
        self._plist = self._backup._plist['Info.plist']
        info_dict = dict()
        info_dict['device'] = self.parse_device_info()
        info_dict['backup'] = self.parse_backup_info()

        return info_dict
