def change_machine_state(machine, status, end=False):
    if machine.state.status == status:
        return
    for state in machine:
        if state.status == status:
            break
    if end:
        machine.next(end=True)


def recalculate_procedure():
    pass
