class TicTacToe:
    def __init__(self, grid_size=3, win_requirement=3, dead_squares=None):
        self.grid_size = grid_size
        self.win_requirement = win_requirement
        self.dead_squares = dead_squares if dead_squares else []
        self.board = ['#' if i in self.dead_squares else ' ' for i in range(self.grid_size * self.grid_size)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*self.grid_size:(i+1)*self.grid_size] for i in range(self.grid_size)]:
            print('| ' + ' | '.join(row) + ' |')

    def print_board_nums(self):
        number_board = [[str(i) for i in range(j*self.grid_size, (j+1)*self.grid_size)] for j in range(self.grid_size)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        r, c = square // self.grid_size, square % self.grid_size
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            count = 1
            
            for i in range(1, self.win_requirement):
                nr, nc = r + dr*i, c + dc*i
                if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size and self.board[nr * self.grid_size + nc] == letter:
                    count += 1
                else:
                    break
                    
            for i in range(1, self.win_requirement):
                nr, nc = r - dr*i, c - dc*i
                if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size and self.board[nr * self.grid_size + nc] == letter:
                    count += 1
                else:
                    break
                    
            if count >= self.win_requirement:
                return True
                
        return False