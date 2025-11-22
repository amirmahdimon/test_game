import tkinter as tk
from tkinter import messagebox
import sys

# ANSI color codes
COLOR_X = '\033[92m'  # Green
COLOR_O = '\033[94m'  # Blue
COLOR_RESET = '\033[0m'
COLOR_SEPARATOR = '\033[90m' # Grey for separators

def create_gui(board_size, board, current_player, game_is_running, handle_move, restart_game_callback):
    """Creates the Tkinter GUI for the Tic Tac Toe game."""
    window = tk.Tk()
    window.title("Tic Tac Toe")
    
    # Adjust button size and font size dynamically
    base_button_size = 5
    base_button_font_size = 40
    button_size = base_button_size + (board_size - 3) * 2 # Increase button size for larger boards
    button_font_size = base_button_font_size - (board_size - 3) * 10 # Adjust font size based on board size

    # Adjust window size dynamically
    base_window_size = 300
    window_size = base_window_size + (board_size - 3) * 100
    window.geometry(f"{window_size}x{window_size + 50}")
    window.resizable(False, False)

    frame_board = tk.Frame(window)
    frame_board.pack(pady=20) # Increased padding

    buttons = []
    for i in range(board_size * board_size):
        row = i // board_size
        col = i % board_size
        button = tk.Button(frame_board, text=board[i] if board[i].isalpha() else "", 
                           font=("Arial", button_font_size), width=button_size, height=2, # Increased height
                           command=lambda idx=i: handle_move(idx))
        button.grid(row=row, column=col, padx=10, pady=10) # Increased padding
        buttons.append(button)

    label_player = tk.Label(window, text=f"Player {current_player}'s Turn", font=("Arial", 24)) # Increased font size
    label_player.pack(pady=20) # Increased padding

    button_restart = tk.Button(window, text="Restart Game", font=("Arial", 16), command=restart_game_callback) # Increased font size
    button_restart.pack(pady=15) # Increased padding

    def update_display():
        for i in range(board_size * board_size):
            button_text = board[i]
            if button_text == "X":
                button_color = "green"
            elif button_text == "O":
                button_color = "blue"
            else:
                button_color = None # Default color for empty spots

            buttons[i].config(text=button_text if button_text.isalpha() else "", 
                              state=tk.NORMAL if board[i].isdigit() else tk.DISABLED,
                              fg=button_color)
        label_player.config(text=f"Player {current_player}'s Turn")
        window.update_idletasks()

    return window, update_display, buttons, label_player

def get_win_conditions(board_size):
    """Generates win conditions for an N x N board."""
    win_conditions = []
    # Rows
    for r in range(board_size):
        win_conditions.append(tuple(r * board_size + c for c in range(board_size)))
    # Columns
    for c in range(board_size):
        win_conditions.append(tuple(r * board_size + c for r in range(board_size)))
    # Diagonals
    win_conditions.append(tuple(i * board_size + i for i in range(board_size)))
    win_conditions.append(tuple(i * board_size + (board_size - 1 - i) for i in range(board_size)))
    return win_conditions

def check_win(board, player, board_size):
    """Checks if the current player has won."""
    win_conditions = get_win_conditions(board_size)
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def check_tie(board):
    """Checks if the game is a tie (board is full)."""
    return all(not spot.isdigit() for spot in board)

def play_game(board_size):
    """Initializes and runs a single game of Tic Tac Toe."""
    board = [str(i) for i in range(1, board_size * board_size + 1)]
    current_player = "X"
    game_is_running = True
    window = None
    update_display = None
    label_player = None
    buttons = []

    def restart_game_callback():
        nonlocal window
        if window:
            window.destroy()
        play_game(board_size)

    def handle_move(move_index):
        nonlocal board, current_player, game_is_running, window, update_display, label_player, buttons

        if game_is_running and board[move_index].isdigit():
            board[move_index] = current_player
            
            # Update button appearance based on player
            button_color = "green" if current_player == "X" else "blue"
            buttons[move_index].config(text=current_player, state=tk.DISABLED, fg=button_color)

            if check_win(board, current_player, board_size):
                messagebox.showinfo("Game Over", f"Player {current_player} Wins!")
                game_is_running = False
                
                def ask_play_again():
                    if messagebox.askyesno("Play Again?", "Do you want to play again?"):
                        window.destroy()
                        play_game(board_size)
                    else:
                        window.destroy()
                        sys.exit()
                ask_play_again()

            elif check_tie(board):
                messagebox.showinfo("Game Over", "It's a Tie!")
                game_is_running = False
                
                def ask_play_again():
                    if messagebox.askyesno("Play Again?", "Do you want to play again?"):
                        window.destroy()
                        play_game(board_size)
                    else:
                        window.destroy()
                        sys.exit()
                ask_play_again()

            else:
                current_player = "O" if current_player == "X" else "X"
                label_player.config(text=f"Player {current_player}'s Turn")
                
    window, update_display, buttons, label_player = create_gui(board_size, board, current_player, game_is_running, handle_move, restart_game_callback)
    
    # Initial display update for the buttons
    for i in range(board_size * board_size):
        if board[i].isalpha():
            button_color = "green" if board[i] == "X" else "blue"
            buttons[i].config(text=board[i], fg=button_color, state=tk.DISABLED)
        else:
            buttons[i].config(text="")

    window.mainloop()

def get_board_size_from_user():
    """Prompts the user for the board size and validates it."""
    while True:
        try:
            size_str = input("Enter board size (e.g., 3 for 3x3, 4 for 4x4): ")
            size = int(size_str)
            if size < 3:
                print("Board size must be at least 3x3.")
            else:
                return size
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    """Main function to get board size and start the game."""
    board_size = get_board_size_from_user()
    play_game(board_size)

if __name__ == "__main__":
    main()