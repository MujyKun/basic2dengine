from typing import Callable, List, Sequence


class Trigger:
    """
    A trigger function for calling a function on a key press.

    :param key:
        The key that needs to be pressed to trigger the function.
    :param func: Callable
        The function to call. Must take the key pressed as a parameter.
    """
    def __init__(self, key, func: Callable):
        self.key = key
        self.func = func


class KeyboardTrigger:
    """
    Handle keyboard input.

    :param trigger_functions: List[:ref:`Trigger`]
        A list of triggers
    """
    def __init__(self, trigger_functions: List[Trigger] = None):
        self.trigger_functions = trigger_functions or []

    def run(self, pressed_keys: Sequence[bool]):
        """
        Run the trigger functions if a trigger key is pressed.

        :param pressed_keys: Sequence[bool]
            A list of pressed keys
        """
        _ = [trigger.func(trigger.key) for trigger in self.trigger_functions if pressed_keys[trigger.key]]

