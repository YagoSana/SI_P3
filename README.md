# SI_P3
---
## Enunciado
### AStar.py:
    def GetPlan(self):
        findGoal = False
        #TODO implementar el algoritmo A*
        #cosas a tener en cuenta:
        #Si el número de sucesores es 0 es que el algoritmo no ha encontrado una solución, d
        #Hay que invertir el path para darlo en el orden correcto al devolverlo (path[::-1])
        #GetSucesorInOpen(sucesor) nos devolverá None si no lo encuentra, si lo encuentra
        #es que ese sucesor ya está en la frontera de exploración, DEBEMOS MIRAR SI EL NUEVO
        #SI esto es asi, hay que cambiarle el padre y setearle el nuevo coste.
        self.open.clear()
        self.precessed.clear()
        self.open.append(self.problem.Initial())
        path = []
        #mientras no encontremos la meta y haya elementos en open....
        #TODO implementar el bucle de búsqueda del algoritmo A*
        return path
    
    #nos permite configurar un nodo (node) con el padre y la nueva G
    def _ConfigureNode(self, node, parent, newG):
        node.SetParent(parent)
        node.SetG(newG)
        #TODO Setearle la heuristica que está implementada en el problema. (si ya la tenía)

    #reconstruye el path desde la meta encontrada.
    def ReconstructPath(self, goal):
        path = []
        #TODO: devuelve el path invertido desde la meta hasta que el padre sea None.
        return path

### BCNode.py:
    ## DONE
    def IsEqual(self,node):
        #TODO: dos nodos son iguales cuando sus coordenadas x e y son iguales.
        return False

### BCProblem.py:
    ##DONE
    #Calcula la heuristica del nodo en base al problema planteado (Se necesita reimplementar
    def Heuristic(self, node):
        #TODO: heurística del nodo
        print("Aqui falta ncosas por hacer :) ")
        return 0
    
    ##DONE
    #Genera la lista de sucesores del nodo (Se necesita reimplementar)
    def GetSucessors(self, node):
        successors = []
        #TODO: sucesores de un nodo dado
        print("Aqui falta ncosas por hacer :) ")
        return successors

    ##DONE    
    #se utiliza para calcular el coste de cada elemento del mapa
    @staticmethod
    def GetCost(value):
        #TODO: debes darle un coste a cada tipo de casilla del mapa.
        return sys.maxsize

### GoalMonitor.py:
    #determina si necesitamos replanificar
    def NeedReplaning(self, perception, map, agent):
        if self.recalculate:
        self.lastTime = perception[AgentConsts.TIME]
        return True
        #TODO definir la estrategia de cuando queremos recalcular
        #puede ser , por ejemplo cada cierto tiempo o cuanod tenemos poca vida.
        return False
        
    #selecciona la meta mas adecuada al estado actual
    def SelectGoal(self, perception, map, agent):
        #TODO definir la estrategia del cambio de meta
        print("TODO aqui faltan cosas :)")
        return self.goals[random.randint(0,len(self.goals))]

### GoalOrientedAgent.py:
    #método interno que encapsula la creació nde un plan
    def _CreatePlan(self,perception,map):
        #currentGoal = self.problem.GetGoal()
        if self.goalMonitor != None:
        #TODO creamos un plan, pasos:
        #-con gualMonito, seleccionamos la meta actual (Que será la mas propicia => defi
        #-le damos el modo inicial _CreateInitialNode
        #-establecer la meta actual al problema para que A* sepa cual es.
        #-Calcular el plan usando A*
        print("TODO aqui faltan cosas :)")
        return self.aStar.GetPlan()
        
    #no podemos iniciarlo en el start porque no conocemos el mapa ni las posiciones de los o
    def InitAgent(self,perception,map):
        #creamos el problema
        #TODO inicializamos:
        # - creamos el problema con BCProblem
        # - inicializamos el mapa problem.InitMap
        # - inicializamos A*
        # - creamos un plan inicial
        print("TODO aqui faltan cosas :)")
        goal1CommanCenter = None
        goal2Life = self._CreateLifeGoal(perception)
        goal3Player = self._CreatePlayerGoal(perception)
        self.goalMonitor = GoalMonitor(self.problem,[goal1CommanCenter,goal2Life,goal3Player
