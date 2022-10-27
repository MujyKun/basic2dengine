class Action:
    """
    Represents a bounded action when encountering the boundaries of a scene or sprite.

    :param action_type: str
        The action type.
    """
    def __init__(self, action_type: str):
        self.type: str = action_type

    def __eq__(self, other):
        return self.type.lower() == other.type.lower()

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def die(cls):
        """Die when encountering a scene or sprite."""
        return Action("die")

    @classmethod
    def wrap(cls):
        """Wrap around the scene."""
        return Action("wrap")

    @classmethod
    def stop(cls):
        """Stop when hitting the boundary of a scene or sprite."""
        return Action("stop")

    @classmethod
    def bounce(cls):
        """Bounce off when hitting the boundary of a scene or sprite."""
        return Action("bounce")

    @classmethod
    def pass_through(cls):
        """Pass through a sprite."""
        return Action("pass")

