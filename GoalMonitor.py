import random
from States.AgentConsts import AgentConsts
class GoalMonitor:

    GOAL_COMMAND_CENTER = 0
    GOAL_LIFE = 1
    GOAL_PLAYER = 2
    GOAL_NPC=3 #MATAR AL OTRO AGENTE PORQUE ME MOLESTA MUCHISIMO
    GOAL_COVER=4 #BUSCAR COVERTURA PARA QUE NO ME MATEN Y TAL
 

    def __init__(self, problem, goals):
        self.goals = goals
        self.problem = problem
        self.lastTime = -1
        self.recalculate = False
        self.ticks=0
    def ForceToRecalculate(self):
        self.recalculate = True

    #determina si necesitamos replanificar
    def NeedReplaning(self, perception, map, agent):
        self.ticks+=1
        #Se ha detectado una bala y por lo tanto debemos actuar en consecuencia
        if perception[AgentConsts.NEIGHBORHOOD_RIGHT]==AgentConsts.SHELL or perception[AgentConsts.NEIGHBORHOOD_LEFT]==AgentConsts.SHELL or perception[AgentConsts.NEIGHBORHOOD_UP]==AgentConsts.SHELL or perception[AgentConsts.NEIGHBORHOOD_DOWN]==AgentConsts.SHELL:
            return True
        elif perception[AgentConsts.HEALTH]<2: #Vida 
            return self.goals[self.GOAL_LIFE]
        elif abs(perception[AgentConsts.PLAYER_X]-perception[AgentConsts.AGENT_X])<6 and abs(perception[AgentConsts.PLAYER_Y]-perception[AgentConsts.AGENT_Y])<6:
            return True
        if(self.ticks>20): 
            print("Replanificacion por ticks")
            self.ticks=0
            return True
        return False
    
    #selecciona la meta mas adecuada al estado actual
    def SelectGoal(self, perception, map, agent):
        if (perception[AgentConsts.NEIGHBORHOOD_RIGHT]==AgentConsts.SHELL or perception[AgentConsts.NEIGHBORHOOD_LEFT]==AgentConsts.SHELL or perception[AgentConsts.NEIGHBORHOOD_UP]==AgentConsts.SHELL or perception[AgentConsts.NEIGHBORHOOD_DOWN]==AgentConsts.SHELL) and perception[AgentConsts.CAN_FIRE]==AgentConsts.SHELL:
            return self.goals[GOAL_PLAYER]

        if abs(perception[AgentConsts.PLAYER_X]-perception[AgentConsts.AGENT_X])<6 and abs(perception[AgentConsts.PLAYER_Y]-perception[AgentConsts.AGENT_Y])<6:
            return self.goals[self.GOAL_PLAYER]

        elif perception[AgentConsts.HEALTH]<2: #Vida 
            return self.goals[self.GOAL_LIFE]
            
        else:
            return self.goals[self.GOAL_COMMAND_CENTER]

    def UpdateGoals(self,goal, goalId):
        self.goals[goalId] = goal
