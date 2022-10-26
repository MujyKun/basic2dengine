from dataclasses import dataclass
import math
from typing import Optional


@dataclass
class MovementManipulator:
    """
    Holds a change/modification or position to an axis or direction.

    :param x: int
        Change/Modifier or position in X direction.
    :param y: int
        Change/Modifier or position in X direction.
    """
    x: int
    y: int


class Angle:
    """
    Holds an angle in radians.

    :param radians: Optional[float]
        Angle in radians
    :param degrees: Optional[float]
        Angle in degrees
    """
    def __init__(self, radians: Optional[float] = None, degrees: Optional[float] = None):
        if radians:
            self._angle = radians
        elif degrees:
            self._angle = self.degrees_to_radians(degrees)
        else:
            self._angle = 0

    @property
    def angle(self):
        """Get the angle in radians."""
        return self._angle

    @angle.setter
    def angle(self, radians: float):
        """Set the angle in radians.

        :param radians: float
            The angle to set.
        """
        self._angle = radians

    @staticmethod
    def radians_to_degrees(radians: float):
        """Convert radians to degrees.

        :param radians: float
            The radians to convert.
        """
        return math.degrees(radians)

    @staticmethod
    def degrees_to_radians(degrees: float):
        """Convert degrees to radians.

        :param degrees: float
            The degrees to convert.
        """
        return math.radians(degrees)


class Movement:
    """
    Handles and contains attributes for movement.
    :param position: :ref:`MovementManipulator`
        The position of the object.
    :param speed: int
        The speed of the object.
    :param velocity: :ref:`MovementManipulator`
        The velocity of the object.
    :param acceleration: :ref:`MovementManipulator`
        The acceleration of the object.
    :param img_angle: :ref:`Angle`
        The image angle of the object.
    :param move_angle: ref:`Angle`:
        The move angle of the object.
    """
    def __init__(self, speed=0,
                 position: MovementManipulator = None, velocity: MovementManipulator = None,
                 acceleration: MovementManipulator = None, img_angle: Angle = None, move_angle: Angle = None):
        self._speed = abs(speed)
        self.position = position or MovementManipulator(0, 0)
        self.velocity = velocity or MovementManipulator(0, 0)
        self.acceleration = acceleration or MovementManipulator(0, 0)
        self.img_angle = img_angle or Angle()
        self.move_angle = move_angle or Angle()

    @property
    def speed(self):
        """Get the speed of the object."""
        if self._speed <= 0:
            self._speed = abs(self._speed)
        return self._speed

    @speed.setter
    def speed(self, new_speed: int):
        """
        Set the new speed of the object.

        :param new_speed: int
            The new speed of the object.
        """
        self._speed = abs(new_speed)
