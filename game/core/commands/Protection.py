from core.commands.Command import Command


class Protection(Command):
    def __init__(self, active, name, rect, color, image):
        super().__init__(active, name, rect, color, image)

    def apply(self, unit):
        unit.protected = True
