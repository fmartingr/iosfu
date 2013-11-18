from iosfu.plugin.library import Library


lib = Library()
lib.discover()
print(lib.plugins)
