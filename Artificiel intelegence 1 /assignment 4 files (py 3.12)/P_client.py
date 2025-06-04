# client to Mancala server. Lab4, DVA340, MDU.
# For students: you only need to fill out function decide_move(boardIn, playerTurnIn)
# it currently selects a random available move.
# To test your client: start Mancala_server.pyc, then your program and one bot in that order (server first, then clients)

import socket
import numpy as np
import time
from multiprocessing.pool import ThreadPool
import os
from datetime import date


def decide_move(boardIn, playerTurnIn):
    #CHANGE THIS FILE TO CODE INTELLIGENCE IN YOUR CLIENT.
    # PLAYERMOVE IS '1'..'6'
    # BOARDIN CONSISTS OF 14 INTS. BOARDIN[0-5] ARE P1 HOLES, BOARDIN[6] IS P1 STORE
    # BOARDIN[7-12] ARE P2 HOLES, BOARDIN[13] IS P2 STORE
    def get_board(board, player):
        player_store = board[6] if player == 1 else board[13]  # players store index
        opp_store = board[13] if player == 1 else board[6]  # opponents store index
        player_pits = sum(board[0:6]) if player == 1 else sum(board[7:13])  # stones on players side
        opp_pits = sum(board[7:13]) if player == 1 else sum(board[0:6])  # stones on opponents side
        
        score = player_store - opp_store
        score += 0.2 * (player_pits - opp_pits) # weight calculated
        if playerTurnIn == 1: # bonus added 
            score += 0.1
        else:
            score -= 0.1
            
        if sum(board[0:6]) == 0 or sum(board[7:13]) == 0:
            score += (board[6] if player == 1 else board[13]) * 2
        
        for i in range(6):
            if player == 1 and board[i] == 6 - i:
                score += 10 # round to win the game 
            elif player == 2 and board[7 + i] == 6 - i:
                score += 10 # round to win the game
        for i in range(6):
            idx = i if player == 1 else 7 + i
            if board[idx] == 1:
                opp_idx = 12 - idx
                score += board[opp_idx] + 2
        
        # final utility
        return score
        
    def valid_moves(board, player):
        offset = 0 if player == 1 else 7  # player 1 pits: 0–5, Player 2 pits: 7–12
        return [i + 1 for i in range(6) if board[offset + i] > 0] 

    # minimax algorithm with depth-limited search to select the best move.
    # It alternates between maximizing and minimizing players.
    def minimax(board, player, depth, maxing):
        if depth == 0:
            return get_board(board, player), None  # evaluate board at leaf node

        current_player = player if maxing else 3 - player  # decide whose turn it is in the simulation

        # defensive check to abort if invalid state
        if current_player not in [1, 2] or len(board) != 14:
            return get_board(board, player), None

        possible_moves = valid_moves(board, current_player)  # get list of legal moves

        best_value = float('-inf') if maxing else float('inf')
        best_move = None

        for move in possible_moves:
            if not isinstance(move, int) or not (1 <= move <= 6):
                continue  # skip illegal or corrupt move values

            board_copy = board.copy()
            result = play(current_player, move, board_copy)  # simulate the move

            # skip move if simulation fails
            if result is None or not isinstance(result, tuple) or len(result) != 2:
                continue

            new_board, next_turn = result
            
            # ensure valid state after move
            if len(new_board) != 14 or next_turn not in [1, 2]:
                continue

            # determine if the same player continues
            next_maxing = maxing if next_turn == current_player else not maxing
            value, _ = minimax(new_board, depth - 1, player, next_maxing)
            
            # penalty bot for good set-up
            if next_turn != current_player:
                # Assume opponent will play perfectly
                if current_player == 1 and new_board[7:13].count(1) > 0:
                    value = value - 3 if value is not None else -3
                elif current_player == 2 and new_board[0:6].count(1) > 0:
                    value = value - 3 if value is not None else -3
            
            # update best value and best move based on maxing/minimizing
            if maxing and value > best_value:
                best_value = value
                best_move = move
            elif not maxing and value < best_value:
                best_value = value
                best_move = move
            elif maxing < best_value:
                best_value = value
                best_move = move
            elif not maxing > best_value:
                best_value = value
                best_move = move
            
        return best_value, best_move    
    # use Minimax to find the best move, searching 3 roots deep
    _, best_move = minimax(boardIn.copy(), playerTurnIn, 3, True)

    # fallback if no move found, should happen if pits are empty
    if best_move is None:
        moves = valid_moves(boardIn, playerTurnIn)
        best_move = moves[0] if moves else 1  # default first legal move

    return str(best_move), "minimax"
    """moves = [
        '1',
        '2',
        '3',
        '4',
        '5',
        '6']
    if playerTurnIn == 1:
        options = np.array(boardIn[0:6])
        options = np.where(options > 0)
        options = options[0]
        position = options[np.random.randint(len(options), size=1)]
        playerMove = moves[position[0]]
    elif playerTurnIn == 2:
        options = np.array(boardIn[7:13])
        options = np.where(options > 0)
        options = options[0]
        position = options[np.random.randint(len(options), size=1)]
        playerMove = moves[position[0]]
    return playerMove, "randommove"""



