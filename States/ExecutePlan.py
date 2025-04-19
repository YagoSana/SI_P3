from StateMachine.State import State
from States.AgentConsts import AgentConsts
from MyProblem.BCProblem import BCProblem


class ExecutePlan(State):

    def __init__(self, id):
        super().__init__(id)
        self.nextNode = 0
        self.lastMove = 0
        self.transition = ""

    def Start(self, agent):
        self.transition = ""
        self.XPos = -1
        self.YPos = -1
        self.noMovements = 0

    def Update(self, perception, map, agent):
        shot = False
        move = self.lastMove
        xW = perception[AgentConsts.AGENT_X]
        yW = perception[AgentConsts.AGENT_Y]
        distance = abs(self.XPos - xW) + abs(self.YPos - yW)
        if distance < 0.1:
            self.noMovements += 1
        else:
            self.noMovements = 0

        # Detección de SHELLs en línea para entrar en modo ataque
        bullet_directions = [
            (AgentConsts.NEIGHBORHOOD_UP, 1),
            (AgentConsts.NEIGHBORHOOD_DOWN, 2),
            (AgentConsts.NEIGHBORHOOD_RIGHT, 3),
            (AgentConsts.NEIGHBORHOOD_LEFT, 4)
        ]
        for bullet, dir_val in bullet_directions:
            if perception[bullet] == AgentConsts.SHELL:
                self.transition = "AttackShell"
                agent.directionToLook = dir_val
                return AgentConsts.NO_MOVE, True

        x, y = BCProblem.WorldToMapCoordFloat(xW, yW, agent.problem.ySize)

        plan = agent.GetPlan()
        if len(plan) == 0:
            agent.goalMonitor.ForceToRecalculate()
            return AgentConsts.NO_MOVE, False

        nextNode = plan[0]
        if self.IsInNode(nextNode, x, y, self.lastMove, 0.17) and len(plan) > 1:
            plan.pop(0)
            if len(plan) == 0:
                agent.goalMonitor.ForceToRecalculate()
                return AgentConsts.NO_MOVE, False
            nextNode = plan[0]

        goal = agent.problem.GetGoal()

        # Nueva lógica de disparo
        targetX = goal.x + 0.5
        targetY = goal.y + 0.5
        alignedX = abs(x - targetX) < 0.2
        alignedY = abs(y - targetY) < 0.2

        canShoot = False
        if alignedX or alignedY:
            canShoot = self.ClearLineOfFire(x, y, targetX, targetY, agent)

        # Si no hay línea clara pero hay BRICKs en medio y es PLAYER, destruir cobertura
        if not canShoot and (alignedX or alignedY) and goal.value == AgentConsts.PLAYER:
            if self.BrickBlockingPath(x, y, goal.x, goal.y, agent.problem.map):
                print("PLAYER detrás de BRICK, disparando para destruir cobertura")
                canShoot = True

        if canShoot and perception[AgentConsts.CAN_FIRE] == 1:
            self.transition = "Attack"
            if alignedX:
                move = AgentConsts.MOVE_DOWN if targetY > y else AgentConsts.MOVE_UP
            else:
                move = AgentConsts.MOVE_RIGHT if targetX > x else AgentConsts.MOVE_LEFT
            agent.directionToLook = move - 1
            shot = True
            print(f"Shot: {shot}, disparando hacia cobertura o enemigo.")
        else:
            move = self.GetDirection(nextNode, x, y)
            shot = nextNode.value == AgentConsts.BRICK or nextNode.value == AgentConsts.COMMAND_CENTER
            print(f"Shot: {shot}, nextNode.value: {nextNode.value}, VALOR BRICK: {AgentConsts.BRICK}")

        self.lastMove = move
        return move, shot

    def Transit(self, perception, map):
        if self.transition != None and self.transition != "":
            return self.transition
        elif self.noMovements > 5:
            return "Random"
        return self.id

    @staticmethod
    def MoveDown(node, x, y):
        return abs(node.x + 0.5 - x) <= abs(node.y + 0.5 - y) and (node.y + 0.5) >= y

    @staticmethod
    def MoveUp(node, x, y):
        return abs(node.x + 0.5 - x) <= abs(node.y + 0.5 - y) and (node.y + 0.5) <= y

    @staticmethod
    def MoveRight(node, x, y):
        return abs(node.x + 0.5 - x) >= abs(node.y + 0.5 - y) and (node.x + 0.5) >= x

    @staticmethod
    def MoveLeft(node, x, y):
        return abs(node.x + 0.5 - x) >= abs(node.y + 0.5 - y) and (node.x + 0.5) <= x

    @staticmethod
    def IsInNode(node, x, y, lastDir, threshold):
        distanceX = abs((node.x + 0.5) - x)
        distanceY = abs((node.y + 0.5) - y)
        inAceptZone = distanceX < threshold and distanceY < threshold
        if inAceptZone:
            return True
        else:
            directionX, directionY = ExecutePlan.GetDirectionVector(lastDir)
            simulateX = x + directionX * threshold
            simulateY = y + directionY * threshold
            simulateDistanceX = abs((node.x + 0.5) - simulateX)
            simulateDistanceY = abs((node.y + 0.5) - simulateY)
            return (simulateDistanceX + simulateDistanceY) > (distanceX + distanceY)

    @staticmethod
    def GetDirectionVector(direction):
        if direction == AgentConsts.NO_MOVE:
            return 0.0, 0.0
        elif direction == AgentConsts.MOVE_UP:
            return 0.0, -1.0
        elif direction == AgentConsts.MOVE_DOWN:
            return 0.0, 1.0
        elif direction == AgentConsts.MOVE_RIGHT:
            return 1.0, 0.0
        else:
            return -1.0, 0.0

    def GetDirection(self, node, x, y):
        if ExecutePlan.MoveDown(node, x, y):
            return AgentConsts.MOVE_DOWN
        elif ExecutePlan.MoveUp(node, x, y):
            return AgentConsts.MOVE_UP
        elif ExecutePlan.MoveRight(node, x, y):
            return AgentConsts.MOVE_RIGHT
        elif ExecutePlan.MoveLeft(node, x, y):
            return AgentConsts.MOVE_LEFT
        else:
            return AgentConsts.NO_MOVE

    def ClearLineOfFire(self, x1, y1, x2, y2, agent):
        x1_map, y1_map = BCProblem.WorldToMapCoordFloat(x1, y1, agent.problem.ySize)
        x2_map, y2_map = BCProblem.WorldToMapCoordFloat(x2, y2, agent.problem.ySize)

        if abs(x1_map - x2_map) < 0.2:  # misma columna
            start = int(min(y1_map, y2_map)) + 1
            end = int(max(y1_map, y2_map))
            for y in range(start, end):
                cell = agent.problem.map[int(x1_map)][y]
                if cell != AgentConsts.NOTHING and cell != AgentConsts.BRICK:
                    return False
        elif abs(y1_map - y2_map) < 0.2:  # misma fila
            start = int(min(x1_map, x2_map)) + 1
            end = int(max(x1_map, x2_map))
            for x in range(start, end):
                cell = agent.problem.map[x][int(y1_map)]
                if cell != AgentConsts.NOTHING and cell != AgentConsts.BRICK:
                    return False
        else:
            return False  # no están alineados

        return True

    def BrickBlockingPath(self, x1, y1, x2, y2, map):
        x1_map, y1_map = int(x1), int(y1)
        x2_map, y2_map = int(x2), int(y2)

        if x1_map == x2_map:  # Mismo eje vertical
            step = 1 if y2_map > y1_map else -1
            for y in range(y1_map + step, y2_map, step):
                cell = map[x1_map][y]
                if cell == AgentConsts.UNBREAKABLE:
                    return False
                if cell == AgentConsts.BRICK:
                    return True
        elif y1_map == y2_map:  # Mismo eje horizontal
            step = 1 if x2_map > x1_map else -1
            for x in range(x1_map + step, x2_map, step):
                cell = map[x][y1_map]
                if cell == AgentConsts.UNBREAKABLE:
                    return False
                if cell == AgentConsts.BRICK:
                    return True
        return False
