from os import listdir
from os.path import join as join_paths, basename, isdir, isfile
from plistlib import readPlist

from biplist import readPlist as readBinaryPlist

from .conf import BACKUPS_PATH
from iosfu import utils


class BackupManager(object):
    # Path to backups
    path = None

    # Backups loaded
    backups = {}

    def __init__(self, path=BACKUPS_PATH):
        self.path = path

    def lookup(self):
        """
        Look for backup folders on PATH
        """
        folders = listdir(self.path)
        for dirname in folders:
            path = join_paths(self.path, dirname)
            if isdir(path):
                backup = Backup(path)
                self.backups[backup.id] = backup

    def get(self, backup_id):
        if backup_id in self.backups and self.backups[backup_id].valid:
            return self.backups[backup_id]
        else:
            raise Exception('Backup not registered')


class Backup(object):
    """
    Backup object
    """
    # Backup id
    id = None

    # Backup name (settings)
    name = None

    # Backup path
    path = None

    # Files
    files = []

    # bool if its valid -> self.init_check()
    valid = True

    # Required files to mark as valid
    _required_files = [
        'Info.plist', 'Manifest.mbdb', 'Manifest.plist', 'Status.plist'
    ]

    # File handlers to call methods
    _file_handlers = {
        '.plist': '_read_plist'
    }

    _plist = {}

    # Data
    _data_file = None
    _data = {}

    def __init__(self, path):
        self.path = path
        self.get_info()
        self._data_file = self.get_data_file()
        self.init_check()
        self.read_data_file()

    def get_data_file(self):
        return "{}.iosfu".format(self.path)

    def read_data_file(self):
        try:
            handler = open(self._data_file)
        except FileNotFoundError:
            handler = open(self._data_file, 'w+')
            # Initial data
            data = {
                "id": self.id,
                "cache": {}
            }
            handler.write(utils.serialize(data))
            handler.seek(0)
        finally:
            with handler as f:
                data_file = f.read()

            self._data = utils.deserialize(data_file)
            handler.close()

    def get_info(self):
        """
        Get all the basic info for the backup
        """
        self.id = basename(self.path)
        self.name = self.id

        # Check all files
        for filename in listdir(self.path):
            if isfile(join_paths(self.path, filename)):
                self.files.append(filename)

                # Check handlers
                for match in self._file_handlers.keys():
                    if match in filename:
                        handler = getattr(self, self._file_handlers[match])
                        handler(filename)

    def init_check(self):
        """
        Check if the needed stuff are there to consider this a backup
        """
        for required_file in self._required_files:
            # Check if required files are there
            # FIXME Sometimes it doesn't work :?
            if required_file not in self.files:
                self.valid = False

    def exists(self, filename):
        """
        Check if the given file exists
        """
        return filename in self.files

    def get_file(self, filename, handler=False):
        """
        Returns given file path
        - handler (bool) - Returns handler instead of path
        """
        result = None
        if self.exists(filename):
            file_path = join_paths(self.path, filename)
            if handler:
                result = open(file_path, 'rb')
            else:
                result = file_path
        return result

    #
    #   File handlers
    #
    def _read_plist(self, filename):
        """
        Handler for .plist files
        Reads them and stores on self._plist for plugin access
        """
        file_path = self.get_file(filename)
        try:
            self._plist[filename] = readPlist(file_path)
        except:
            # Is binaryPlist?
            try:
                self._plist[filename] = readBinaryPlist(file_path)
            except:
                # What is it?
                pass

    #
    #   Backup data file
    #
    def data(self, key, value=None):
        result = value
        if value:
            self._data[key] = value
        elif key in self._data:
            result = self._data[key]

        return result

    def cache(self, key, value=None):
        result = value
        if value:
            self._data['cache'][key] = value
        elif key in self._data['cache']:
            result = self._data['cache'][key]

        return result

    def clear_cache(self):
        self._data['cache'] = {}
        self.write_data_file()

    def write_data_file(self):
        handler = open(self._data_file, 'w+')
        handler.write(utils.serialize(self._data))
        handler.close()
