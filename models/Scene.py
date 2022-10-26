from typing import List

import pygame

from . import Size, MovementManipulator, Sprite, Visibility, Color


class Scene(Visibility):
    """
    Represents a Scene.

    :param title: str
        The title of the scene.
    :param size: Optional[:ref:`Size`]
        The size instance of the scene.
    :param position: Optional[:ref:`MovementManipulator`]
        The position instance of the scene.
    :param frame_rate: int
        The frame rate of the scene.
    :param sprites: Optional[List[:ref:`BaseSprite`]]
         A list of sprites.
    :param visibility: bool
        Whether the sprite is visible.

    """
    def __init__(self, title: str, size: Size = None, position: MovementManipulator = None, frame_rate: int = 60,
                 sprites: List[Sprite] = None, visibility: bool = True):
        super(Scene, self).__init__(visibility)
        self.title = title
        self.size: Size = size or Size(1280, 720)
        self.position = position or MovementManipulator(0, 0)
        self.frame_rate = abs(frame_rate)
        self.sprites: List[Sprite] = sprites or []
        self.sprite_groups = []

        pygame.init()
        self.screen = pygame.display.set_mode(self.size.get_tuple())
        self.clock = pygame.time.Clock()
        self.background = pygame.Surface(self.size.get_tuple())
        self.background.fill(Color.white())
        self.active = False

    def start(self):
        """Start the scene."""
        self.sprite_groups.append(pygame.sprite.OrderedUpdates(*self.sprites))
        pygame.display.set_caption(self.title)
        self.screen.blit(self.background, (0, 0))
        self.active = True

        while self._run_loop() is not False and self.active:
            continue

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            return False

    def _run_loop(self):
        """Main Loop for the scene."""
        self.clock.tick(self.frame_rate)

        for event in pygame.event.get():
            if self.handle_event(event) is False:
                return False

        self.update()

        for sprite_group in self.sprite_groups:
            sprite_group.clear(self.screen, self.background)
            sprite_group.update()
            sprite_group.draw(self.screen)

        pygame.display.flip()

    def update(self):
        """Update the scene and check for collision detection."""
        # for sprite in self.sprites:
        #     sprite.collides_with()


    def clear(self):
        """Clear the scene."""

    def stop(self):
        """Stop/End the scene."""
        self.active = False

    def pause(self):
        """Pause the scene."""

    def save(self):
        """Save the scene."""

    def load(self):
        """Load the scene."""

    def hide_cursor(self):
        """Hide the cursor."""

    def show_cursor(self):
        """Show the cursor."""
