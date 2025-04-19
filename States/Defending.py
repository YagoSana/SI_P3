from StateMachine.State import State
from States.AgentConsts import AgentConsts

class Defending(State):

    def __init__(self, id):
        super().__init__(id)
        self.last_move = AgentConsts.NO_MOVE
        self.directionToLook = -1

    def Update(self, perception, map, agent):
        # Detectar la dirección de la bala
        direccion_bala = -1
        for i, move in enumerate([AgentConsts.NEIGHBORHOOD_UP, AgentConsts.NEIGHBORHOOD_DOWN, 
                                  AgentConsts.NEIGHBORHOOD_LEFT, AgentConsts.NEIGHBORHOOD_RIGHT]):
            if perception[move] == AgentConsts.SHELL:
                direccion_bala = i  # Dirección de la bala detectada
                self.directionToLook = direccion_bala
                print("BALA DETECTADA")

        # Verificar si el agente ya está en la posición adecuada para disparar
        if direccion_bala != -1 and perception[AgentConsts.CAN_FIRE] == 1:
            print("Disparando a la bala")
            return self.ShootAtBullet(perception, direccion_bala)

        # Si no podemos disparar, intentar esquivar la bala o mover en la dirección opuesta
        if direccion_bala != -1 and perception[AgentConsts.CAN_FIRE] == 0:
            return self.EvadeBullet(perception, direccion_bala)

        # Si no hay amenaza, permanecemos en el lugar
        return AgentConsts.NO_MOVE, 0

    def Transit(self, perception, map):
        # Si no hay bala o si ya no estamos en defensa, volvemos al estado de plan de ejecución
        if self.last_move == AgentConsts.NO_MOVE:
            return "ExecutePlan"
        return self.id

    def ShootAtBullet(self, perception, direccion_bala):
        """Intentamos disparar a la bala si estamos en posición."""
        print("Agente en posición para disparar")
        # Aquí se puede implementar la lógica para disparar directamente si el agente está en la posición correcta
        return AgentConsts.NO_MOVE, 1  # Retorna un movimiento nulo pero indica que disparó (1)

    def EvadeBullet(self, perception, direccion_bala):
        """Intentamos esquivar la bala si no podemos disparar."""
        if direccion_bala == AgentConsts.NEIGHBORHOOD_DOWN:
            return self.TryMove(perception, AgentConsts.NEIGHBORHOOD_LEFT, AgentConsts.MOVE_LEFT) or \
                   self.TryMove(perception, AgentConsts.NEIGHBORHOOD_RIGHT, AgentConsts.MOVE_RIGHT) or \
                   self.TryMove(perception, AgentConsts.NEIGHBORHOOD_UP, AgentConsts.MOVE_UP)

        elif direccion_bala == AgentConsts.NEIGHBORHOOD_UP:
            return self.TryMove(perception, AgentConsts.NEIGHBORHOOD_LEFT, AgentConsts.MOVE_LEFT) or \
                   self.TryMove(perception, AgentConsts.NEIGHBORHOOD_RIGHT, AgentConsts.MOVE_RIGHT) or \
                   self.TryMove(perception, AgentConsts.NEIGHBORHOOD_DOWN, AgentConsts.MOVE_DOWN)

        elif direccion_bala == AgentConsts.NEIGHBORHOOD_LEFT:
            return self.TryMove(perception, AgentConsts.NEIGHBORHOOD_UP, AgentConsts.MOVE_UP) or \
                   self.TryMove(perception, AgentConsts.NEIGHBORHOOD_DOWN, AgentConsts.MOVE_DOWN) or \
                   self.TryMove(perception, AgentConsts.NEIGHBORHOOD_RIGHT, AgentConsts.MOVE_RIGHT)

        elif direccion_bala == AgentConsts.NEIGHBORHOOD_RIGHT:
            return self.TryMove(perception, AgentConsts.NEIGHBORHOOD_UP, AgentConsts.MOVE_UP) or \
                   self.TryMove(perception, AgentConsts.NEIGHBORHOOD_DOWN, AgentConsts.MOVE_DOWN) or \
                   self.TryMove(perception, AgentConsts.NEIGHBORHOOD_LEFT, AgentConsts.MOVE_LEFT)

        return AgentConsts.NO_MOVE, 0

    def MoveAwayFromBullet(self, perception, direccion_bala):
        """Si no podemos esquivar, intentamos movernos en la dirección opuesta a la bala."""
        if direccion_bala == AgentConsts.NEIGHBORHOOD_UP and perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.NOTHING:
            return AgentConsts.MOVE_DOWN, 0
        elif direccion_bala == AgentConsts.NEIGHBORHOOD_DOWN and perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.NOTHING:
            return AgentConsts.MOVE_UP, 0
        elif direccion_bala == AgentConsts.NEIGHBORHOOD_LEFT and perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.NOTHING:
            return AgentConsts.MOVE_RIGHT, 0
        elif direccion_bala == AgentConsts.NEIGHBORHOOD_RIGHT and perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.NOTHING:
            return AgentConsts.MOVE_LEFT, 0

        return AgentConsts.NO_MOVE, 0

    def TryMove(self, perception, direction, move):
        """Intenta mover en la dirección indicada si está libre."""
        if perception[direction] == AgentConsts.NOTHING:
            self.last_move = move
            return move, 0
        return AgentConsts.NO_MOVE, 0
