# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
import sys
from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foodDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        ghostDistances = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]

        currentPosition = currentGameState.getPacmanPosition()
        currentScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        if successorGameState.isWin():
            return 99999
        
        for ghost in newGhostStates:
            if ghost.getPosition() == currentPosition and ghost.scaredTimer == 0:
                return -99999
        
        if action == 'Stop':
            return -99999

        foodEaten = False
        
        if newScaredTimes[0] > currentScaredTimes[0]:
            foodEaten = True
        
        score = 0

        minimumFoodDistance = min(foodDistances)
        minimumGhostDistance = min(ghostDistances)

        score += 1.0/(1.0+minimumFoodDistance)

        if foodEaten:
            score+= 1.0/(1.0+minimumGhostDistance)
        else:
            score-= 1.0/(1.0+minimumGhostDistance)
        return successorGameState.getScore() + score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def maxValue(self, gameState, depth):
        currentDepth = depth+1
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        currMax = -sys.maxsize
        possibleActions = gameState.getLegalActions(0)
        for action in possibleActions:
            nextState = gameState.generateSuccessor(0,action)
            currMax = max(currMax, self.minValue(nextState, currentDepth, 1))
        
        return currMax
    
    def minValue(self, gameState, depth, ghostIndex):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        currMin = sys.maxsize
        possibleActions = gameState.getLegalActions(ghostIndex)
        for action in possibleActions:
            nextState = gameState.generateSuccessor(ghostIndex, action)
            if ghostIndex == (gameState.getNumAgents()-1):
                currMin = min(currMin, self.maxValue(nextState, depth))
            else:
                currMin = min(currMin, self.minValue(nextState, depth, ghostIndex+1))

        return currMin
    
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        possibleActions = gameState.getLegalActions(0)
        currScore = -sys.maxsize
        optimalAction = ''

        for action in possibleActions:
            nextState = gameState.generateSuccessor(0, action)
            score = self.minValue(nextState, 0 , 1)
            if score>currScore:
                optimalAction = action
                currScore = score

        return optimalAction
        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def maxValue(self, gameState, depth, alpha, beta):
        currentDepth = depth+1
        currAlpha = alpha
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        currMax = -sys.maxsize
        possibleActions = gameState.getLegalActions(0)
        for action in possibleActions:
            nextState = gameState.generateSuccessor(0,action)
            currMax = max(currMax, self.minValue(nextState, currentDepth, 1, currAlpha, beta))
            if currMax>beta:
                return currMax
            currAlpha = max(currAlpha, currMax)
        return currMax
    
    def minValue(self, gameState, depth, ghostIndex, alpha, beta):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        currMin = sys.maxsize
        currBeta = beta
        possibleActions = gameState.getLegalActions(ghostIndex)
        for action in possibleActions:
            nextState = gameState.generateSuccessor(ghostIndex, action)
            if ghostIndex == (gameState.getNumAgents()-1):
                currMin = min(currMin, self.maxValue(nextState, depth, alpha, currBeta))
                if currMin<alpha:
                    return currMin
                currBeta = min(currBeta, currMin)
            else:
                currMin = min(currMin, self.minValue(nextState, depth, ghostIndex+1, alpha, currBeta))
                if currMin < alpha:
                    return currMin
                currBeta = min(currBeta, currMin)

        return currMin

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        possibleActions = gameState.getLegalActions(0)
        currScore = -sys.maxsize
        alpha = -sys.maxsize + 1
        beta = sys.maxsize - 1
        optimalAction = ''

        for action in possibleActions:
            nextState = gameState.generateSuccessor(0, action)
            score = self.minValue(nextState, 0 , 1, alpha, beta)
            if score>currScore:
                optimalAction = action
                currScore = score
            if score > beta:
                return optimalAction
            alpha = max(alpha, score) 

        return optimalAction

        # util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectiValue(gameState,agentID,depth):
            possibleActions=gameState.getLegalActions(agentID)
            if len(possibleActions)==0:
                return (self.evaluationFunction(gameState),None)

            l=0
            Act=None
            for action in possibleActions:
                if(agentID==gameState.getNumAgents() -1):
                    sucsValue=maxValue(gameState.generateSuccessor(agentID,action),depth+1)
                else:
                    sucsValue=expectiValue(gameState.generateSuccessor(agentID,action),agentID+1,depth)
                sucsValue=sucsValue[0]
                prob=sucsValue/len(possibleActions)
                l+=prob
            return(l,Act)
        
        def maxValue(gameState,depth):
            possibleActions=gameState.getLegalActions(0)
            if len(possibleActions)==0 or gameState.isWin() or gameState.isLose() or depth==self.depth:   
                return (self.evaluationFunction(gameState),None)                                  

            w=-sys.maxsize - 1
            Act=None

            for action in possibleActions:
                sucsValue=expectiValue(gameState.generateSuccessor(0,action),1,depth)
                sucsValue=sucsValue[0]
                if(w<sucsValue):
                    w,Act=sucsValue,action                                                          
            return(w,Act)
        
        maxValue=maxValue(gameState,0)[1]
        return maxValue
        # util.raiseNotDefined()

