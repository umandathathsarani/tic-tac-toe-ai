import random
from game import TicTacToe
from ai import minimax

def play(game, x_player, o_player, difficulty, print_game=True):
    if print_game:
        game.print_board_nums()

    letter = 'X'
    while game.empty_squares():
        if letter == 'O':
            if difficulty == 'easy':
                square = random.choice(game.available_moves())
            elif difficulty == 'medium':
                if random.random() < 0.5:
                    square = minimax(game, letter)['position']
                else:
                    square = random.choice(game.available_moves())
            else:
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
    
    print("Select Difficulty:")
    print("1. Easy (Random Moves)")
    print("2. Medium (50% Smart, 50% Random)")
    print("3. Hard (Unbeatable AI)")
    
    choice = ''
    while choice not in ['1', '2', '3']:
        choice = input("Enter 1, 2, or 3: ")
        
    diff_map = {'1': 'easy', '2': 'medium', '3': 'hard'}
    selected_difficulty = diff_map[choice]
    
    print(f"\nStarting game on {selected_difficulty.upper()} difficulty!")
    play(t, 'X', 'O', selected_difficulty, print_game=True)