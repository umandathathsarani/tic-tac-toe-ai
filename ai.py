import math

def get_adjacent_moves(state):
    moves = set()
    occupied = [i for i, spot in enumerate(state.board) if spot == 'X' or spot == 'O']
    
    if not occupied:
        center = (state.grid_size * state.grid_size) // 2
        if state.board[center] == ' ':
            return [center]
        return state.available_moves()

    for square in occupied:
        r, c = square // state.grid_size, square % state.grid_size
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < state.grid_size and 0 <= nc < state.grid_size:
                    idx = nr * state.grid_size + nc
                    if state.board[idx] == ' ':
                        moves.add(idx)
    return list(moves)

def minimax(state, player, depth, alpha=-math.inf, beta=math.inf):
    max_player = 'O'
    other_player = 'O' if player == 'X' else 'X'

    if state.current_winner == other_player:
        score = 1000 + depth
        return {'position': None, 'score': score if other_player == max_player else -score}
    elif not state.empty_squares():
        return {'position': None, 'score': 0}

    if depth == 0:
        return {'position': None, 'score': 0}

    if player == max_player:
        best = {'position': None, 'score': -math.inf}
    else:
        best = {'position': None, 'score': math.inf}

    moves_to_check = get_adjacent_moves(state)

    for possible_move in moves_to_check:
        state.make_move(possible_move, player)
        sim_score = minimax(state, other_player, depth - 1, alpha, beta)
        
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