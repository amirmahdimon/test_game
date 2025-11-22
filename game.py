import tkinter as tk
from tkinter import messagebox
import sys

# ANSI color codes (not directly used in GUI but good for context)
COLOR_X = '\033[92m'  # Green
COLOR_O = '\033[94m'  # Blue
COLOR_RESET = '\033[0m'
COLOR_SEPARATOR = '\033[90m' # Grey for separators

# GUI Color Scheme
GUI_BG_COLOR = "#2E3440"  # Dark background
GUI_FG_COLOR = "#ECEFF4"  # Light text
BUTTON_X_COLOR = "#A3BE8C" # Greenish for X
BUTTON_O_COLOR = "#81A1C1" # Bluish for O
BUTTON_DEFAULT_COLOR = "#4C566A" # Greyish for default
BUTTON_HOVER_COLOR = "#5E81AC" # Lighter blue for hover
LABEL_TURN_COLOR = "#ECEFF4" # Light text for turn label
RESTART_BUTTON_BG = "#5E81AC" # Bluish for restart
RESTART_BUTTON_FG = "#ECEFF4"

def create_gui(board_size, board, current_player, game_is_running, handle_move, restart_game_callback):
    """Creates the Tkinter GUI for the Tic Tac Toe game with enhanced design."""
    window = tk.Tk()
    window.title("Tic Tac Toe")
    window.configure(bg=GUI_BG_COLOR)

    # Adjust button size and font size dynamically
    base_button_size = 6
    base_button_font_size = 30
    button_size = base_button_size + (board_size - 3) * 1
    button_font_size = base_button_font_size - (board_size - 3) * 8

    # Adjust window size dynamically
    base_window_size_w = 400
    base_window_size_h = 450
    window_width = base_window_size_w + (board_size - 3) * 80
    window_height = base_window_size_h + (board_size - 3) * 80
    window.geometry(f"{window_width}x{window_height}")
    window.resizable(False, False)

    frame_board = tk.Frame(window, bg=GUI_BG_COLOR)
    frame_board.pack(pady=20, padx=20)

    buttons = []
    for i in range(board_size * board_size):
        row = i // board_size
        col = i % board_size
        button = tk.Button(frame_board, text="",
                           font=("Segoe UI", button_font_size, "bold"),
                           width=button_size, height=2,
                           bg=BUTTON_DEFAULT_COLOR, fg=GUI_FG_COLOR,
                           activebackground=BUTTON_HOVER_COLOR,
                           activeforeground=GUI_FG_COLOR,
                           relief=tk.RAISED, borderwidth=3,
                           command=lambda idx=i: handle_move(idx))
        button.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
        buttons.append(button)
        # Configure row and column weights for proper resizing if window were resizable
        frame_board.grid_rowconfigure(row, weight=1)
        frame_board.grid_columnconfigure(col, weight=1)


    label_player = tk.Label(window, text=f"Player X's Turn", font=("Segoe UI", 20, "bold"), bg=GUI_BG_COLOR, fg=LABEL_TURN_COLOR)
    label_player.pack(pady=10)

    button_restart = tk.Button(window, text="Restart Game", font=("Segoe UI", 16, "bold"),
                               command=restart_game_callback,
                               bg=RESTART_BUTTON_BG, fg=RESTART_BUTTON_FG,
                               activebackground=BUTTON_HOVER_COLOR, activeforeground=GUI_FG_COLOR,
                               relief=tk.RAISED, borderwidth=2)
    button_restart.pack(pady=15)

    def update_display():
        """Updates the GUI elements to reflect the current game state."""
        for i in range(board_size * board_size):
            button_text = board[i]
            if button_text == "X":
                button_color = BUTTON_X_COLOR
            elif button_text == "O":
                button_color = BUTTON_O_COLOR
            else:
                button_color = BUTTON_DEFAULT_COLOR # Default color for empty spots

            buttons[i].config(text=button_text if button_text.isalpha() else "",
                              state=tk.NORMAL if board[i].isdigit() else tk.DISABLED,
                              fg=GUI_FG_COLOR,  # Ensure text color is consistent
                              bg=button_color)
        
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
        """Destroys the current window and starts a new game."""
        nonlocal window
        if window:
            window.destroy()
        play_game(board_size)

    def handle_move(move_index):
        """Handles a player's move, updates the board, checks for win/tie, and switches players."""
        nonlocal board, current_player, game_is_running, window, update_display, label_player, buttons

        if game_is_running and board[move_index].isdigit():
            board[move_index] = current_player
            
            # Update button appearance based on player
            button_color = BUTTON_X_COLOR if current_player == "X" else BUTTON_O_COLOR
            buttons[move_index].config(text=current_player, state=tk.DISABLED, fg=GUI_FG_COLOR, bg=button_color)

            if check_win(board, current_player, board_size):
                messagebox.showinfo("Game Over", f"Player {current_player} Wins!", parent=window)
                game_is_running = False
                
                def ask_play_again():
                    if messagebox.askyesno("Play Again?", "Do you want to play again?", parent=window):
                        window.destroy()
                        play_game(board_size)
                    else:
                        window.destroy()
                        sys.exit()
                ask_play_again()

            elif check_tie(board):
                messagebox.showinfo("Game Over", "It's a Tie!", parent=window)
                game_is_running = False
                
                def ask_play_again():
                    if messagebox.askyesno("Play Again?", "Do you want to play again?", parent=window):
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
    
    # Initial display update for the buttons based on any pre-filled board (not applicable here but good practice)
    for i in range(board_size * board_size):
        if board[i].isalpha():
            button_color = BUTTON_X_COLOR if board[i] == "X" else BUTTON_O_COLOR
            buttons[i].config(text=board[i], fg=GUI_FG_COLOR, bg=button_color, state=tk.DISABLED)
        else:
            buttons[i].config(text="", bg=BUTTON_DEFAULT_COLOR)

    window.mainloop()

def get_board_size_from_user():
    """Prompts the user for the board size and validates it, using Tkinter for input."""
    dialog_root = tk.Tk()
    dialog_root.withdraw() # Hide the main window

    while True:
        try:
            # Use tk.simpledialog.askstring which is the correct way to get string input
            from tkinter import simpledialog
            size_str = simpledialog.askstring("Board Size", "Enter board size (e.g., 3 for 3x3, 4 for 4x4):", parent=dialog_root, initialvalue="3")
            
            if size_str is None: # User cancelled
                dialog_root.destroy()
                sys.exit()
            size = int(size_str)
            if size < 3:
                messagebox.showerror("Invalid Input", "Board size must be at least 3x3.", parent=dialog_root)
            else:
                dialog_root.destroy()
                return size
        except ValueError:
            messagebox.showerror("Invalid Input", "Invalid input. Please enter a number.", parent=dialog_root)
        except tk.TclError: # Handle case where prompt might fail (e.g., no display)
            print("Error: Could not display input prompt. Please ensure you are running in an environment with a display.")
            dialog_root.destroy()
            sys.exit(1)
        finally:
            # Ensure the dialog root is destroyed if the loop exits for any reason other than sys.exit()
            if dialog_root.winfo_exists():
                dialog_root.destroy()


def main():
    """Main function to get board size and start the game."""
    board_size = get_board_size_from_user()
    play_game(board_size)

if __name__ == "__main__":
    main()