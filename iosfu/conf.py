from os import getcwd
from os.path import join as join_paths


# Main
ROOT_PATH = getcwd()

# Backups folder name
BACKUPS_PATH = join_paths(ROOT_PATH, '_backups')

# Backup default settings
BACKUP_DEFAULT_SETTINGS = {
    "cache.enabled": False,
    "cache": {}
}
