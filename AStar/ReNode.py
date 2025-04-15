from Node import Node

class ReNode(Node):
    def __init__(self, parent, g, state):
        super().__init__(parent, g)
        self.state = state  #Estado especifico del nodo

def Heuristic(self, node):
    #El coste es igual a la distancia al nodo
    x1, y1 = node.state
    x2, y2 = self.goal.state
    return abs(x1 - x2) + abs(y1 - y2)

def GetSucessors(self, node):
        x, y = node.state
        successors = []
        directions = [(-1,0), (1,0), (0,-1), (0,1)]  # arriba, abajo, izq, der

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.IsValid(nx, ny):
                successor = GridNode(state=(nx, ny), parent=node, g=node.G() + 1)
                successors.append(successor)

        return successors

def GetGCost(self, nodeTo):    
     return nodeTo.G()

def IsValid(self, x, y):
    return (0 <= x < len(self.grid) and
            0 <= y < len(self.grid[0]) and
            self.grid[x][y] == 0)  # 0 = celda libre