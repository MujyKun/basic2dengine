from dataclasses import dataclass


@dataclass
class Size:
    """
    Represents the size of an object.

    :param width: int
        Width of the object.
    :param height: int
        Height of the object.
    """
    width: int
    height: int

    def get_tuple(self) -> tuple:
        return self.width, self.height
