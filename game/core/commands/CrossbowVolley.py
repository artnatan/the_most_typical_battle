import random
from core.commands.Command import Command


class CrossbowVolley(Command):
    def __init__(self, active, name, rect, color, image):
        super().__init__(active, name, rect, color, image)

    def apply(self, unit):
        unit.number_soldiers -= random.randint(3, 6)
