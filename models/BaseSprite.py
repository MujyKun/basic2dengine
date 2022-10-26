from . import Image, Movement, Size, MovementManipulator, Angle
from math import sqrt, atan2


class BaseSprite:
    """
    Handles a general entity as a sprite.

    ..Note:: This is an abstract model.

    :param size: Optional[:ref:`Size`]
        The size instance of the sprite.
    :param image: Optional[:ref:`Image`]
        The image instance of the sprite.
    :param movement: Optional[:ref:`Movement`]
        The movement instance of the sprite.
    :param visibility: bool
        Whether the sprite is visible.
    """
    def __init__(self, size: Size = None, image: Image = None, movement: Movement = None, visibility: bool = True):
        self.size: Size = size or Size(100, 100)
        self._image: Image = image or Image()
        self.movement: Movement = movement or Movement()
        self.__visibility = visibility

    @property
    def center(self) -> MovementManipulator:
        """Get the center of the sprite."""
        x = self.movement.position.x + (self.size.width/2)
        y = self.movement.position.y + (self.size.height/2)
        return MovementManipulator(x, y)

    @property
    def image(self):
        """Get the image of the sprite."""
        return self._image

    @image.setter
    def image(self, new_image: Image):
        """
        Set the new image of the object.

        :param new_image: :ref:`Image`
            The new image of the object.
        """
        self._image = new_image

    @property
    def visible(self):
        return self.__visibility

    @property
    def left(self):
        return self.movement.position.x - (self.size.width / 2)

    @property
    def right(self):
        return self.movement.position.x + (self.size.width / 2)

    @property
    def top(self):
        return self.movement.position.y - (self.size.width / 2)

    @property
    def bottom(self):
        return self.movement.position.y + (self.size.width / 2)

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

    def collides_with(self, sprite):
        """Check if a sprite collides with another sprite.

        :param sprite: :ref:`BaseSprite`
            The sprite to check collisions with.
        """
        if not (self.visible and sprite.visible):
            return False

        # instead of checking to see if the sprites are inside each other (inherently more complex),
        # we check if they are outside.
        if any([self.bottom < sprite.top,
                self.top > sprite.bottom,
                self.right < sprite.left,
                self.left > sprite.right]):
            return False

        return True

    def angle_to(self, sprite) -> Angle:
        """Check the angle to another sprite.

        :param sprite: :ref:`BaseSprite`
            The sprite to check angles with.
        """
        return Angle(degrees=atan2(self.center.y - sprite.center.y, self.center.x - sprite.center.x) + 90)

    def distance_to(self, sprite):
        """Check the distance to another sprite.

        :param sprite: :ref:`BaseSprite`
            The sprite to check distances with.
        """
        x_diff = self.movement.position.x - sprite.movement.position.x
        y_diff = self.movement.position.y - sprite.movement.position.y
        return sqrt(x_diff**2 + y_diff**2)

    def check_bounds(self):
        """Check the bounds of the sprite."""

    def update(self):
        """Update the sprite."""

    def _draw(self):
        """Draw the sprite."""

