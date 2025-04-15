class AStar:
    def __init__(self, problem):
        self.open = []               # frontera (lista de nodos por explorar)
        self.processed = set()       # conjunto de nodos explorados (por coordenadas)
        self.problem = problem       # instancia del problema (que sabe cómo expandir, calcular H, etc.)

    def GetPlan(self):
        self.open.clear()
        self.processed.clear()
        path = []

        # Nodo inicial
        start_node = self.problem.Initial()
        self._ConfigureNode(start_node, None, 0)
        self.open.append(start_node)

        while self.open:
            # Ordenar por F (g + h)
            self.open.sort(key=lambda n: n.F())
            current = self.open.pop(0)

            if self.problem.IsASolution(current):
                return self.ReconstructPath(current)

            # Marcamos la posición como procesada
            self.processed.add((current.x, current.y))

            successors = self.problem.GetSucessors(current)

            if not successors:
                return []  # No hay solución

            for successor in successors:
                if (successor.x, successor.y) in self.processed:
                    continue

                newG = current.G() + self.problem.GetGCost(successor)
                old = self.GetSucesorInOpen(successor)

                if old is None:
                    # Nuevo nodo → configurar y agregar
                    self._ConfigureNode(successor, current, newG)
                    self.open.append(successor)
                else:
                    # Nodo ya estaba en open → mejorar si es posible
                    if newG < old.G():
                        self._ConfigureNode(old, current, newG)

        return []  # No se encontró solución

    def _ConfigureNode(self, node, parent, newG):
        node.SetParent(parent)
        node.SetG(newG)
        node.SetH(self.problem.Heuristic(node))  # importante: actualizar la heurística

    def GetSucesorInOpen(self, sucesor):
        for node in self.open:
            if node.IsEqual(sucesor):
                return node
        return None

    def ReconstructPath(self, goal):
        path = []
        aux = goal
        while aux is not None:
            path.append(aux)
            aux = aux.GetParent()
        return path[::-1]
