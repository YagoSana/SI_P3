from Problem import Problem

class ReProblem(Problem):
    def __init__(self, initial, goal):
        super().__init__(initial, goal)
        self.grid = grid 

    def Initial():
        return self.initial
    
    #Calcula la heuristica del nodo en base al problema planteado (Se necesita reimplementar)
    def Heuristic(self, node):
        raise NotImplementedError("Heuristic no implementado")
        return 0.0

    #Genera la lista de sucesores del nodo (Se necesita reimplementar)
    def GetSucessors(self, node):
        raise NotImplementedError("GetSucessors no implementado")
        return []

    #Calcula el coste de ir del nodo from al nodo to (Se necesita reimplementar)
    
    def GetGCost(self, nodeTo):
        raise NotImplementedError("GetGCost no implementado")
        return 0.0
    
    def SetGoal(self, goal):
        self.goal = goal

    def SetInitial(self, initial):
        self.initial = initial

    def GetGoal(self):
        return self.goal



