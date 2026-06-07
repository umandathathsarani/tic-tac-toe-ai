import tkinter as tk
from tkinter import messagebox
import json
import os
import random
from game import TicTacToe
from ai import minimax

SAVE_FILE = "save_data.json"

class CampaignGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe: Infinite Campaign")
        self.current_level = self.load_progress()
        self.game = None
        self.buttons = []
        self.setup_menu()

    def get_level_data(self, level):
        grid_size = min(12, 3 + (level - 1) // 3)
        
        if grid_size <= 4:
            win_req = 3
        elif grid_size <= 6:
            win_req = 4
        else:
            win_req = 5
            
        num_dead = min((grid_size * grid_size) // 5, (level - 1))
        
        random.seed(level)
        dead = random.sample(range(grid_size * grid_size), num_dead)
        random.seed()
        
        return {"grid_size": grid_size, "win_req": win_req, "dead": dead}

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
        
        tk.Label(self.menu_frame, text=f"Level {self.current_level}", font=('Arial', 18, 'bold')).pack(pady=10)
        
        level_data = self.get_level_data(self.current_level)
        desc = f"Grid: {level_data['grid_size']}x{level_data['grid_size']}\nWin: {level_data['win_req']} in a row"
        tk.Label(self.menu_frame, text=desc, font=('Arial', 12)).pack(pady=5)
        
        tk.Button(self.menu_frame, text="Play Level", font=('Arial', 14), bg="green", fg="white", command=self.start_level).pack(pady=15)
        tk.Button(self.menu_frame, text="Reset Progress", font=('Arial', 10), command=self.reset_campaign).pack(pady=5)

    def reset_campaign(self):
        self.current_level = 1
        self.save_progress(1)
        self.menu_frame.pack_forget()
        self.setup_menu()

    def start_level(self):
        self.menu_frame.pack_forget()
        
        level_data = self.get_level_data(self.current_level)
        self.game = TicTacToe(grid_size=level_data['grid_size'], 
                              win_requirement=level_data['win_req'], 
                              dead_squares=level_data['dead'])
                              
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=10, padx=10)
        
        self.buttons = []
        font_size = 18 if level_data['grid_size'] <= 5 else 12
        btn_width = 4 if level_data['grid_size'] <= 5 else 2
        btn_height = 2 if level_data['grid_size'] <= 5 else 1
        
        for i in range(level_data['grid_size'] * level_data['grid_size']):
            btn = tk.Button(self.board_frame, text=" ", font=('Arial', font_size, 'bold'), width=btn_width, height=btn_height,
                            command=lambda s=i: self.player_move(s))
            
            if i in level_data['dead']:
                btn.config(state="disabled", bg="black")
                
            btn.grid(row=i // level_data['grid_size'], column=i % level_data['grid_size'], padx=1, pady=1)
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
            
        square = minimax(self.game, 'O', depth=3)['position']
            
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
            messagebox.showinfo("Survival!", "It's a tie! You survived the AI. Moving to next level!")
            self.current_level += 1
            self.save_progress(self.current_level)
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