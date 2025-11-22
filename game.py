import tkinter as tk
from tkinter import messagebox

def create_gui(board, current_player, game_is_running, handle_move):
    """Creates the Tkinter GUI for the Tic Tac Toe game."""
    window = tk.Tk()
    window.title("Tic Tac Toe")
    window.geometry("300x350")
    window.resizable(False, False)

    frame_board = tk.Frame(window)
    frame_board.pack(pady=10)

    buttons = []
    for i in range(9):
        row = i // 3
        col = i % 3
        button = tk.Button(frame_board, text=board[i] if board[i].isalpha() else "", 
                           font=("Arial", 40), width=3, height=1, 
                           command=lambda idx=i: handle_move(idx))
        button.grid(row=row, column=col, padx=5, pady=5)
        buttons.append(button)

    label_player = tk.Label(window, text=f"Player {current_player}'s Turn", font=("Arial", 16))
    label_player.pack(pady=10)

    def update_display():
        for i in range(9):
            buttons[i].config(text=board[i] if board[i].isalpha() else "", 
                              state=tk.NORMAL if board[i].isdigit() else tk.DISABLED)
        label_player.config(text=f"Player {current_player}'s Turn")
        window.update_idletasks()

    return window, update_display, buttons, label_player

def check_win(board, player):
    """Checks if the current player has won."""
    win_conditions = [
        # Rows
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        # Columns
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        # Diagonals
        (0, 4, 8), (2, 4, 6)
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def check_tie(board):
    """Checks if the game is a tie (board is full)."""
    return all(not spot.isdigit() for spot in board)

def main():
    """Main function to run the Tic Tac Toe game loop."""
    board = [str(i) for i in range(1, 10)]
    current_player = "X"
    game_is_running = True

    def handle_move(move_index):
        nonlocal board, current_player, game_is_running, window, update_display, label_player

        if game_is_running and board[move_index].isdigit():
            board[move_index] = current_player
            update_display()

            if check_win(board, current_player):
                messagebox.showinfo("Game Over", f"Player {current_player} Wins!")
                game_is_running = False
                window.destroy()
            elif check_tie(board):
                messagebox.showinfo("Game Over", "It's a Tie!")
                game_is_running = False
                window.destroy()
            else:
                current_player = "O" if current_player == "X" else "X"
                label_player.config(text=f"Player {current_player}'s Turn")
                
    window, update_display, buttons, label_player = create_gui(board, current_player, game_is_running, handle_move)
    update_display()
    window.mainloop()

if __name__ == "__main__":
    main()