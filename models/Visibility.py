class Visibility:
    """Handles the visibility state of an object.

    :param visibility: bool
        Whether the object is visible.
    """

    def __init__(self, visibility: bool = True):
        self.__visibility = visibility

    @property
    def visible(self):
        return self.__visibility

    @visible.setter
    def visible(self, flag: bool):
        """
        Set whether the sprite is visible.

        :param flag: bool
            Whether the sprite should be visible.
        """
        self.__visibility = flag

    def hide(self):
        """Hide the sprite."""
        self.visible = False

    def show(self):
        """Show the sprite."""
        self.visible = True
