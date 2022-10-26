import pygame

from . import Image, Movement, Size, MovementManipulator, Angle, Visibility, Action
from math import sqrt, atan2


class Sprite(pygame.sprite.Sprite):
    """
    Handles a general entity as a sprite.


    :param size: Optional[:ref:`Size`]
        The size instance of the sprite.
    :param image: Optional[:ref:`Image`]
        The image instance of the sprite.
    :param movement: Optional[:ref:`Movement`]
        The movement instance of the sprite.
    :param visibility: bool
        Whether the sprite is visible.
    :param scene_size: :ref:`Size`
        The size instance for the scene. Useful for boundary checking.
    """

    def __init__(self, size: Size = None,
                 image: Image = None,
                 movement: Movement = None,
                 visibility: bool = True, scene_size: Size = None, bounded_action: Action = None):
        super(Sprite, self).__init__()
        self.size: Size = size or Size(100, 100)
        self.image_obj: Image = image or Image(self.size)
        self.movement: Movement = movement or Movement()
        self.__visibility = Visibility(visibility)
        self._rect = None
        self._rect_surface = None
        self._scene_size = scene_size or Size(1280, 720)
        self._bounded_action = bounded_action or Action.wrap()

    @property
    def rect(self):
        """Get the object's rect.

        ..Note:: This bypasses pygame needing to be initialized first.
        """
        if not self._rect:
            self._rect = self.image_obj.surface.get_rect()
            self.movement.set_position(self._rect.x, self._rect.y)
            self._rect_surface = self.image_obj.surface

        if self._rect_surface != self.image_obj.surface:
            self._rect = None
            return self.rect  # recursive reset.
        return self._rect

    @property
    def visible(self):
        return self.__visibility.visible

    def hide(self):
        self.__visibility.hide()
        # only change our current rect values and set them off-screen.
        # we can later fetch our last known position by the movement instance.
        self.rect.x = 0 - self.size.width
        self.rect.y = 0 - self.size.height

    def show(self):
        self.__visibility.show()
        # our movement position contains the true values of our position.
        self.rect.x = self.movement.position.x
        self.rect.y = self.movement.position.y

    @property
    def center(self) -> MovementManipulator:
        """Get the center of the sprite."""
        x = self.movement.position.x + (self.size.width / 2)
        y = self.movement.position.y + (self.size.height / 2)
        return MovementManipulator(x, y)

    @property
    def image(self) -> pygame.Surface:
        """Get the surface of the image."""
        return self.image_obj.surface

    @image.setter
    def image(self, new_image: Image):
        """
        Set the new image of the object.

        :param new_image: :ref:`Image`
            The new image of the object.
        """
        self.image_obj = new_image

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

    def collides_with(self, sprite):
        """Check if a sprite collides with another sprite.

        :param sprite: :ref:`Sprite`
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

        :param sprite: :ref:`Sprite`
            The sprite to check angles with.
        """
        return Angle(degrees=atan2(self.center.y - sprite.center.y, self.center.x - sprite.center.x) + 90)

    def distance_to(self, sprite):
        """Check the distance to another sprite.

        :param sprite: :ref:`Sprite`
            The sprite to check distances with.
        """
        x_diff = self.movement.position.x - sprite.movement.position.x
        y_diff = self.movement.position.y - sprite.movement.position.y
        return sqrt(x_diff ** 2 + y_diff ** 2)

    def _check_bounds(self):
        """Check the bounds of the sprite."""
        new_x = self.movement.position.x
        new_y = self.movement.position.y
        top_check = self.movement.position.y < 0
        bottom_check = self.movement.position.y > self._scene_size.height
        left_check = self.movement.position.x < 0
        right_check = self.movement.position.x > self._scene_size.width

        wrap = self._bounded_action.wrap() == self._bounded_action

        if top_check:
            new_y = self._scene_size.height if wrap else 0
        if bottom_check:
            new_y = 0 if wrap else self._scene_size.height
        if left_check:
            new_x = self._scene_size.width if wrap else 0
        if right_check:
            new_x = 0 if wrap else self._scene_size.width

        if self._bounded_action.die() == self._bounded_action and \
                any([top_check, bottom_check, left_check, right_check]):
            self.hide()

        self.movement.set_position(new_x, new_y)

    def _update_position_and_angle(self):
        """Update the position of the sprite."""
        if not self.visible:
            return

        if not self.image_obj.no_rotation_surface:
            _ = self.image_obj.surface

        self._rect = self.image_obj.rotate(Angle(degrees=180))
        self._rect_surface = self.image_obj.surface
        # self.movement.add_vector(Angle(degrees=20), 5)
        self.movement.update()
        self._rect.centerx = self.movement.position.x
        self._rect.centery = self.movement.position.y

    def update(self):
        """Update the sprite."""
        if not self.visible:
            return

        self._check_bounds()  # check bounds
        self._update_position_and_angle()  # update pos

        self._draw()

    def _draw(self):
        """Draw the sprite."""

