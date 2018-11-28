# Joao Nogueira 83488; Joao Pina 85080;  Grupo 13

from search import *
from utils import *
import copy
import timeit
import math

# Color
# sem cor = 0
# com cor > 0

def get_no_color():
    return 0

def no_color (c):
    return c==0

def color (c):
    return c > 0

###################

# Pos
# Tuple (l, c)

def make_pos(l, c):
    return (l, c)

def pos_l(pos):
    return pos[0]

def pos_c(pos):
    return pos[1]

# Group
# [Pos1, Pos2, ...]

def make_group():
    return []

def add_pos(group, pos):
    group.append(pos)

def get_first_pos(group):
    return group[0]
########################

# Board
# Ex: [[1,2,2,3,3],[2,2,2,1,3],[1,2,2,2,2],[1,1,1,1,1]]

def get_linhas(board):
    return len(board)

def get_colunas(board):
    return len(board[0])

def get_value(board, linha, coluna):
    return board[linha][coluna]

def set_value(board, linha, coluna, value):
    board[linha][coluna] = value

#########################


def find_group(board, start, group):

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dir in directions:
        linha = pos_l(start) + dir[0]
        coluna = pos_c(start) + dir[1]

        # Searchs in every direction
        # Ignores positions already in group
        if ( 0 <= linha  < get_linhas(board) and 0 <= coluna < get_colunas(board) and get_value(board, linha, coluna) == get_value(board, pos_l(start), pos_c(start)) and make_pos(linha,coluna) not in group):
            pos = make_pos(linha, coluna)
            add_pos(group, pos)
            group = find_group(board, pos, group) # Searches from the new position added to the group

    return group



def board_find_groups(board):

    groups = []

    # Goes through every position on the board
    for linha in range(get_linhas(board)):

        for coluna in range(get_colunas(board)):

            # Ignores positions with no color
            if (no_color(get_value(board, linha, coluna))): continue

            found = False

            for group in groups:
                if make_pos(linha, coluna) in group:
                    found = True
                    break
            # Ignores positions already in a group
            if ( found ): continue

            # Creates a new group and adds current position
            pos = make_pos(linha, coluna)
            group = make_group()
            add_pos(group, pos)
            
            # Searches for the rest of the group elements and adds to the
            # final list of groups
            groups.append(find_group(board, pos, group))

    return groups




def board_remove_group(board, group):

    new_board = copy.deepcopy(board) # Copies the board

    # Replaces the values of the positions in the group with no_color (0)
    for pos in group:
        set_value(new_board, pos_l(pos), pos_c(pos), get_no_color())

    # Vertical 
    for linha in range(get_linhas(new_board)): #Starts in the first line

        for coluna in range(get_colunas(new_board)): # and goes through all collumns

            # If there is no color we shift all the positions above 1 line down
            if (no_color(get_value(new_board, linha, coluna))):
                for aux_l in range(linha - 1, -2, -1):
                    if ( aux_l >= 0 ):
                        set_value(new_board, aux_l + 1, coluna, get_value(new_board, aux_l, coluna))
                    else:
                        set_value(new_board, aux_l + 1, coluna, get_no_color())

    # The variable "linha" has the index for the last line in the board
    # Since we already did the vertical compression we just have to
    # check if each column in that line is empty
    # Horizontal
    for coluna in range(get_colunas(new_board) -1, -1, -1):
        empty = True
        if (color(get_value(new_board, linha, coluna))):
            empty = False

        # If the column is empty we shift every line 1 position to the left
        if (empty):
            for aux_c in range(coluna, get_colunas(new_board)):
                for aux_l in range(get_linhas(new_board)):
                    if (aux_c+1 < get_colunas(new_board)):
                        set_value(new_board, aux_l, aux_c, get_value(new_board, aux_l, aux_c + 1))
                    else:
                        set_value(new_board, aux_l, aux_c, get_no_color())

    return new_board


class sg_state:

    def __init__(self, board):
        self.board = board
        self.groups = make_group()

    """We count the number of positions with no color to order the states"""
    def __lt__(self, other):
        count_self = 0
        count_other = 0
        for linha in range(get_linhas(self.board)):
            for coluna in range(get_colunas(self.board)):
                if (no_color(get_value(self.board, linha, coluna))): count_self += 1
                if (no_color(get_value(other.board, linha, coluna))): count_other += 1

        return count_self < count_other



class same_game(Problem):
    def __init__(self, board):
        super(self.__class__, self).__init__(sg_state(board), [])

    """Return the actions that can be executed in the given state"""    
    def actions(self, state):
        if (not state.groups): state.groups = board_find_groups(state.board)
        groups = state.groups
        final = []
        # Filters the groups with only one position
        for group in groups:
            if (len(group) != 1):
                final.append(group)
        return final

    """Return the state that results from executing the given
    action in the given state"""
    def result(self, state, action):
        return sg_state(board_remove_group(state.board, action))

    """Return True if the state is a goal"""
    def goal_test(self, state):
        return board_find_groups(state.board) == self.goal

    """No need to redefine path_cost()"""
    #def path_cost(self, c, state1, action, state2):

    """Heuristic used is the number of groups"""
    def h(self, node):
        if (not node.state.groups): node.state.groups = board_find_groups(node.state.board)    
        return len(node.state.groups)


