from game import TicTacToe
from ai import minimax

def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    letter = 'X'
    while game.empty_squares():
        if letter == 'O':
            square = minimax(game, letter)['position']
        else:
            valid_square = False
            while not valid_square:
                square = input(f"{letter}'s turn. Input move (0-8): ")
                try:
                    val = int(square)
                    if val not in game.available_moves():
                        raise ValueError
                    valid_square = True
                    square = val
                except ValueError:
                    print("Invalid square. Try again.")

        if game.make_move(square, letter):
            if print_game:
                print(f"{letter} makes a move to square {square}")
                game.print_board()
                print('')

            if game.current_winner:
                if print_game:
                    print(f"{letter} wins!")
                return letter
            
            letter = 'O' if letter == 'X' else 'X'

    if print_game:
        print("It's a tie!")

if __name__ == '__main__':
    t = TicTacToe()
    play(t, 'X', 'O', print_game=True)