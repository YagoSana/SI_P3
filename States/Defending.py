from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random


#La ultima opcion deberia ser acercarse hacia la bala si no podemos disparar, en casos extremos nos moveremos en direccion contraria a ella, buscaremos siempre un hueco para esquivarla
def defending(self, perception):
    print("Me estoy defendiendo")
    direccion_bala = -1
    direcciones_vacias = []

    # Buscar la dirección de la bala y las direcciones vacías
    for i, moves in enumerate(directions):
        if perception[moves] == AgentConsts.SHELL:
            print("BALA DETECTADA")
            direccion_bala = i  # Dirección de la bala

            #review
            self.status = AgentConsts.DEFENDING

        elif perception[moves] == AgentConsts.NOTHING:
            direcciones_vacias.append(i)  # Guardamos las direcciones vacías

    # Si encontramos una bala y no podemos disparar, intentamos esquivarla
    if direccion_bala != -1 and perception[AgentConsts.CAN_FIRE] == 0:
        if direccion_bala == AgentConsts.NEIGHBORHOOD_DOWN:
            if perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.NOTHING:
                self.last_move = AgentConsts.MOVE_LEFT
                return AgentConsts.MOVE_LEFT, 0
            elif perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.NOTHING:
                self.last_move = AgentConsts.MOVE_RIGHT
                return AgentConsts.MOVE_RIGHT, 0
            elif perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.NOTHING:
                self.last_move = AgentConsts.MOVE_UP
                return AgentConsts.MOVE_UP, 0
        elif direccion_bala == AgentConsts.NEIGHBORHOOD_UP:
            if perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.NOTHING:
                self.last_move = AgentConsts.MOVE_LEFT
                return AgentConsts.MOVE_LEFT, 0
            elif perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.NOTHING:
                self.last_move = AgentConsts.MOVE_RIGHT
                return AgentConsts.MOVE_RIGHT, 0
            elif perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.NOTHING:
                self.last_move = AgentConsts.MOVE_DOWN
                return AgentConsts.MOVE_DOWN, 0
        elif direccion_bala == AgentConsts.NEIGHBORHOOD_LEFT:
            if perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.NOTHING:
                self.last_move = AgentConsts.MOVE_UP
                return AgentConsts.MOVE_UP, 0
            elif perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.NOTHING:
                self.last_move = AgentConsts.MOVE_DOWN
                return AgentConsts.MOVE_DOWN, 0
            elif perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.NOTHING:
                self.last_move = AgentConsts.MOVE_RIGHT
                return AgentConsts.MOVE_RIGHT, 0
        elif direccion_bala == AgentConsts.NEIGHBORHOOD_RIGHT:
            if perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.NOTHING:
                self.last_move = AgentConsts.MOVE_UP
                return AgentConsts.MOVE_UP, 0
            elif perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.NOTHING:
                self.last_move = AgentConsts.MOVE_DOWN
                return AgentConsts.MOVE_DOWN, 0
            elif perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.NOTHING:
                self.last_move = AgentConsts.MOVE_LEFT
                return AgentConsts.MOVE_LEFT, 0

    # Si no podemos esquivar, intentamos movernos en la dirección opuesta a la bala
    if direccion_bala in [AgentConsts.NEIGHBORHOOD_UP, AgentConsts.NEIGHBORHOOD_DOWN, AgentConsts.NEIGHBORHOOD_LEFT, AgentConsts.NEIGHBORHOOD_RIGHT]:
        if direccion_bala == AgentConsts.NEIGHBORHOOD_UP and perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.NOTHING:
            self.last_move = AgentConsts.MOVE_DOWN
            return AgentConsts.MOVE_DOWN, 0
        elif direccion_bala == AgentConsts.NEIGHBORHOOD_DOWN and perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.NOTHING:
            self.last_move = AgentConsts.MOVE_UP
            return AgentConsts.MOVE_UP, 0
        elif direccion_bala == AgentConsts.NEIGHBORHOOD_LEFT and perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.NOTHING:
            self.last_move = AgentConsts.MOVE_RIGHT
            return AgentConsts.MOVE_RIGHT, 0
        elif direccion_bala == AgentConsts.NEIGHBORHOOD_RIGHT and perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.NOTHING:
            self.last_move = AgentConsts.MOVE_LEFT
            return AgentConsts.MOVE_LEFT, 0
    
    # Si no hay escapatoria, giramos hacia la dirección de la bala y disparamos
    if direccion_bala != -1:
        print("No hay escapatoria, girando hacia la bala y disparando")
        self.status = AgentConsts.ATTACKING
        self.last_move = AgentConsts.DIRECTIONS[direccion_bala]
        return AgentConsts.DIRECTIONS[direccion_bala], AgentConsts.ACTION_FIRE  # Girar hacia la bala y disparar

    # Si no hay amenaza, permanecemos en el lugar y cambiamos al modo attacking para seguir pendiente de amenazas
    self.status = AgentConsts.ATTACKING
    return 0, AgentConsts.NOTHING