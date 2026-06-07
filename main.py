import tkinter as tk
from tkinter import messagebox
import random
from game import TicTacToe
from ai import minimax

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Tic-Tac-Toe")
        self.game = TicTacToe()
        self.difficulty = "hard"
        self.buttons = []
        self.setup_menu()

    def setup_menu(self):
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=20)
        
        tk.Label(self.menu_frame, text="Select Difficulty:", font=('Arial', 14)).pack(pady=5)
        
        tk.Button(self.menu_frame, text="Easy", font=('Arial', 12), width=10, command=lambda: self.start_game("easy")).pack(pady=5)
        tk.Button(self.menu_frame, text="Medium", font=('Arial', 12), width=10, command=lambda: self.start_game("medium")).pack(pady=5)
        tk.Button(self.menu_frame, text="Hard", font=('Arial', 12), width=10, command=lambda: self.start_game("hard")).pack(pady=5)

    def start_game(self, difficulty):
        self.difficulty = difficulty
        self.menu_frame.pack_forget()
        
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=10)
        
        for i in range(9):
            btn = tk.Button(self.board_frame, text=" ", font=('Arial', 24, 'bold'), width=5, height=2,
                            command=lambda s=i: self.player_move(s))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

    def player_move(self, square):
        if self.game.board[square] == ' ' and not self.game.current_winner:
            self.game.make_move(square, 'X')
            self.buttons[square].config(text='X')
            
            if self.check_game_over():
                return
                
            self.root.after(250, self.ai_move)

    def ai_move(self):
        if not self.game.empty_squares() or self.game.current_winner:
            return
            
        if self.difficulty == 'easy':
            square = random.choice(self.game.available_moves())
        elif self.difficulty == 'medium':
            if random.random() < 0.5:
                square = minimax(self.game, 'O')['position']
            else:
                square = random.choice(self.game.available_moves())
        else:
            square = minimax(self.game, 'O')['position']
            
        if square is not None:
            self.game.make_move(square, 'O')
            self.buttons[square].config(text='O')
            self.check_game_over()

    def check_game_over(self):
        if self.game.current_winner == 'X':
            messagebox.showinfo("Game Over", "You win!")
            self.reset_game()
            return True
        elif self.game.current_winner == 'O':
            messagebox.showinfo("Game Over", "AI wins!")
            self.reset_game()
            return True
        elif not self.game.empty_squares():
            messagebox.showinfo("Game Over", "It's a tie!")
            self.reset_game()
            return True
        return False

    def reset_game(self):
        self.game = TicTacToe()
        for btn in self.buttons:
            btn.config(text=" ")
        self.board_frame.pack_forget()
        self.buttons = []
        self.setup_menu()

if __name__ == '__main__':
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()