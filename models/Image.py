from pathlib import Path

import pygame

from . import Size, Angle


ASSETS_FOLDER_PATH = f"{Path(__file__).parent.parent.absolute()}/assets"
DEFAULT_IMAGE = ASSETS_FOLDER_PATH + "/default.png"


class Image:
    """
    Stores the information of an image such as a name and file location.

    :param image_name: Optional[str]
        The image name.
    :param file_location: Optional[str]
        The absolute or relative file location.
    """
    def __init__(self, size: Size, image_name=None, file_location=None):
        self.size: Size = size
        self.image_name = image_name or "DEFAULT"
        self.file_location = file_location or DEFAULT_IMAGE
        self._surface = None
        # helps for rotating an image at an angle without distorting the image.
        self.no_rotation_surface = None

    @property
    def surface(self):
        """Return a pygame surface.

        ..Note:: Is defined as a property because the pygame display must be initialized first.
        """
        if not self._surface:
            self.no_rotation_surface = pygame.transform.scale(
                pygame.image.load(self.file_location), self.size.get_tuple()).convert()
            self._surface = self.no_rotation_surface
        return self._surface

    @surface.setter
    def surface(self, new_surface):
        """Set a new surface."""
        self._surface = new_surface

    def rotate(self, angle: Angle):
        new_surface = pygame.transform.rotate(self.no_rotation_surface, angle.angle_in_degrees)
        old_rect = self.no_rotation_surface.get_rect().copy()
        old_rect.center = new_surface.get_rect().center
        new_surface = new_surface.subsurface(old_rect).convert()
        new_surface_rect = new_surface.get_rect()
        self.surface = new_surface
        return new_surface_rect