def play(playerTurn: int, playerMove: int, boardGame):  
    #playerTurn ar 1 eller 2
    #playerMove ar 1..6
    #boardGame ar en 1x14 vektor
    if not correctPlay(playerMove, boardGame, playerTurn):
        print("Illegal move! break")
        return
    
    # Determine starting index based on playerTurn and playerMove
    idx = playerMove -1 + (playerTurn-1)*7 #-1 for p1, +6 for p2
    # grab stones from hole
    numStones:int  = boardGame[idx]
    boardGame[idx] = 0
    hand:int = numStones
    while hand > 0:
        #idx next hole
        idx = (idx +1) % 14 
        # Skip opponent's store
        if idx == 13 - 7*(playerTurn-1): #13 for p1, 6 for p2
            continue
        # add stone in hole, 
        boardGame[idx] += 1
        hand -= 1
    
    # end in store? get another turn. otherwise other players turn
    nextTurn = 3 - playerTurn
    if idx == 6 + 7*(playerTurn-1):
        nextTurn = playerTurn
    
    #end on own empty hole? score stone and opposite hole
    if boardGame[idx] == 1 and idx in range((playerTurn-1)*7,6+(playerTurn-1)*7):
        boardGame[idx] -= 1 #score stone in last hole
        boardGame[6+(playerTurn-1)*7] += 1 #and remove it from the hole
        boardGame[6+(playerTurn-1)*7] += boardGame[12 - idx] #also score stones from opposite hole
        boardGame[12 - idx] = 0 #and remove them from the hole
    return (boardGame, nextTurn)


def correctPlay(playerMove:int, board, playerTurn):
    correct = 0
    if playerMove in range(1,7) and board[playerMove-1 + (playerTurn-1)*7] > 0:
        correct = 1
    return correct



def countScorePlayer1(boardGame):
    (p1s, p2s) = countPoints(boardGame)
    return int(p1s - p2s)
    


def countPoints(boardGame):
    return (boardGame[6], boardGame[13])



def receive(socket):
    msg = ''.encode()

    try:
        data = socket.recv(1024)
        msg += data
    except:
        pass

    return msg.decode()


def send(socket, msg):
    socket.sendall(msg.encode())

    

# LET THE MAIN BEGIN



startTime = date(2020, 11, 9)
playerName = 'Oscar_Gullberg'
host = '127.0.0.1'
port = 30000
s = socket.socket()
pool = ThreadPool(processes=1)
gameEnd = False
MAX_RESPONSE_TIME = 20
print('The player: ' + playerName + ' starts!')
s.connect((host, port))
print('The player: ' + playerName + ' connected!')
while not gameEnd:
    asyncRetult = pool.apply_async(receive, (s,))
    startTime = time.time()
    currentTime = 0
    received = 0
    data = []
    while received == 0 and currentTime < MAX_RESPONSE_TIME:
        time.sleep(0.01)
        if asyncRetult.ready():
            data = asyncRetult.get()
            received = 1
        currentTime = time.time() - startTime
    if received == 0:
        print('No response in ' + str(MAX_RESPONSE_TIME) + ' sec')
        gameEnd = 1
    if data == 'N':
        send(s, playerName)
    if data == 'E':
        gameEnd = 1
    if len(data) > 1:
        board = [            0,            0,            0,            0,            0,            0,            0,            0,            0,            0,            0,            0,            0,            0]
        playerTurn = int(data[0])
        i = 0
        j = 1
        while i <= 13:
            board[i] = int(data[j]) * 10 + int(data[j + 1])
            i += 1
            j += 2
        (move, botname) = decide_move(board, playerTurn)
    #    print('sending ', move)
        send(s, move)

        
#wait = input('Press ENTER to close the program.')
