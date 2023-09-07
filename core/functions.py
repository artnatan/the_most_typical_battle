# движение юнита
def move(active_unit, target_unit):
    # Обмен местами
    active_unit.x, target_unit.x = (
        target_unit.x,
        active_unit.x,
    )
    active_unit.y, target_unit.y = (
        target_unit.y,
        active_unit.y,
    )


# атака
def attack(active_unit, target_unit):
    active_unit.number_soldiers, target_unit.number_soldiers = (
        active_unit.number_soldiers - target_unit.number_soldiers,
        target_unit.number_soldiers - active_unit.number_soldiers,
    )
