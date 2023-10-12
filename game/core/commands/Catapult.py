import random
from core.commands.Command import Command
from core.sounds_dict import sounds_dict


class Catapult(Command):
    def __init__(self, active, name, rect, color, image):
        super().__init__(active, name, rect, color, image)
        self.sound_name = sounds_dict.get("catapult")

    def apply(self, unit):
        unit.number_soldiers -= random.randint(10, 16)
