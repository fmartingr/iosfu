from os import listdir
from os.path import join as join_paths, basename, isdir, isfile
from plistlib import readPlist

from biplist import readPlist as readBinaryPlist

from .conf import BACKUPS_PATH


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
    id = None
    name = None
    path = None
    files = []

    valid = True

    _required_files = [
        'Info.plist', 'Manifest.mbdb', 'Manifest.plist', 'Status.plist'
    ]

    _file_handlers = {
        '.plist': '_read_plist'
    }

    _plist = {}

    def __init__(self, path):
        self.path = path
        self.get_info()
        self.init_check()

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
