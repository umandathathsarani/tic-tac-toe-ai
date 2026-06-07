import tkinter as tk
from tkinter import messagebox
import json
import os
from game import TicTacToe
from ai import minimax

LEVELS = {
    1: {"grid_size": 3, "win_req": 3, "dead": []},
    2: {"grid_size": 4, "win_req": 3, "dead": [0, 3, 12, 15]},
    3: {"grid_size": 4, "win_req": 4, "dead": []},
    4: {"grid_size": 5, "win_req": 4, "dead": [12]},
    5: {"grid_size": 5, "win_req": 4, "dead": [0, 4, 20, 24]}
}

SAVE_FILE = "save_data.json"

class CampaignGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe: Campaign Mode")
        self.current_level = self.load_progress()
        self.game = None
        self.buttons = []
        self.setup_menu()

    def load_progress(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                return data.get("level", 1)
        return 1

    def save_progress(self, level):
        with open(SAVE_FILE, "w") as f:
            json.dump({"level": level}, f)

    def setup_menu(self):
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=20, padx=50)
        
        if self.current_level > max(LEVELS.keys()):
            tk.Label(self.menu_frame, text="You beat the game!", font=('Arial', 18, 'bold')).pack(pady=10)
            tk.Button(self.menu_frame, text="Reset Progress", font=('Arial', 12), command=self.reset_campaign).pack(pady=5)
            return

        tk.Label(self.menu_frame, text=f"Level {self.current_level}", font=('Arial', 18, 'bold')).pack(pady=10)
        
        level_data = LEVELS[self.current_level]
        desc = f"Grid: {level_data['grid_size']}x{level_data['grid_size']}\nWin: {level_data['win_req']} in a row"
        tk.Label(self.menu_frame, text=desc, font=('Arial', 12)).pack(pady=5)
        
        tk.Button(self.menu_frame, text="Play Level", font=('Arial', 14), bg="green", fg="white", command=self.start_level).pack(pady=15)

    def reset_campaign(self):
        self.current_level = 1
        self.save_progress(1)
        self.menu_frame.pack_forget()
        self.setup_menu()

    def start_level(self):
        self.menu_frame.pack_forget()
        
        level_data = LEVELS[self.current_level]
        self.game = TicTacToe(grid_size=level_data['grid_size'], 
                              win_requirement=level_data['win_req'], 
                              dead_squares=level_data['dead'])
                              
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=10, padx=10)
        
        self.buttons = []
        for i in range(level_data['grid_size'] * level_data['grid_size']):
            btn = tk.Button(self.board_frame, text=" ", font=('Arial', 18, 'bold'), width=4, height=2,
                            command=lambda s=i: self.player_move(s))
            
            if i in level_data['dead']:
                btn.config(state="disabled", bg="black")
                
            btn.grid(row=i // level_data['grid_size'], column=i % level_data['grid_size'], padx=2, pady=2)
            self.buttons.append(btn)

    def player_move(self, square):
        if self.game.board[square] == ' ' and not self.game.current_winner:
            self.game.make_move(square, 'X')
            self.buttons[square].config(text='X', fg="blue")
            
            if self.check_game_over():
                return
                
            self.root.after(100, self.ai_move)

    def ai_move(self):
        if not self.game.empty_squares() or self.game.current_winner:
            return
            
        square = minimax(self.game, 'O', depth=4)['position']
            
        if square is not None:
            self.game.make_move(square, 'O')
            self.buttons[square].config(text='O', fg="red")
            self.check_game_over()

    def check_game_over(self):
        if self.game.current_winner == 'X':
            messagebox.showinfo("Victory!", f"You beat Level {self.current_level}!")
            self.current_level += 1
            self.save_progress(self.current_level)
            self.cleanup_board()
            return True
        elif self.game.current_winner == 'O':
            messagebox.showinfo("Defeat", "The AI wins. Try again!")
            self.cleanup_board()
            return True
        elif not self.game.empty_squares():
            messagebox.showinfo("Tie", "No more moves! Try again.")
            self.cleanup_board()
            return True
        return False

    def cleanup_board(self):
        self.board_frame.pack_forget()
        self.buttons = []
        self.setup_menu()

if __name__ == '__main__':
    root = tk.Tk()
    app = CampaignGUI(root)
    root.mainloop()