from random import randint

import pygame

from models import Sprite, Image, Scene, Movement, MovementManipulator, Angle, Action, Size, KeyboardTrigger, Trigger

SCENE_WIDTH = 1080
SCENE_HEIGHT = 720

SCENE_WIDTH = 1920
SCENE_HEIGHT = 1080


def create_brick_sprites():
    """Create the brick sprites."""
    brick_sprites = []
    size = Size(384 // 3, 128 // 3)

    brick_start_width = 0.15 * scene_size.width
    brick_end_width = 0.85 * scene_size.width

    brick_start_height = 0.10 * scene_size.height
    brick_end_height = 0.50 * scene_size.height

    i_start_range = 0
    i_end_range = 0
    j_start_range = 0
    j_end_range = 0

    while True:
        # calculate the number of bricks that should be applied to the resolution.
        next_x = (i_end_range + 1) * size.width
        next_y = (j_end_range + 1) * size.height
        if brick_start_width < next_x < brick_end_width:
            i_end_range += 1
        elif next_x < brick_start_width:
            i_start_range += 1
            i_end_range += 1
        elif brick_start_height < next_y < brick_end_height:
            j_end_range += 1
        elif next_y < brick_start_height:
            j_start_range += 1
            j_end_range += 1
        else:
            break

    for i in range(i_start_range, i_end_range):
        for j in range(j_start_range, j_end_range):
            x = (i * size.width)
            y = (j * size.height)
            img = Image(size=size, image_name=f"tile{i}-{j}", file_location="assets/blue_tile.png")
            position = MovementManipulator(x, y)
            movement = Movement(static=True, position=position)
            sprite = Sprite(image=img, movement=movement, scene_size=scene_size, collision_action=Action.hide())
            brick_sprites.append(sprite)
    return brick_sprites


def create_ball_sprite():
    """Create a ball sprite."""
    return Sprite(
        image=Image(size=Size(24, 24),
                    image_name=f"ball",
                    file_location="assets/ball.png"),
        movement=Movement(
            static=False,
            position=MovementManipulator(600, 600),
            velocity=MovementManipulator(-5, -5)),
        bounded_action=Action.bounce(), collision_action=Action.bounce(), scene_size=scene_size,
        angle_collision=True
    )


def create_player_platform():
    """Create player platform."""
    return Sprite(
        image=Image(size=Size(200, 40), image_name="player_platform", file_location="assets/platform.png"),
        bounded_action=Action.wrap(),
        scene_size=scene_size,
        angle_collision=False,
        movement=Movement(
            position=MovementManipulator(scene_size.width // 2, 0.99 * scene_size.height)
        ), player_controlled=True
    )


def create_platform_triggers(sprite):
    """Create triggers for the platform."""
    def move(key):
        if key == pygame.K_LEFT:
            sprite.movement.add_vector(Angle(degrees=180), thrust=1)
        elif key == pygame.K_RIGHT:
            sprite.movement.add_vector(Angle(degrees=0), thrust=1)

    def spawn_ball(key):
        if key == pygame.K_SPACE:
            new_ball = create_ball_sprite()
            new_ball.movement.set_position(sprite.rect.centerx, sprite.rect.centery - 20)
            new_ball.movement.velocity.x = 0
            new_ball.movement.velocity.y = -20
            new_ball.add(sprite.groups())

    return [Trigger(pygame.K_LEFT, move), Trigger(pygame.K_RIGHT, move), Trigger(pygame.K_SPACE, spawn_ball)]


def create_ball_death_floor():
    """Create a sprite for the ball's death."""
    return Sprite(
        image=Image(size=Size(scene_size.width, 2),
                    image_name=f"death",
                    file_location="assets/red_tile.png"),
        movement=Movement(
            static=True, position=MovementManipulator(scene_size.width / 2, scene_size.height),
            velocity=MovementManipulator(-5, -5)),
        collision_action=Action.kill_non_players(), scene_size=scene_size
    )


def create_wallpaper():
    """Create a wallpaper."""
    return Sprite(image=Image(scene_size, image_name="wallpaper", file_location="assets/sky2.jpg", wallpaper=True),
                  movement=Movement(position=MovementManipulator(scene_size.width/2, scene_size.height/2), static=True),
                  bounded_action=Action.pass_through(),
                  collision_action=Action.pass_through())


if __name__ == '__main__':
    scene_size = Size(SCENE_WIDTH, SCENE_HEIGHT)
    player_platform = create_player_platform()
    ball = create_ball_sprite()
    ball_death_floor = create_ball_death_floor()
    wallpaper = create_wallpaper()
    sprites = [wallpaper, ball_death_floor] + create_brick_sprites() + [ball, player_platform]
    platform_triggers = create_platform_triggers(player_platform)
    brick_breaker = Scene("Brick Breaker", sprites=sprites, size=scene_size,
                          keyboard_input=KeyboardTrigger(platform_triggers))
    brick_breaker.start()
