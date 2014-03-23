from os.path import join as join_path, dirname
from inspect import getfile

from iosfu.utils import slugify


class Component(object):
    """
    Base GUI Component object
    """

    # Component type, do NOT modify
    _type = None

    def __unicode__(self):
        return self.name


# class Category(Component):
#     _type = 'category'

#     name = None

#     def __init__(self, name):
#         self.name = name


class Panel(Component):
    """
    Main panel component.
    Adds a section on the top navigation bar, into the selected category.
    If the category don't have any other panels, this will be shown as main
    button instead of the section.
    """
    _type = 'panel'

    # Identifier of the panel. Created automatically as a slug of the name if
    # not set. GUI Panel identifiers MUST NOT BE REPEATED.
    id = None

    # Name of the panel (will be slugified to create an ID)
    name = None

    # List of sections
    sections = []

    # Section mapping by id
    _section_map = {}

    def __init__(self):
        if not self.id and self.name:
            self.id = slugify(self.name)

        self._map_sections()

    def get_section(self, section_id, backup):
        if section_id in self._section_map:
            return self.sections[self._section_map[section_id]](
                backup=backup)

    def render(self, *args, **kwargs):
        """
        Main render method
        """
        return 'Base GUIPanel'

    #
    # Privates
    #
    def _map_sections(self):
        """
        Map section list position to its id in a dict()
        """
        i = 0
        for section in self.sections:
            ins = section()
            self._section_map[ins.__slug__] = i
            i += 1

    @property
    def __slug__(self):
        return self.id


class Section(Component):
    """
    Section main component.

    Gets a backup instance and a context, and returns the new context with
    the plugin analysis finished and the template to render the information.
    """
    _type = 'section'

    # In case you need a custom ID for this panel.
    id = None

    # Name of the section
    name = None

    # Backup instance to work with
    backup = None

    # Plugin to use automagically
    plugin = None

    # Template context
    context = dict()

    def __init__(self, backup=None):
        if backup:
            self.backup = backup

        if not self.id and self.name:
            self.id = "{}".format(slugify(self.name))

    def get_template(self, template_name):
        tmpl = join_path(
            dirname(getfile(self.__class__)), 'templates', template_name)
        try:
            with open(tmpl) as handler:
                template_content = handler.read()

        except IOError:
            try:
                # raise 'Template {} do not exist.'.format(template_name)
                tmpl = join_path(dirname(getfile(
                    self.__class__.__bases__[0])), 'templates', template_name)

                with open(tmpl) as handler:
                    template_content = handler.read()
            except IOError:
                raise 'Could not read template {}'.format(template_name)

        return template_content

    def extra_context(self, ctx):
        return {}

    def get_context(self):
        if self.backup and self.plugin:
            plugin = self.plugin(backup=self.backup)
            self.context = plugin.do()

        # Extra context
        for key, value in self.extra_context(self.context).items():
            if key not in self.context:
                self.context[key] = value

    def render(self, *args, **kwargs):
        """
        Base rendering method
        """
        ctx = kwargs.pop('ctx', dict())
        self.get_context()
        ctx.update(dict(plugin_data=self.context))
        return self.get_template(self.template), ctx

    @property
    def __slug__(self):
        return self.id
