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

    def __init__(self):
        if not self.id and self.name:
            self.id = slugify(self.name)

    def __slug__(self):
        return slugify(self.name)


class GUISection(GUIComponent):
    """
    Pene
    """
    _type = 'section'

    # A GUIPanel ID
    panel = None

    # Name of the section
    name = None
