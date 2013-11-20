from iosfu.plugin.library import Library
from iosfu.backup import BackupManager

manager = BackupManager()
manager.lookup()

lib = Library()
lib.discover()
print(lib.plugins)
