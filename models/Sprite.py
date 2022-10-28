from typing import List

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
    :param bounded_action: :ref:`Action`
        The action instance for hitting the boundaries of a scene.
    :param collision_action: :ref:`Action`
        The action instance for hitting the boundaries of a sprint.
    """

    def __init__(self, size: Size = None,
                 image: Image = None,
                 movement: Movement = None,
                 visibility: bool = True, scene_size: Size = None, bounded_action: Action = None,
                 collision_action: Action = None):
        super(Sprite, self).__init__()
        self.size: Size = size or Size(100, 100)
        self.image_obj: Image = image or Image(self.size)
        # The sprite size must match the image size.
        # The image may change the size to fit.
        self.size = self.image_obj.size
        self.movement: Movement = movement or Movement()
        self.__visibility = Visibility(visibility)
        self._rect = None
        self._rect_surface = None
        self._scene_size = scene_size or Size(1280, 720)
        self._bounded_action = bounded_action or Action.wrap()
        self.collision_action = collision_action or Action.bounce()
        self.stationary_collisions = []
        self._invert_v_x = False
        self._invert_v_y = False
        self._interacted_with_scene = False  # Know if our display is constantly updating.

    @property
    def rect(self):
        """Get the object's rect.

        ..Note:: This bypasses pygame needing to be initialized first.
        """
        if not self._rect:
            self._rect = self.image_obj.surface.get_rect()

            if not self.static:
                pos = self.movement.position.get_tuple()
                if pos == (0, 0):
                    pos = (self._rect.x, self._rect.y)
                self.movement.set_position(*pos)
            elif self.image_obj.wallpaper:
                self._rect.x, self._rect.y = (0, 0)
            else:
                self._rect.centerx, self._rect.centery = self.movement.position.get_tuple()

            self._rect_surface = self.image_obj.surface

        if self._rect_surface != self.image_obj.surface:
            self._rect = None
            return self.rect  # recursive reset.
        return self._rect

    @property
    def visible(self):
        return self.__visibility.visible

    @property
    def static(self):
        return self.movement.static

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
        """Get the left of the sprite."""
        return self.rect.left

    @property
    def right(self):
        """Get the right of the sprite."""
        return self.rect.right

    @property
    def top(self):
        """Get the top of the sprite."""
        return self.rect.top

    @property
    def bottom(self):
        """Get the bottom of the sprite."""
        return self.rect.bottom

    def collides_with(self, sprite, visible=True, return_results=False):
        """Check if a sprite collides with another sprite.

        :param sprite: :ref:`Sprite`
            The sprite to check collisions with.
        :param visible: bool
            Whether the object needs to be visible or not.
        :param return_results: bool
            Return the results.
        """
        if (visible and not (self.visible and sprite.visible)) or self == sprite:
            return False

        # instead of checking to see if the sprites are inside each other (inherently more complex),
        # we check if they are outside.
        results = [self.bottom < sprite.top, self.top > sprite.bottom, self.right < sprite.left,
                   self.left > sprite.right]

        if return_results:
            return results

        if any(results):
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

        wrap = Action.wrap() == self._bounded_action

        if top_check:
            new_y = self._scene_size.height if wrap else 0
        if bottom_check:
            new_y = 0 if wrap else self._scene_size.height
        if left_check:
            new_x = self._scene_size.width if wrap else 0
        if right_check:
            new_x = 0 if wrap else self._scene_size.width

        out_of_bounds = any([top_check, bottom_check, left_check, right_check])

        if Action.die() == self._bounded_action and out_of_bounds:
            self.hide()
        if Action.bounce() == self._bounded_action and out_of_bounds:
            if bottom_check or top_check:
                self.movement.velocity.y *= -1
            if right_check or left_check:
                self.movement.velocity.x *= -1

        self.movement.set_position(new_x, new_y)

    def _update_position_and_angle(self):
        """Update the position of the sprite."""
        if not self.visible or self.static:
            return

        if not self.image_obj.no_rotation_surface:
            _ = self.image_obj.surface

        self._rect = self.image_obj.rotate(self.movement.img_angle)
        self._rect_surface = self.image_obj.surface
        # self.movement.add_vector(Angle(degrees=20), 5)
        self.movement.update()
        self._rect.centerx = self.movement.position.x
        self._rect.centery = self.movement.position.y

    def _check_collisions(self):
        """Check sprite collision and apply appropriate action."""
        if self._invert_v_y:
            self.movement.velocity.y *= -1
            self._invert_v_y = False
        if self._invert_v_x:
            self.movement.velocity.x *= -1
            self._invert_v_x = False

        if not self._interacted_with_scene:
            return

        colliding_sprites: List[Sprite] = [sprite for sprite_group in self.groups()
                                           for sprite in sprite_group.sprites()
                                           if self != sprite and self.collides_with(sprite, visible=True)]
        if not colliding_sprites or self.collision_action.pass_through() == self.collision_action:
            return

        for sprite in colliding_sprites:
            if self.image_obj.wallpaper:
                continue

            self._handle_collision(sprite)

    def _handle_collision(self, sprite):
        """Handle the collisions of a sprite."""
        if sprite.image_obj.wallpaper:
            return

        # Check if the objects disappear.
        both_static = self.static and sprite.static
        if Action.die() == self.collision_action and \
                Action.pass_through() != sprite.collision_action and not both_static:
            self.hide()
        if Action.die() == sprite.collision_action and \
                Action.pass_through() != self.collision_action and not both_static:
            sprite.hide()

        # confirm both objects are still visible unless we need to bounce.
        if not (sprite.visible and self.visible) and \
                not (Action.bounce() in [self.collision_action, sprite.collision_action]):
            return

        if Action.pass_through() in [self.collision_action, sprite.collision_action]:
            return

        # handle bounce for current sprite.
        if Action.bounce() == self.collision_action:
            self._handle_bounce(self, sprite)

        # This is the only case where we handle the bounce of the other sprite because we do not want to
        # bounce against this object in the future when it is not visible or it is static.
        # this sprite object will not have to handle the bounce again.
        other_sprite_bounce = Action.bounce() == sprite.collision_action
        other_sprite_dynamic = not sprite.static
        current_sprite_invisible = not self.visible
        current_sprite_die = Action.die() == self.collision_action

        handle_other_sprite = other_sprite_bounce and \
                              ((other_sprite_dynamic) or
                               current_sprite_invisible)
        if handle_other_sprite:
            sprite.stationary_collisions.append(self)
            if not self.visible:
                self._handle_bounce(sprite, self)

    @staticmethod
    def _handle_bounce(sprite, collided_sprite):
        if sprite.static:
            return

        def inverse_current_sprite_velocity():
            results = sprite.collides_with(collided_sprite, return_results=True)
            if any(results):
                if abs(sprite.movement.velocity.x) > abs(sprite.movement.velocity.y):
                    sprite.movement.velocity.x *= -1
                else:
                    sprite.movement.velocity.y *= -1
            else:
                sprite.movement.update_move_angle()
                angle = Angle.normalize_degrees(sprite.movement.move_angle.angle_in_degrees)
                # touching_left_side = collided_sprite.right > sprite.right > collided_sprite.left
                # touching_bot_side = collided_sprite.top > sprite.top > collided_sprite.bottom
                # touching_top_side = collided_sprite.bottom > sprite.bottom > collided_sprite.top
                # touching_right_side = collided_sprite.left < sprite.left < collided_sprite.right

                left_diff = abs(sprite.right - collided_sprite.left) or 0
                bot_diff = abs(sprite.top - collided_sprite.bottom) or 0
                top_diff = abs(sprite.bottom - collided_sprite.top) or 0
                right_diff = abs(sprite.left - collided_sprite.right) or 0

                if angle in range(0, 90):  # top left
                    if max(top_diff, left_diff) == top_diff:
                        sprite.movement.velocity.x *= -1
                    else:
                        sprite.movement.velocity.y *= -1
                elif angle in range(90, 180):  # top right
                    if max(top_diff, right_diff) == top_diff:
                        sprite.movement.velocity.x *= -1
                    else:
                        sprite.movement.velocity.y *= -1

                elif angle in range(180, 270):  # bottom right
                    if max(bot_diff, right_diff) == bot_diff:
                        sprite.movement.velocity.x *= -1
                    else:
                        sprite.movement.velocity.y *= -1
                else:
                    if max(bot_diff, left_diff) == bot_diff:  # bottom left
                        sprite.movement.velocity.x *= -1
                    else:
                        sprite.movement.velocity.y *= -1

        if not sprite.movement.is_moving:
            # current object is stationary.
            # move the direction of the collided object.
            sprite.movement.add_vector(collided_sprite.movement.move_angle)
            # we cannot find out if a sprite was stationary since its velocity is now non-zero.
            # we store the information in our collided sprite instead since
            # we do not modify the collided sprites here.
            collided_sprite.stationary_collisions.append(sprite)
        else:
            # current object is moving, move the opposite direction of the collided object.
            if collided_sprite in sprite.stationary_collisions:  # our collided_sprite was once stationary.
                # check how much we've moved in a direction to determine which direction to change.
                if collided_sprite.movement.velocity.get_tuple() == (0, 0):
                    inverse_current_sprite_velocity()
                elif abs(collided_sprite.movement.velocity.x) > abs(collided_sprite.movement.velocity.y):
                    sprite.movement.velocity.x *= -1
                else:
                    sprite.movement.velocity.y *= -1
                sprite.stationary_collisions.remove(collided_sprite)  # we do not need this information anymore.
            elif collided_sprite.movement.is_moving:
                # Check if the current sprite needs to be inverted.
                s_x_neg = sprite.movement.velocity.x < 0  # sprite velocity x negative
                s_y_neg = sprite.movement.velocity.y < 0  # sprite velocity y negative
                cs_x_neg = collided_sprite.movement.velocity.x < 0  # collided sprite velocity x negative
                cs_y_neg = collided_sprite.movement.velocity.y < 0  # collided sprite velocity y negative

                # handle direction of current sprite.
                # heading towards each other in the x direction
                if (s_x_neg and not cs_x_neg) or (cs_x_neg and not s_x_neg):
                    sprite.movement.velocity.x *= -1  # repel in x direction
                    collided_sprite._invert_v_x = True
                # heading towards each other in the y direction
                elif (s_y_neg and not cs_y_neg) or (cs_y_neg and not s_y_neg):
                    sprite.movement.velocity.y *= -1  # repel in y direction
                    collided_sprite._invert_v_y = True

            else:
                # Handle stationary objects against moving objects.
                inverse_current_sprite_velocity()

    def update(self):
        """Update the sprite."""
        if not self.visible:
            return

        self._check_bounds()  # check bounds
        self._check_collisions()
        self._update_position_and_angle()  # update pos

        if not self._interacted_with_scene:
            self._interacted_with_scene = True
