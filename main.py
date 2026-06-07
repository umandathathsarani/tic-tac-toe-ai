import tkinter as tk
from tkinter import messagebox
import json
import os
import random
import pygame
from game import TicTacToe
from ai import minimax

SAVE_FILE = "save_data.json"

THEME = {
    "bg": "#546B41",
    "text": "#FFF8EC",
    "btn_bg": "#DCCCAC",
    "btn_active": "#99AD7A",
    "x_color": "#2A3B1D",
    "o_color": "#8A4F3C",
    "dead": "#99AD7A",
    "play_btn": "#FFF8EC",
    "play_text": "#546B41"
}

class CampaignGUI:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg=THEME["bg"])
        self.root.geometry("+300+150")
        
        self.pixel = tk.PhotoImage(width=1, height=1)
        self.current_square_size = 0
        self.allow_resize = False
        
        try:
            pygame.mixer.init()
            self.snd_move = pygame.mixer.Sound("move.wav")
            self.snd_win = pygame.mixer.Sound("win.wav")
            self.snd_lose = pygame.mixer.Sound("lose.wav")
            self.snd_tie = pygame.mixer.Sound("tie.wav")
            self.audio = True
        except:
            self.audio = False
        
        self.current_level = self.load_progress()
        self.game = None
        self.buttons = []
        
        self.main_frame = tk.Frame(self.root, bg=THEME["bg"])
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.bind("<Configure>", self.on_resize)
        
        self.setup_menu()

    def play_sound(self, sound_obj):
        if self.audio:
            try:
                sound_obj.play()
            except:
                pass

    def on_resize(self, event):
        if not getattr(self, 'allow_resize', False):
            return
            
        if event.widget == self.main_frame and self.buttons and self.game:
            self.scale_board(event.width, event.height)

    def scale_board(self, width, height):
        avail_w = width - 100
        avail_h = height - 100
        
        if avail_w < 100 or avail_h < 100:
            return
            
        grid_size = self.game.grid_size
        padding_offset = grid_size * 6
        
        new_size = max(30, min((avail_w - padding_offset) // grid_size, (avail_h - padding_offset) // grid_size))
        new_size = min(new_size, 150) 
        
        font_size = max(12, new_size // 3)
        
        if self.current_square_size != new_size:
            self.current_square_size = new_size
            for btn in self.buttons:
                btn.config(width=new_size, height=new_size, font=('Segoe UI', font_size, 'bold'))

    def get_level_data(self, level):
        grid_size = min(10, 3 + (level - 1) // 3)
        
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
        self.allow_resize = False
        self.root.title(f"Tic-Tac-Toe: Level {self.current_level}")
        
        self.menu_frame = tk.Frame(self.main_frame, bg=THEME["bg"])
        self.menu_frame.pack(pady=30, padx=60, expand=True)
        
        tk.Label(self.menu_frame, text=f"Level {self.current_level}", font=('Segoe UI', 24, 'bold'), bg=THEME["bg"], fg=THEME["text"]).pack(pady=10)
        
        level_data = self.get_level_data(self.current_level)
        desc = f"Grid: {level_data['grid_size']}x{level_data['grid_size']}\nWin: {level_data['win_req']} in a row"
        tk.Label(self.menu_frame, text=desc, font=('Segoe UI', 14), bg=THEME["bg"], fg=THEME["text"]).pack(pady=10)
        
        tk.Button(self.menu_frame, text="Play Level", font=('Segoe UI', 14, 'bold'), bg=THEME["play_btn"], fg=THEME["play_text"], 
                  activebackground=THEME["btn_active"], activeforeground=THEME["play_text"], relief="flat", padx=20, pady=5, 
                  command=self.start_level).pack(pady=20)
                  
        tk.Button(self.menu_frame, text="Reset Progress", font=('Segoe UI', 10), bg=THEME["bg"], fg=THEME["text"], 
                  activebackground=THEME["bg"], relief="flat", command=self.reset_campaign).pack(pady=5)
                  
        self.root.update_idletasks()
        self.root.geometry("")

    def reset_campaign(self):
        self.current_level = 1
        self.save_progress(1)
        self.menu_frame.pack_forget()
        self.setup_menu()

    def start_level(self):
        self.allow_resize = False
        self.menu_frame.pack_forget()
        
        level_data = self.get_level_data(self.current_level)
        self.game = TicTacToe(grid_size=level_data['grid_size'], 
                              win_requirement=level_data['win_req'], 
                              dead_squares=level_data['dead'])
                              
        self.board_frame = tk.Frame(self.main_frame, bg=THEME["bg"])
        self.board_frame.pack(pady=10, padx=20, expand=True)
        
        self.buttons = []
        
        font_size = 24 if level_data['grid_size'] <= 4 else 16
        square_size = 80 if level_data['grid_size'] <= 4 else 50 
        
        for i in range(level_data['grid_size'] * level_data['grid_size']):
            btn = tk.Button(self.board_frame, text=" ", font=('Segoe UI', font_size, 'bold'), 
                            image=self.pixel, compound="c", width=square_size, height=square_size,
                            bg=THEME["btn_bg"], fg=THEME["text"], activebackground=THEME["btn_active"], relief="raised", bd=3,
                            command=lambda s=i: self.player_move(s))
            
            if i in level_data['dead']:
                btn.config(state="disabled", bg=THEME["dead"], disabledforeground=THEME["dead"], relief="sunken")
                
            btn.grid(row=i // level_data['grid_size'], column=i % level_data['grid_size'], padx=3, pady=3)
            self.buttons.append(btn)
            
        self.current_square_size = square_size
        self.root.update_idletasks()
        
        if self.root.state() != 'zoomed':
            self.root.geometry("")
            
        self.root.after(200, self.enable_resize)

    def enable_resize(self):
        self.allow_resize = True
        if self.buttons and self.game:
            self.scale_board(self.main_frame.winfo_width(), self.main_frame.winfo_height())

    def player_move(self, square):
        if self.game.board[square] == ' ' and not self.game.current_winner:
            self.game.make_move(square, 'X')
            self.buttons[square].config(text='X', fg=THEME["x_color"])
            self.play_sound(self.snd_move)
            
            if self.check_game_over():
                return
                
            self.root.after(150, self.ai_move)

    def ai_move(self):
        if not self.game.empty_squares() or self.game.current_winner:
            return
            
        square = minimax(self.game, 'O', depth=3)['position']
            
        if square is not None:
            self.game.make_move(square, 'O')
            self.buttons[square].config(text='O', fg=THEME["o_color"])
            self.play_sound(self.snd_move)
            self.check_game_over()

    def check_game_over(self):
        if self.game.current_winner == 'X':
            self.play_sound(self.snd_win)
            messagebox.showinfo("Victory!", f"You beat Level {self.current_level}!")
            self.current_level += 1
            self.save_progress(self.current_level)
            self.cleanup_board()
            return True
        elif self.game.current_winner == 'O':
            self.play_sound(self.snd_lose)
            messagebox.showinfo("Defeat", "The AI wins. Try again!")
            self.cleanup_board()
            return True
        elif not self.game.empty_squares():
            self.play_sound(self.snd_tie)
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