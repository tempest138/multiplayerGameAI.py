import copy
# Symbols for P1 and P2
player, AI = 'x', 'o'

# Empty game board
board = [['-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-']]

# min and max alpha-beta values
MAX = 1000
MIN = -1000

# Main game function. Player can input 1 or 2 to be 'x' or 'o'. Input 'MM' to have AI player
# use Minimax algorithm or 'AB' to use Alpha-Beta pruning.
# Rules: input coordinates of which spot to black out. When a spot is selected all adjacent spots are blacked out as well.
# The player who can no longer make a move is the loser.
def game():
    player = 'x'
    AI = 'o'
    turn_order = []
    states = []
    i = 0
    human = True
    max_player = False
    print('Select player: ')
    x = int(input())
    print('Select search method: ')
    y = input()
    print('Select depth level')
    depth = input()


    get_board(board)
    states.append(board)
    current_state = states.pop()

    if y == 'AB':
        if x == 2:
            player = 'o'
            AI = 'x'
            turn_order.append(AI)
            human = False
            max_player = True
            move = alpha_move(current_state, max_player, depth)
            states.append(block(current_state, move[0], move[1], max_player))
            i += 1
            current_state = states.pop()
            print(move)
            get_board(current_state)

        while check_terminal(board) == False:
            turn_order.append(player)
            print(turn_order)
            print('Select row: ')
            r = int(input())
            print('Select column: ')
            c = int(input())
            states.append(block(current_state, r, c, human))
            current_state = states.pop()
            get_board(current_state)

            if check_terminal(current_state) == False:
                turn_order.append(AI)
                print(turn_order)
                move = alpha_move(current_state, max_player, depth)
                states.append(block(current_state, move[0], move[1], max_player))
                current_state = states.pop()
                print(move)
                get_board(current_state)
    elif y == 'MM':
        if x == 2:
            player = 'o'
            AI = 'x'
            turn_order.append(AI)
            human = False
            max_player = True
            move = make_move(current_state, max_player, depth)
            states.append(block(current_state, move[0], move[1], max_player))
            i += 1
            current_state = states.pop()
            print(move)
            get_board(current_state)

        while check_terminal(board) == False:
            turn_order.append(player)
            print(turn_order)
            print('Select row: ')
            r = int(input())
            print('Select column: ')
            c = int(input())
            states.append(block(current_state, r, c, human))
            current_state = states.pop()
            get_board(current_state)

            if check_terminal(current_state) == False:
                turn_order.append(AI)
                print(turn_order)
                move = make_move(board, max_player, depth)
                states.append(block(current_state, move[0], move[1], max_player))
                current_state = states.pop()
                print(move)
                get_board(current_state)
    else:
        print('invalid input')

    if turn_order[len(turn_order) - 1] == 'x':
        print('GAME OVER: PLAYER 1 WINS!!!')
    else:
        print('GAME OVER: PLAYER 2 WINS!!!')

# Prints current state of the board
def get_board(board):
    for i in range(len(board)):
        for j in range(len(board)):
            print(board[i][j], end=" ")
        print()
    print()

# Minimax algorithm
def minimax(board, depth, target_depth, max_player):
    tmp = copy.deepcopy(board)
    score = get_score(tmp, max_player)
    node_count = 0
    if score == 10:
        return 10
    if score == -10:
        return -10

    if depth == target_depth:
        return get_score(tmp, max_player)

    if (max_player):
        best_score = -1000

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == '-':
                    block(tmp, i, j, max_player)
                    best_score = max(best_score, minimax(tmp, depth + 1, target_depth, max_player))
                    node_count += 1
                    # unblock(tmp, i, j)
        return best_score
    else:
        best_score = 1000
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == '-':
                    block(tmp, i, j, max_player)
                    best_score = min(best_score, minimax(tmp, depth + 1, target_depth, max_player))
                    node_count += 1
                    # unblock(tmp, i, j)
        return best_score

# Alpha-Beta Pruning algorithm
def alpha_beta(board, depth, target_depth, max_player, alpha, beta):
    tmp = copy.deepcopy(board)
    score = get_score(tmp, max_player)
    node_count = 0
    if score == 10:
        return 10
    if score == -10:
        return -10

    if depth == target_depth:
        return get_score(tmp, max_player)

    if (max_player):
        best_score = MIN

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == '-':
                    block(tmp, i, j, max_player)
                    best_score = max(best_score, minimax(tmp, depth + 1, target_depth, max_player))
                    node_count += 1
                    alpha = max(alpha,  best_score)

                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = MAX
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == '-':
                    block(tmp, i, j, max_player)
                    best_score = min(best_score, minimax(tmp, depth + 1, target_depth, max_player))
                    node_count += 1
                    beta = min(beta, best_score)

                    if beta <= alpha:
                        break
        return best_score

# Individual move for AI player (Minimax)
def make_move(board, max_player, depth):
    tmp = copy.deepcopy(board)
    node_count = 0
    if max_player:
        best_value = -100
        best_move = (-1, -1)

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == '-':
                    block(tmp, i, j, True)
                    move_value = minimax(tmp, 0, depth, True)
                    node_count += 1
                    if move_value > best_value:
                        best_move = (i, j)
                        best_value = move_value
        return best_move
    else:
        best_value = 100
        best_move = (-1, -1)

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == '-':
                    block(tmp, i, j, False)
                    move_value = minimax(tmp, 0, depth, False)
                    node_count += 1
                    if move_value < best_value:
                        best_move = (i, j)
                        best_value = move_value
        return best_move

# Individual move for AI (Alpha-Beta)
def alpha_move(board, max_player, depth):
    tmp = copy.deepcopy(board)
    node_count = 0
    if max_player:
        best_value = -100
        best_move = (-1, -1)

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == '-':
                    block(tmp, i, j, True)
                    move_value = alpha_beta(tmp, 0, depth, True, MIN, MAX)
                    node_count += 1
                    unblock(tmp, i, j)
                    if move_value > best_value:
                        best_move = (i, j)
                        best_value = move_value
        return best_move
    else:
        best_value = 100
        best_move = (-1, -1)

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == '-':
                    block(tmp, i, j, False)
                    move_value = alpha_beta(tmp, 0, depth, False, MIN, MAX)
                    node_count += 1
                    unblock(tmp, i, j)
                    if move_value < best_value:
                        best_move = (i, j)
                        best_value = move_value
        return best_move

# Checks if the board is in terminal state for AI player to move or game is finished
def check_terminal(state):
    for i in range(len(state)):
        for j in range(len(state)):
            if state[i][j] == '-':
                return False
    return True

# Returns score for AI player move path
def get_score(board, max_player):
    if check_terminal(board) == True:
        if max_player == False:
            return 10
        else: return -10
    else:
        return 0

# Function for blocking space on board
def block(state, r,  c, max_player):
    if max_player == True:
        state[r][c] = player
    else:
        state[r][c] = AI

    for i in range(len(state)):
        if i == r - 1 or i == r or i == r + 1:
            for j in range(len(state)):
                if (j == c - 1 or j == c or j == c + 1) and state[i][j] == '-':
                    state[i][j] = '/'
    return state

# Function to reverse move so AI player can test other paths
def unblock(state, r,  c):
    for i in range(len(state)):
        if i == r - 1 or i == r or i == r + 1:
            for j in range(len(state)):
                if j == c - 1 or j == c or j == c + 1:
                    state[i][j] = '-'
    return state


game()