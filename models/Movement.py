from dataclasses import dataclass
import math
from typing import Optional, Union


@dataclass
class MovementManipulator:
    """
    Holds a change/modification or position to an axis or direction.

    :param x: Union[int, float]
        Change/Modifier or position in X direction.
    :param y: Union[int, float]
        Change/Modifier or position in X direction.
    """
    x: Union[int, float]
    y: Union[int, float]


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

    @property
    def angle_in_degrees(self):
        """Get the angle in degrees."""
        return self.radians_to_degrees(self._angle)

    @angle.setter
    def angle(self, radians: float):
        """Set the angle in radians.

        :param radians: float
            The angle to set.
        """
        self._angle = radians

    @property
    def cos(self):
        """Get the cos of the angle."""
        return math.cos(self.angle)

    @property
    def sin(self):
        """Get the sin of the angle."""
        return math.sin(self.angle)

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
    :param static: bool
        Whether the object doesn't move / is not dynamic.
    """
    def __init__(self, speed=0,
                 position: MovementManipulator = None, velocity: MovementManipulator = None,
                 acceleration: MovementManipulator = None, img_angle: Angle = None, move_angle: Angle = None,
                 static=False):
        self._speed = abs(speed)
        self.position = position or MovementManipulator(0, 0)
        self.velocity = velocity or MovementManipulator(0, 0)
        self.acceleration = acceleration or MovementManipulator(0, 0)
        self.img_angle = img_angle or Angle()
        self.move_angle = move_angle or Angle()
        self.static = static

    def set_position(self, center_x, center_y):
        """Set the object's position."""
        self.position.x, self.position.y = center_x, center_y

    def update_position(self):
        """Update the position of the object."""
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y

    def add_vector(self, angle: Angle, thrust=1):
        """Modify the motion."""
        self.velocity.x += thrust * angle.cos
        self.velocity.y += thrust * angle.sin

    def update(self):
        """Update the movement."""
        if not self.static:
            self.update_speed()
            self.update_move_angle()
            self.update_velocity()
            self.update_position()

    @property
    def is_moving(self):
        return not (self.velocity.x == 0 and self.velocity.y == 0)

    def update_velocity(self):
        """Update the velocity of the object."""
        self.velocity.x = self.speed * self.move_angle.cos
        self.velocity.y = self.speed * self.move_angle.sin

    def update_speed(self):
        """Update the speed."""
        self._speed = math.sqrt(self.velocity.x**2 + self.velocity.y**2)

    def update_move_angle(self):
        """Update the move angle."""
        self.move_angle.angle = math.atan2(self.velocity.y, self.velocity.x)

    def update_img_angle(self, angle: Angle):
        """Update the image angle."""
        self.img_angle = angle

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
        self.update_velocity()
