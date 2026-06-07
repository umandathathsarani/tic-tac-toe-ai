import math

def minimax(state, player, alpha=-math.inf, beta=math.inf):
    max_player = 'O'
    other_player = 'O' if player == 'X' else 'X'

    if state.current_winner == other_player:
        return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}
    elif not state.empty_squares():
        return {'position': None, 'score': 0}

    if player == max_player:
        best = {'position': None, 'score': -math.inf}
    else:
        best = {'position': None, 'score': math.inf}

    for possible_move in state.available_moves():
        state.make_move(possible_move, player)
        sim_score = minimax(state, other_player, alpha, beta)
        
        state.board[possible_move] = ' '
        state.current_winner = None
        sim_score['position'] = possible_move

        if player == max_player:
            if sim_score['score'] > best['score']:
                best = sim_score
            alpha = max(alpha, best['score'])
        else:
            if sim_score['score'] < best['score']:
                best = sim_score
            beta = min(beta, best['score'])
            
        if beta <= alpha:
            break
            
    return best