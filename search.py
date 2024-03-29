# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import random

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

#===========================================================================
# Heuristicas para Busca A*
#===========================================================================

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

#***********************************************************************
# Heuristica Nao Admissivel (nao deve ser utilizada)
#   A heuristica abaixo foi implementada para verificarmos problemas
#   causados pela nao admissibilidade.
#***********************************************************************

def nao_admissivel(state, problem=None):
	return 10*max([abs(state[0]-problem.goal[0]), abs(state[1] - problem.goal[1])])

#***********************************************************************
# Heuristicas Admissiveis
#   As heuristicas abaixo foram comparadas em busca da melhor solucao
#   nos mapas bigMaze, mediumMaze e smallMaze
#
#   Apesar do desempenho marginalmente melhor de convex_euc_man,
#   consideramos a heuristica manhattan como a melhor opcao, pois, com
#   base na teoria de A* e na estrutura do pacman, espera-se que essa
#   heuristica tenha generalizacao melhor do que convex_euc_man
#***********************************************************************    

# Primeira Opcao (por generalizacao e perfomance)
def manhattan(state, problem=None): 
    # Distancia Manhatan, retorna |dx| + |dy|
	return abs(state[0]-problem.goal[0])+abs(state[1] - problem.goal[1])

def euclidean(state, problem=None):
    # Distancia Euclidiana
    X = (state[0] - problem.goal[0])**2
    Y = (state[1] - problem.goal[1])**2
    return (X + Y)**0.5

def min_manhattan(state, problem=None): 
    # Retorna o componente minimo da Distancia Manhatan
	return min([abs(state[0]-problem.goal[0]), abs(state[1] - problem.goal[1])])

def max_manhattan(state, problem=None):
    # Retorna o componente maximo da Distancia Manhatan
	return max([abs(state[0]-problem.goal[0]), abs(state[1] - problem.goal[1])])

# Segunda Opcao (por perfomance marginalmente superior em um labirinto)
def convex_euc_man(state, problem=None):
    # Retorna uma combinacao convexa entre as distancias euclidiana e manhattan
    # Requer importacao do modulo math
    X = (state[0] - problem.goal[0])**2
    Y = (state[1] - problem.goal[1])**2
    E = (X+Y)**0.5
    M = abs(state[0] - problem.goal[0]) + abs(state[1] - problem.goal[1])
    return M*0.8 + E*0.2

#===========================================================================
# Implementacao da Busca A*
#===========================================================================

def aStarSearch(problem, heuristic=nullHeuristic):
    #Neste codigo, utilizamos fila de prioridade, que e o padrao no A*

    visitados = [] #Armazena (Estado,Custo)
    EstadoInicial = problem.getStartState() #Armazena o Estado Inicial
    NoInicial = (EstadoInicial, [], 0) #(Estado,Acao, Custo) de A*
    fronteira = util.PriorityQueue() #Fila de prioridade oficial da implementacao de UC Berkeley
    fronteira.push(NoInicial, 0)
    
    while not fronteira.isEmpty():
        #Armazena o estado atual as acoes e custo atual para o proximo no.
        EstadoAtual, acoes, CustoAtual = fronteira.pop()
        NoAtual = (EstadoAtual, CustoAtual)
        visitados.append((EstadoAtual, CustoAtual))

        #Se encontrou objetivo retorna lista de acoes
        if problem.isGoalState(EstadoAtual):
            return acoes
        
        #Lista de filhos na forma (filho, acaoFilho, CustoAcao)
        filhos = problem.getSuccessors(EstadoAtual)
        
        #Para cada filho
        for filhosEstado, filhosAcoes, filhosCustos in filhos:
        	#Atualiza Custo e acao
            NovaAcao = acoes + [filhosAcoes]
            NovoCusto = problem.getCostOfActions(NovaAcao)
            NovoNo = (filhosEstado, NovaAcao, NovoCusto)
            visitado = False #label de visitado
            for explorado in visitados:
                #Armazena estado visitado e custo visitado
                EstadoVisitado, CustoVisitado = explorado

                #verifica se ja foi visitado e se o custo dele e maior que o existente.
                if (filhosEstado == EstadoVisitado) and (NovoCusto >= CustoVisitado):
                	visitado = True

            #Coloca NA fronteira caso nao tenha sido visitado ainda.
            if not visitado:
            	#Coloca na fronteira com o  custo dos nos carregados + heuristica
                fronteira.push(NovoNo, NovoCusto + heuristic(filhosEstado, problem))
                visitados.append((filhosEstado, NovoCusto))
    return 0

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
