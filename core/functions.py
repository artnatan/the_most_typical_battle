# движение юнита
def move(selected_units):
    active_unit, target_unit = selected_units[0], selected_units[1]

    if active_unit.can_swap_with(target_unit):
        # Обмен местами
        active_unit.x, target_unit.x = (
            target_unit.x,
            active_unit.x,
        )
        active_unit.y, target_unit.y = (
            target_unit.y,
            active_unit.y,
        )
        for unit in selected_units:
            unit.active = False
        selected_units = []  # Очищаем список выбранных юнитов


# атака
def attack(selected_units):
    active_unit, target_unit = selected_units[0], selected_units[1]

    if (
        active_unit.side != target_unit.side
        and active_unit.side != None
        and target_unit.side != None
    ):
        active_unit.number_soldiers, target_unit.number_soldiers = (
            active_unit.number_soldiers - target_unit.number_soldiers,
            target_unit.number_soldiers - active_unit.number_soldiers,
        )

        for unit in selected_units:
            unit.active = False
        selected_units = []  # Очищаем список выбранных юнитов
