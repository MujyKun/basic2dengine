from models import Sprite, Image, Scene, Movement, MovementManipulator, Angle, Action


if __name__ == '__main__':
    velocity = MovementManipulator(1, 3)
    movement = Movement(velocity=velocity)
    sprite = Sprite(movement=movement, bounded_action=Action.stop())
    Scene("Test", sprites=[sprite]).start()

