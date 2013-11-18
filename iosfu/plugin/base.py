from iosfu.utils import slugify


class BasePlugin(object):
    """
    Base plugin object
    """
    category = 'Base'  # Category of the plugin
    name = 'Base Plugin'  # Name of the plugin
    description = ''  # Description

    _backup = None  # BackupManager instance

    @property
    def __slug__(self):
        """
        Returns slugified name for identification
        """
        return u"{0}.{1}".format(
            slugify(self.category),
            slugify(self.name)
        )
