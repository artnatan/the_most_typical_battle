import random
from core.commands.Command import Command
from core.sounds_dict import sounds_dict


class CrossbowVolley(Command):
    def __init__(self, active, name, rect, color, image):
        super().__init__(active, name, rect, color, image)
        self.sound_name = sounds_dict.get("crossbow")

    def apply(self, unit):
        unit.number_soldiers -= random.randint(3, 6)
