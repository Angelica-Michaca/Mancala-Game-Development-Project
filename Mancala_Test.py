import tkinter as tk
from tkinter import messagebox, simpledialog
import copy

class Mancala:
    def __init__(self, root):
        self.root = root
        self.root.title("Mancala")
        self.player_turn = 1
        self.game_over = False
        self.single_player = True  # Default; will be set in choose_game_mode
        self.board = [4] * 6 + [0] + [4] * 6 + [0]  # Initialize the board
        self.player_names = ["Player 1", "AI"]  # Default names
        self.ask_player_name()   # Ask for Player 1's name
        self.choose_game_mode()  # Choose single-player or two-player mode
        self.welcome_user()      # Welcome and show the rules

    def ask_player_name(self):
        player_name = simpledialog.askstring("Enter Name", "Please enter your name (Player 1):")
        if player_name:
            self.player_names[0] = player_name
        else:
            messagebox.showinfo("Goodbye!", "Name not provided. Exiting.")
            self.root.destroy()

    def choose_game_mode(self):
        mode = messagebox.askquestion("Game Mode", "Do you want to play against the AI?\n(Yes for AI, No for two-player)")
        if mode == 'yes':
            self.single_player = True
            self.player_names[1] = "AI"
        else:
            self.single_player = False
            player2_name = simpledialog.askstring("Enter Name", "Please enter Player 2's name:")
            if player2_name:
                self.player_names[1] = player2_name
            else:
                messagebox.showinfo("Goodbye!", "Name not provided for Player 2. Exiting.")
                self.root.destroy()

    def welcome_user(self):
        response = messagebox.askyesno("Welcome to Mancala!", "Welcome to Mancala! Would you like to play?")
        if response:
            self.show_rules()
        else:
            messagebox.showinfo("Goodbye!", "Goodbye! Have a great day!")
            self.root.destroy()

    def show_rules(self):
        rules = (
            "Rules of Mancala:\n\n"
            "1. The game is played with two players.\n"
            "2. Each player has six pits and one Mancala (store).\n"
            "3. Players take turns picking up all the stones from one of their pits and distributing them counterclockwise.\n"
            "4. If the last stone lands in your Mancala, you get another turn.\n"
            "5. If the last stone lands in an empty pit on your side, you capture that stone and all stones in the opposite pit and place them in your Mancala.\n"
            "6. The game ends when all pits on one side are empty. The player with the most stones in their Mancala wins.\n\n"
            "Do you understand the rules?"
        )
        response = messagebox.askyesno("Mancala Rules", rules)
        if response:
            self.create_board()
        else:
            messagebox.showinfo("Goodbye!", "It's okay. Goodbye!")
            self.root.destroy()

    def create_board(self):
        # Mancala for Player 2 (Left)
        self.mancala2 = tk.Label(self.root, text=str(self.board[6]), font=("Arial", 20), relief="sunken", width=5, height=2)
        self.mancala2.grid(row=1, column=0, padx=10, pady=10)

        # Pits for Player 2 (Top Row)
        self.pits2 = []
        for i in range(5, -1, -1):
            pit = tk.Button(self.root, text=str(self.board[i]), font=("Arial", 15), width=5, height=2,
                            command=lambda i=i: self.move_stones(i))
            pit.grid(row=1, column=6 - i, padx=5, pady=5)
            self.pits2.append(pit)

        # Pits for Player 1 (Bottom Row)
        self.pits1 = []
        for i in range(7, 13):
            pit = tk.Button(self.root, text=str(self.board[i]), font=("Arial", 15), width=5, height=2,
                            command=lambda i=i: self.move_stones(i))
            pit.grid(row=2, column=i - 6, padx=5, pady=5)
            self.pits1.append(pit)

        # Mancala for Player 1 (Right)
        self.mancala1 = tk.Label(self.root, text=str(self.board[13]), font=("Arial", 20), relief="sunken", width=5, height=2)
        self.mancala1.grid(row=1, column=7, padx=10, pady=10, rowspan=2)

        # Turn Label (Centered Below the Board)
        self.turn_label = tk.Label(self.root, text=f"{self.player_names[self.player_turn - 1]}'s Turn", font=("Arial", 15))
        self.turn_label.grid(row=3, column=0, columnspan=8, pady=10)

        # If it's AI's turn first in single player mode, make the move
        if self.single_player and self.player_turn == 2:
            self.root.after(1000, self.ai_move)

    def move_stones(self, pit_index):
        if self.game_over:
            return

        # Validate move: check that the selected pit belongs to the current player
        if self.player_turn == 1 and pit_index not in range(7, 13):
            messagebox.showinfo("Wrong Side", f"{self.player_names[0]}, please choose a pit from your side (bottom row)!")
            return
        if self.player_turn == 2 and pit_index not in range(0, 6):
            messagebox.showinfo("Wrong Side", f"{self.player_names[1]}, please choose a pit from your side (top row)!")
            return

        stones = self.board[pit_index]
        if stones == 0:
            messagebox.showinfo("Invalid Move", "This pit is empty. Choose another pit.")
            return

        self.board[pit_index] = 0
        current_index = pit_index

        # Distribute the stones
        while stones > 0:
            current_index = (current_index + 1) % 14
            if (self.player_turn == 1 and current_index == 6) or (self.player_turn == 2 and current_index == 13):
                continue  # Skip opponent's Mancala
            self.board[current_index] += 1
            stones -= 1

        # Capture rule: if last stone lands in an empty pit on the player's side
        if self.player_turn == 1 and current_index in range(7, 13) and self.board[current_index] == 1:
            opposite_index = 12 - current_index
            if self.board[opposite_index] > 0:
                self.board[13] += self.board[current_index] + self.board[opposite_index]
                self.board[current_index] = 0
                self.board[opposite_index] = 0
        elif self.player_turn == 2 and current_index in range(0, 6) and self.board[current_index] == 1:
            opposite_index = 12 - current_index
            if self.board[opposite_index] > 0:
                self.board[6] += self.board[current_index] + self.board[opposite_index]
                self.board[current_index] = 0
                self.board[opposite_index] = 0

        # Check if the last stone landed in the player's Mancala (granting an extra turn)
        if (self.player_turn == 1 and current_index == 13) or (self.player_turn == 2 and current_index == 6):
            self.turn_label.config(text=f"{self.player_names[self.player_turn - 1]} gets another turn!")
            if self.single_player and self.player_turn == 2:
                self.root.after(1000, self.ai_move)
        else:
            # Switch turns
            self.player_turn = 3 - self.player_turn
            self.turn_label.config(text=f"{self.player_names[self.player_turn - 1]}'s Turn")
            if self.single_player and self.player_turn == 2:
                self.root.after(1000, self.ai_move)

        # Check for game over: one side empty
        if all(stone == 0 for stone in self.board[0:6]):
            # Player 2 captures all remaining stones on their side
            self.board[13] += sum(self.board[7:13])
            for i in range(7, 13):
                self.board[i] = 0
            self.game_over = True
            self.update_board()
            self.end_game()
            return
        elif all(stone == 0 for stone in self.board[7:13]):
            # Player 1 captures all remaining stones on their side
            self.board[6] += sum(self.board[0:6])
            for i in range(0, 6):
                self.board[i] = 0
            self.game_over = True
            self.update_board()
            self.end_game()
            return

        self.update_board()

    def ai_move(self):
        if self.game_over:
            return

        # Use alpha-beta pruning to choose the move
        _, chosen_pit = self.alpha_beta(self.board, depth=5, alpha=float('-inf'), beta=float('inf'), maximizingPlayer=True)
        if chosen_pit != -1:
            self.move_stones(chosen_pit)

    def heuristic_evaluation(self, board):
        # Evaluation based on the difference in Mancala stones
        return board[6] - board[13]

    def is_game_over(self, board):
        return all(stone == 0 for stone in board[0:6]) or all(stone == 0 for stone in board[7:13])

    def legal_moves(self, board, player):
        if player == 1:
            return [i for i in range(7, 13) if board[i] > 0]
        else:
            return [i for i in range(0, 6) if board[i] > 0]

    def make_move(self, board, pit_index, player):
        new_board = copy.deepcopy(board)
        stones = new_board[pit_index]
        new_board[pit_index] = 0
        current_index = pit_index

        while stones > 0:
            current_index = (current_index + 1) % 14
            if (player == 1 and current_index == 6) or (player == 2 and current_index == 13):
                continue
            new_board[current_index] += 1
            stones -= 1

        # Note: Extra turn or capture moves are not simulated in the alpha-beta search.
        return new_board

    def alpha_beta(self, board, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.is_game_over(board):
            return self.heuristic_evaluation(board), -1

        best_move = -1
        if maximizingPlayer:
            maxEval = float('-inf')
            for move in self.legal_moves(board, player=2):
                eval, _ = self.alpha_beta(self.make_move(board, move, player=2), depth - 1, alpha, beta, False)
                if eval > maxEval:
                    maxEval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval, best_move
        else:
            minEval = float('inf')
            for move in self.legal_moves(board, player=1):
                eval, _ = self.alpha_beta(self.make_move(board, move, player=1), depth - 1, alpha, beta, True)
                if eval < minEval:
                    minEval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval, best_move

    def update_board(self):
        for i in range(6):
            self.pits2[i].config(text=str(self.board[5 - i]))
        self.mancala2.config(text=str(self.board[6]))

        for i in range(6):
            self.pits1[i].config(text=str(self.board[7 + i]))
        self.mancala1.config(text=str(self.board[13]))

    def end_game(self):
        # Determine the winner and display a message
        if self.board[6] > self.board[13]:
            winner = self.player_names[1]
        elif self.board[13] > self.board[6]:
            winner = self.player_names[0]
        else:
            winner = "It's a tie!"
        messagebox.showinfo("Game Over", f"{winner} wins!")

if __name__ == "__main__":
    root = tk.Tk()
    game = Mancala(root)
    root.mainloop()
