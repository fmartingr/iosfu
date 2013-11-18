from os import listdir
from os.path import join as join_paths, basename, isdir, isfile
from plistlib import readPlist

from .conf import BACKUPS_PATH


class BackupManager(object):
    # Path to backups
    path = None

    # Backups loaded
    backups = {}

    def __init__(self):
        self.path = BACKUPS_PATH

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
        self.check()

        self.files = []
        print(self._plist)

    def get_info(self):
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

    def check(self):
        for required_file in self._required_files:
            # Check if required files are there
            if required_file not in self.files:
                self.valid = False

    def exists(self, filename):
        return filename in self.files

    #
    #   File handlers
    #
    def _read_plist(self, filename):
        try:
            self._plist[filename] = readPlist(join_paths(self.path, filename))
        except:
            # TODO
            pass

### TEST
# manager = BackupManager()
# manager.lookup()

# for k, backup in manager.backups.items():
#     print(backup.id, backup.valid, backup.exists('Info.plist'))
