from random import randint

from models import Sprite, Image, Scene, Movement, MovementManipulator, Angle, Action, Size


# def create_brick_sprites():
#     movement = Movement(position=MovementManipulator(900, 300), static=True)
#     default_sprite = Sprite(movement=movement, bounded_action=Action.stop())
#
#     size = Size(384 // 3, 128 // 3)
#     img = Image(size=size, image_name=f"tile", file_location="assets/01-Breakout-Tiles.png")
#     position = MovementManipulator(1150, 600)
#     movement = Movement(static=True, position=position)
#     brick_sprite = Sprite(image=img, movement=movement, collision_action=Action.die())
#     return [default_sprite, brick_sprite]


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
            img = Image(size=size, image_name=f"tile{i}-{j}", file_location="assets/01-Breakout-Tiles.png")
            position = MovementManipulator(x, y)
            movement = Movement(static=True, position=position)
            sprite = Sprite(image=img, movement=movement, scene_size=scene_size, collision_action=Action.die())
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
        bounded_action=Action.bounce(), collision_action=Action.bounce(), scene_size=scene_size
    )


if __name__ == '__main__':
    scene_size = Size(1920, 1080)
    sprites = create_brick_sprites() + [create_ball_sprite()]
    brick_breaker = Scene("Brick Breaker", sprites=sprites, size=scene_size)
    brick_breaker.start()
