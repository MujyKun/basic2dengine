class Action:
    """
    Represents a bounded action when encountering the boundaries of a scene.

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
        """Die"""
        return Action("die")

    @classmethod
    def wrap(cls):
        return Action("wrap")

    @classmethod
    def stop(cls):
        return Action("stop")

