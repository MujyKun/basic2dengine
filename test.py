from models import Sprite, Image, Scene, Movement, MovementManipulator, Angle, Action, Size


wallpaper = Sprite(image=Image(Size(1280, 720), image_name="wallpaper", file_location="assets/wallpaper.jpg",
                               wallpaper=True),
                   movement=Movement(position=MovementManipulator(1280/2, 720/2), static=True),
                   bounded_action=Action.pass_through(),
                   collision_action=Action.pass_through())


def test_horizontal_movement():
    movement = Movement(position=MovementManipulator(300, 300), static=False)
    sprite = Sprite(movement=movement, bounded_action=Action.stop(), collision_action=Action.bounce())
    movement_2 = Movement(velocity=MovementManipulator(-3, 0), position=MovementManipulator(1280, 300))
    sprite_2 = Sprite(movement=movement_2, bounded_action=Action.stop(), collision_action=Action.bounce())
    Scene("Test", sprites=[wallpaper, sprite, sprite_2]).start()


def test_vertical_movement():
    movement = Movement(position=MovementManipulator(300, 300), static=False)
    image = Image(Size(100,100), image_name="stand_still")
    sprite = Sprite(image=image, movement=movement, bounded_action=Action.stop())
    movement_2 = Movement(velocity=MovementManipulator(0, -3), position=MovementManipulator(300, 720))
    sprite_2 = Sprite(movement=movement_2, bounded_action=Action.stop(), collision_action=Action.bounce())
    Scene("Test", sprites=[wallpaper, sprite, sprite_2]).start()


def test_diagonal_movement():
    movement = Movement(position=MovementManipulator(0, 0), velocity=MovementManipulator(3, 3), static=False)
    sprite = Sprite(movement=movement, bounded_action=Action.stop())
    movement_2 = Movement(velocity=MovementManipulator(-3, 3), position=MovementManipulator(1280, 0))
    sprite_2 = Sprite(movement=movement_2, bounded_action=Action.stop(), collision_action=Action.bounce())
    Scene("Test", sprites=[sprite, sprite_2]).start()


def test_static_movement_vertical():
    movement = Movement(position=MovementManipulator(300, 300), static=True)
    sprite = Sprite(movement=movement, bounded_action=Action.stop())
    movement_2 = Movement(velocity=MovementManipulator(0, -3), position=MovementManipulator(300, 720))
    sprite_2 = Sprite(movement=movement_2, bounded_action=Action.stop())
    Scene("Test", sprites=[sprite, sprite_2]).start()


def test_static_movement_horizontal():
    movement = Movement(position=MovementManipulator(300, 300), static=True)
    sprite = Sprite(movement=movement, bounded_action=Action.stop(), collision_action=Action.bounce())
    movement_2 = Movement(velocity=MovementManipulator(-3, 0), position=MovementManipulator(1280, 300))
    sprite_2 = Sprite(movement=movement_2, bounded_action=Action.stop(), collision_action=Action.bounce())
    Scene("Test", sprites=[wallpaper, sprite, sprite_2]).start()


def test_static_movement_diagonal_hit_top_right():
    movement = Movement(position=MovementManipulator(600, 600), static=True)
    sprite = Sprite(movement=movement, bounded_action=Action.stop())
    movement_2 = Movement(velocity=MovementManipulator(-3, 3), position=MovementManipulator(1280, 0))
    sprite_2 = Sprite(movement=movement_2, bounded_action=Action.stop())
    Scene("Test", sprites=[sprite, sprite_2]).start()


def test_static_movement_diagonal_hit_top_left():
    movement = Movement(position=MovementManipulator(600, 600), static=True)
    sprite = Sprite(movement=movement, bounded_action=Action.stop())
    movement_2 = Movement(velocity=MovementManipulator(3, 3), position=MovementManipulator(0, 0))
    sprite_2 = Sprite(movement=movement_2, bounded_action=Action.stop())
    Scene("Test", sprites=[sprite, sprite_2]).start()


def test_static_movement_diagonal_hit_bottom_left():
    movement = Movement(position=MovementManipulator(600, 150), static=True)
    sprite = Sprite(movement=movement, bounded_action=Action.stop())
    movement_2 = Movement(velocity=MovementManipulator(3, -3), position=MovementManipulator(0, 720))
    sprite_2 = Sprite(movement=movement_2, bounded_action=Action.stop())
    Scene("Test", sprites=[sprite, sprite_2]).start()


def test_static_movement_diagonal_hit_bottom_right():
    movement = Movement(position=MovementManipulator(600, 250), static=True)
    sprite = Sprite(movement=movement, bounded_action=Action.stop())
    movement_2 = Movement(velocity=MovementManipulator(-3, -3), position=MovementManipulator(1080, 720))
    sprite_2 = Sprite(movement=movement_2, bounded_action=Action.stop())
    Scene("Test", sprites=[sprite, sprite_2]).start()


def test_cross_movement():
    movement = Movement(position=MovementManipulator(0, 0), velocity=MovementManipulator(3, 3))
    sprite = Sprite(movement=movement, bounded_action=Action.stop())
    movement_2 = Movement(velocity=MovementManipulator(0, -3), position=MovementManipulator(300, 720))
    sprite_2 = Sprite(movement=movement_2, bounded_action=Action.stop(), collision_action=Action.bounce())
    Scene("Test", sprites=[sprite, sprite_2]).start()


def test_brick_and_default():
    scene_size = Size(1920, 1080)
    movement = Movement(position=MovementManipulator(1150, 600), static=True)
    default_sprite = Sprite(movement=movement, bounded_action=Action.stop(), collision_action=Action.bounce())

    size = Size(384 // 3, 128 // 3)
    img = Image(size=size, image_name=f"tile", file_location="assets/01-Breakout-Tiles.png")
    position = MovementManipulator(60, 600)
    movement = Movement(static=True, position=position)
    brick_sprite = Sprite(image=img, movement=movement, collision_action=Action.die())

    ball_sprite = Sprite(
        image=Image(size=Size(24, 24),
                    image_name=f"ball",
                    file_location="assets/ball.png"),
        movement=Movement(
            static=False,
            position=MovementManipulator(600, 600),
            velocity=MovementManipulator(-5, -5)),
        bounded_action=Action.bounce(), collision_action=Action.bounce(), scene_size=scene_size
    )

    Scene("Test", sprites=[default_sprite, brick_sprite, ball_sprite], size=scene_size).start()


if __name__ == '__main__':
    test_horizontal_movement()
    test_vertical_movement()
    test_diagonal_movement()
    test_cross_movement()
    test_static_movement_horizontal()
    test_static_movement_vertical()
    test_static_movement_diagonal_hit_top_right()
    test_static_movement_diagonal_hit_top_left()
    test_static_movement_diagonal_hit_bottom_left()
    test_static_movement_diagonal_hit_bottom_right()
    test_brick_and_default()

