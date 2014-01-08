from iosfu.utils import slugify


class BasePlugin(object):
    """
    Base plugin object
    """
    domain = None  # App Domain com.*.*
    category = 'Base'  # Category of the plugin
    name = 'Base Plugin'  # Name of the plugin
    description = ''  # Description

    _backup = None  # Backup instance

    # Backup requeriments for the plugin to work
    requires = {
        # List of files needed
        'files': [],
    }

    @property
    def __slug__(self):
        """
        Returns slugified name for identification
        """
        return u"{0}.{1}".format(
            slugify(self.category),
            slugify(self.name)
        )

    def __init__(self, backup=None):
        self._backup = backup

    def __unicode__(self):
        return u"{0}".format(self.domain)

    def do(self, *args, **kwargs):
        """
        Main function called by plugin library.
        """
        if self._backup:

            # Load from cache if enabled
            if self._backup.data('cache.enabled'):
                cached = self._backup.cache(self.__slug__)
                if cached is not None:
                    return cached

            # Not found in cache, execute plugin!
            result = self.__do__(*args, **kwargs)

            # Save to cache if enabled
            if self._backup.data('cache.enabled'):
                self._backup.cache(self.__slug__, result)
                self._backup.write_data_file()

            # Return result
            return result
        else:
            raise Exception(
                'Plugin {0} need a backup instance to work with'.format(
                    self.__slug__)
            )

    def __do__(self, *args, **kwargs):
        """
        Main plugin function.
        """
        pass
