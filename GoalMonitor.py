import random
from States.AgentConsts import *
class GoalMonitor:

    GOAL_COMMAND_CENTER = 0
    GOAL_LIFE = 1
    GOAL_PLAYER = 2
 

    def __init__(self, problem, goals):
        self.goals = goals
        self.problem = problem
        self.lastTime = -1
        self.recalculate = False

    def ForceToRecalculate(self):
        self.recalculate = True

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
        print("TODO aqui faltan cosas :)")
        if abs(perception[AgentConsts.PLAYER_X]-perception[AgentConsts.AGENT_X])<6 and abs(perception[AgentConst.PLAYER_Y]-perception[AgentConsts.AGENT_Y])<6:
            return self.goals[self.GOAL_PLAYER]
        elif perception[AgentConsts.HEALTH]<2: #Vida 
            return self.goals[self.GOAL_LIFE]
        else:
            return self.goals[self.GOAL_COMMAND_CENTER]

    def UpdateGoals(self,goal, goalId):
        self.goals[goalId] = goal
