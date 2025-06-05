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
    
    # utility function to evaluate board state
    def get_board(board, player):
        # Get own and opponent store
        player_store = board[6] if player == 1 else board[13]
        opponent_store = board[13] if player == 1 else board[6]

        # get pits for both players
        player_pits = board[0:6] if player == 1 else board[7:13]
        opponent_pits = board[7:13] if player == 1 else board[0:6]

        score = 0
        # main point diff counts most
        score += 3.5 * (player_store - opponent_store)

        # more stones on your side = benefit
        score += 0.5 * (sum(player_pits) - sum(opponent_pits))

        # bonus if a move gives us another turn
        for i in range(6):
            if player == 1 and board[i] == 6 - i:
                score += 2
            elif player == 2 and board[7 + i] == 6 - i:
                score += 2

        # reward possible captures
        for i in range(6):
            idx = i if player == 1 else 7 + i
            if board[idx] == 1:
                opp_idx = 12 - idx
                if board[opp_idx] > 0:
                    score += 2 * board[opp_idx]

        # punish opponent can make a big capture
        for i in range(6):
            if player == 1 and board[i] == 1 and board[12 - i] >= 3:
                score -= board[12 - i] * 0.7
            elif player == 2 and board[7 + i] == 1 and board[5 - i] >= 3:
                score -= board[5 - i] * 0.7

        # endgame bonus or penalty if the game is close to finishing
        if sum(board[0:6]) + sum(board[7:13]) <= 15:
            if player_store > opponent_store:
                score += 100
            elif player_store < opponent_store:
                score -= 100

        return score

    # Returns valid moves for current player
    def valid_moves(board, player):
        offset = 0 if player == 1 else 7
        return [i + 1 for i in range(6) if board[offset + i] > 0]

    # simulates a move and returns new board and whose turn it is
    def play(playerTurn, playerMove, boardGame):
        if not correctPlay(playerMove, boardGame, playerTurn):
            return None

        idx = playerMove - 1 + (playerTurn - 1) * 7
        numStones = boardGame[idx]
        boardGame[idx] = 0

        # distribute stones one-by-one
        while numStones > 0:
            idx = (idx + 1) % 14
            if idx == 13 - 7 * (playerTurn - 1):  # skip opponent's store
                continue
            boardGame[idx] += 1
            numStones -= 1

        # check if player gets another turn
        nextTurn = playerTurn if idx == 6 + 7 * (playerTurn - 1) else 3 - playerTurn

        # If last stone lands in empty pit on own side = capture
        if boardGame[idx] == 1 and idx in range((playerTurn - 1) * 7, 6 + (playerTurn - 1) * 7):
            boardGame[6 + (playerTurn - 1) * 7] += 1 + boardGame[12 - idx]
            boardGame[idx] = 0
            boardGame[12 - idx] = 0

        return boardGame, nextTurn

    # Minimax recursive function
    def minimax(board, player, depth, maxing):
        if depth == 0:
            return get_board(board, player), None

        current_player = player if maxing else 3 - player
        moves = valid_moves(board, current_player)
        best_value = float('-inf') if maxing else float('inf')
        best_move = None

        for move in moves:
            board_copy = board[:]
            result = play(current_player, move, board_copy.copy())
            if result is None:
                continue
            new_board, next_turn = result
            next_maxing = maxing if next_turn == current_player else not maxing

            value, _ = minimax(new_board, player, depth - 1, next_maxing)

            # Small penalty if opponent gets another turn
            if next_turn != current_player:
                value -= 3

            if maxing and value > best_value:
                best_value = value
                best_move = move
            elif not maxing and value < best_value:
                best_value = value
                best_move = move

        return best_value, best_move

    # Try to find the best move with minimax
    _, best_move = minimax(boardIn.copy(), playerTurnIn, 3, True)

    # If no move found, pick first valid move
    if best_move is None:
        valid = valid_moves(boardIn, playerTurnIn)
        best_move = valid[0] if valid else 1

    # Return move as a string and method used
    return str(best_move), "minimax"


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
