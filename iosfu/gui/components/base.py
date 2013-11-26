from iosfu.utils import slugify


class GUIComponent(object):
    """
    Base GUI Component object
    """

    # Component type, do NOT modify
    _type = None


class GUIPanel(GUIComponent):
    """
    Pene
    """
    _type = 'panel'

    # Identifier of the panel. Created automatically as a slug of the name if
    # not set. GUIPanel identifiers MUST NOT BE REPEATED.
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

    def get_section(self, section_id):
        if section_id in self._section_map:
            return self.sections[self._section_map[section_id]]()

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


class GUISection(GUIComponent):
    """
    Pene
    """
    _type = 'section'
    id = None

    # A GUIPanel ID
    panel = None

    # Name of the section
    name = None

    def __init__(self):
        if not self.id and self.name:
            self.id = "{}".format(slugify(self.name))

    @property
    def __slug__(self):
        return self.id
