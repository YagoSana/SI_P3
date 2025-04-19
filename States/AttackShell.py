from StateMachine.State import State
from States.AgentConsts import AgentConsts

class AttackShell(State):

    def __init__(self, id):
        super().__init__(id)
        self.directionToLook = -1  # Dirección deseada para atacar

    def Update(self, perception, map, agent):
        # Verifica si el agente ya está orientado correctamente hacia la dirección de la bala
        if perception[AgentConsts.CAN_FIRE] == 1 and agent.directionToLook == self.directionToLook:
            # Si puede disparar, lo hace y se queda quieto
            return AgentConsts.NO_MOVE, True
        elif agent.directionToLook != self.directionToLook:
            # Si no está orientado correctamente, gira hacia la dirección de la bala
            return self.directionToLook, False
        else:
            # Si no puede disparar aún, espera
            return AgentConsts.NO_MOVE, True

    def Transit(self, perception, map):
        if perception[self.directionToLook] != AgentConsts.SHELL:
            return "ExecutePlan"
        return self.id
