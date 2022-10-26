from . import BaseSprite


class Sprite(BaseSprite):
    """Handles a general entity as a sprite."""
    def __init__(self, *args, **kwargs):
        super(Sprite, self).__init__(*args, **kwargs)

    def update(self):
        """Update the sprite."""
        if not self.__visibility:
            return

        self.update_position()  # update pos
        self.check_bounds()  # check bounds


        self._draw()

    def _draw(self):
        """Draw the sprite."""

    def collides_with(self, sprite: BaseSprite):
        """Check if a sprite collides with another sprite.

        :param sprite: :ref:`BaseSprite`
            The sprite to check collisions with.
        """

    def update_position(self):
        """Update the position of the sprite."""
        ...