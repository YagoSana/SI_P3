from StateMachine.State import State
from States.AgentConsts import AgentConsts
from MyProblem.BCProblem import BCProblem

class DistanceAttack(State):

    def __init__(self, id):
        super().__init__(id)
        self.directionToLook = -1

    def Start(self, agent):
        self.transition = ""

    def Update(self, perception, map, agent):
        # Obtener posición del agente
        xW = perception[AgentConsts.AGENT_X]
        yW = perception[AgentConsts.AGENT_Y]
        x, y = BCProblem.WorldToMapCoordFloat(xW, yW, agent.problem.ySize)
        x = int(x)
        y = int(y)

        # Buscar objetivo alineado y línea despejada
        found, direction = self.FindTargetDirection(map, x, y)
        if found:
            self.directionToLook = direction
            agent.directionToLook = direction
            return 0, True  # Disparo
        return AgentConsts.NO_MOVE, False

    def Transit(self, perception, map):
        # Volver al estado ExecutePlan si ya no hay objetivo visible
        if self.directionToLook == -1:
            return "ExecutePlan"

        target = perception[self.directionToLook]
        if target not in (AgentConsts.PLAYER, AgentConsts.COMMAND_CENTER):
            return "ExecutePlan"
        return self.id

    def FindTargetDirection(self, map, x, y):
        maxX, maxY = len(map), len(map[0])
        
        # Ver arriba
        for j in range(y - 1, -1, -1):
            if self.isBlocked(map[x][j]):
                break
            if map[x][j] in (AgentConsts.PLAYER, AgentConsts.COMMAND_CENTER):
                if self.isClearLine(x, y, x, j, map, vertical=True):
                    return True, AgentConsts.LOOK_UP

        # Ver abajo
        for j in range(y + 1, maxY):
            if self.isBlocked(map[x][j]):
                break
            if map[x][j] in (AgentConsts.PLAYER, AgentConsts.COMMAND_CENTER):
                if self.isClearLine(x, y, x, j, map, vertical=True):
                    return True, AgentConsts.LOOK_DOWN

        # Ver izquierda
        for i in range(x - 1, -1, -1):
            if self.isBlocked(map[i][y]):
                break
            if map[i][y] in (AgentConsts.PLAYER, AgentConsts.COMMAND_CENTER):
                if self.isClearLine(x, y, i, y, map, vertical=False):
                    return True, AgentConsts.LOOK_LEFT

        # Ver derecha
        for i in range(x + 1, maxX):
            if self.isBlocked(map[i][y]):
                break
            if map[i][y] in (AgentConsts.PLAYER, AgentConsts.COMMAND_CENTER):
                if self.isClearLine(x, y, i, y, map, vertical=False):
                    return True, AgentConsts.LOOK_RIGHT

        return False, -1

    def isBlocked(self, value):
        return value == AgentConsts.UNBREAKABLE or value == AgentConsts.SEMI_UNBREKABLE

    def isClearLine(self, x1, y1, x2, y2, map, vertical):
        if vertical:
            for y in range(min(y1, y2) + 1, max(y1, y2)):
                if self.isBlocked(map[x1][y]):
                    return False
        else:
            for x in range(min(x1, x2) + 1, max(x1, x2)):
                if self.isBlocked(map[x][y1]):
                    return False
        return True
