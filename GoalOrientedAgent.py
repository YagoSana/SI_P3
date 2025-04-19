from BaseAgent import BaseAgent
from StateMachine.StateMachine import StateMachine
from States.ExecutePlan import ExecutePlan
from GoalMonitor import GoalMonitor
from AStar.AStar import AStar
from MyProblem.BCNode import BCNode
from MyProblem.BCProblem import BCProblem
from States.AgentConsts import AgentConsts
from States.Attack import Attack
from States.AttackShell import AttackShell
from States.RandomMovement import RandomMovement
from States.Defending import Defending


#implementación de un agente básico basado en objetivos.
#disponemos de la clase GoalMonitor que nos monitorea y replanifica cada cierto tiempo
#o cuando se establezca una serie de condiciones.
class GoalOrientedAgent(BaseAgent):
    def __init__(self, id, name):
        super().__init__(id, name)
        dictionary = {
        "ExecutePlan" : ExecutePlan("ExecutePlan"),
        "Attack" : Attack("Attack"),
        "AttackShell" : AttackShell("AttackShell"),
        "RandomMovement" : RandomMovement("RandomMovement"),
        "Defending": Defending("Defending")
        }
        self.stateMachine = StateMachine("GoalOrientedBehavior",dictionary,"ExecutePlan")
        self.problem = None
        self.aStar = None
        self.plan = None
        self.goalMonitor = None
        self.agentInit = False
        self.XPos=0
        self.YPos=0

    #Metodo que se llama al iniciar el agente. No devuelve nada y sirve para contruir el agente
    def Start(self):
        print("Inicio del agente ")
        self.stateMachine.Start(self)
        self.problem = None
        self.aStar = None
        self.plan = None
        self.goalMonitor = None
        self.agentInit = False

    #Metodo que se llama en cada actualización del agente, y se proporciona le vector de percepciones
    #Devuelve la acción u el disparo si o no
    def Update(self, perception, map):
        if perception == True or perception == False:
            return 0,True
        #inicializamos el agente (no lo podemos hacer en el start porque no tenemos el mapa)
        if not self.agentInit:
            self.InitAgent(perception,map)
            self.agentInit = True
 
        #le damos update a la máquina de estados.
        action, shot = self.stateMachine.Update(perception, map, self)

        #Actualizamos el plan refrescando la posición del player (meta 2)
        goal3Player = self._CreatePlayerGoal(perception)
        self.goalMonitor.UpdateGoals(goal3Player,2)
        if self.goalMonitor.NeedReplaning(perception,map,self):
            self.problem.InitMap(map) ## refrescamos el mapa
            self.plan=self._CreatePlan(perception, map)
        return action, shot
    
    #método interno que encapsula la creación de un plan
    def _CreatePlan(self, perception, map):
        # Se obtiene la meta actual
        currentGoal = self.problem.GetGoal()

        # Solo volvemos a calcular el plan si la meta o el mapa han cambiado
        if self.goalMonitor != None:
            # Verificamos si necesitamos seleccionar un nuevo objetivo
            newGoal = self.goalMonitor.SelectGoal(perception, map, self)
            
            # Si el objetivo ha cambiado, actualizamos la meta
            if newGoal != currentGoal:
                print(f"Meta cambiada de {currentGoal} a {newGoal}")
                self.problem.SetGoal(newGoal)  # Establecemos el nuevo objetivo
                self.problem.InitMap(map)  # Refrescamos el mapa
                
                # Creamos el nuevo nodo inicial basado en la percepción actual
                node = self._CreateInitialNode(perception)
                self.problem.initial = node  # Actualizamos la información del nodo inicial

                # Recalculamos el plan utilizando A* con el nuevo objetivo y nodo inicial
                self.aStar = AStar(self.problem)
                self.plan = self.aStar.GetPlan()
            else:
                # Si no hay cambios, mantenemos el plan actual
                print(f"Manteniendo el plan actual con la meta {currentGoal}")
        else:
            # Si no tenemos un GoalMonitor, simplemente mantenemos el plan actual
            print(f"Sin GoalMonitor, manteniendo el plan actual con la meta {currentGoal}")

        return self.plan

        
    @staticmethod
    def CreateNodeByPerception(perception, value, perceptionID_X, perceptionID_Y,ySize):
      
        xMap, yMap = BCProblem.WorldToMapCoord(perception[perceptionID_X],perception[perceptionID_Y],ySize)
        newNode = BCNode(None,BCProblem.GetCost(value),value,xMap,yMap)
        return newNode

    def _CreatePlayerGoal(self, perception):
        return GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.PLAYER,AgentConsts.PLAYER_X,AgentConsts.PLAYER_Y,15)

    
    def _CreateLifeGoal(self, perception):
        return GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.LIFE,AgentConsts.LIFE_X,AgentConsts.LIFE_Y,15)
    
    def _CreateInitialNode(self, perception):
        node = GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.NOTHING,AgentConsts.AGENT_X,AgentConsts.AGENT_Y,15)
        node.SetG(0)
        return node
    
    def _CreateDefaultGoal(self, perception):
        return GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.COMMAND_CENTER,AgentConsts.COMMAND_CENTER_X,AgentConsts.COMMAND_CENTER_Y,15)
    
    #no podemos iniciarlo en el start porque no conocemos el mapa ni las posiciones de los objetos
    def InitAgent(self,perception,map):

        #TODO: DONE
   
        goal1CommanCenter = self._CreateDefaultGoal(perception) #De primeras va a por el command center
        goal2Life = self._CreateLifeGoal(perception) # va a por la vida
        goal3Player = self._CreatePlayerGoal(perception) # Va a por el jugador
        self.goalMonitor = GoalMonitor(self.problem,[goal1CommanCenter,goal2Life,goal3Player])

        #Creamos el problema
        xSize= 15 #tam del mapa
        ySize= 15
        self.problem= BCProblem(self._CreateInitialNode(perception), self.GetPlan(), 15, 15)
        
        #Inicializamos el mapa
        self.problem.InitMap(map)

        #Inicializamos A*
        self.aStar= AStar(self.problem)
        
        #Creamos un plan inicial
        self.plan= self._CreatePlan(perception, map)

    #muestra un plan por consola
    @staticmethod
    def ShowPlan(plan):
        for n in plan:
            print("X: ",n.x,"Y:",n.y,"[",n.value,"]{",n.G(),"} => ")

    def GetPlan(self):
        return self.plan
    
    #Metodo que se llama al finalizar el agente, se pasa el estado de terminacion
    def End(self, win):
        super().End(win)
        self.stateMachine.End()