def print_board(board):
    """Prints the 3x3 tic-tac-toe board with a more detailed design."""
    print("\n")
    print("    1   2   3")
    print("  ╔═══╦═══╦═══╗")
    print(f"A ║ {board[0]} ║ {board[1]} ║ {board[2]} ║")
    print("  ╠═══╬═══╬═══╣")
    print(f"B ║ {board[3]} ║ {board[4]} ║ {board[5]} ║")
    print("  ╠═══╬═══╣")
    print(f"C ║ {board[6]} ║ {board[7]} ║ {board[8]} ║")
    print("  ╚═══╩═══╩═══╝")
    print("\n")

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

def get_player_move(board, player):
    """Gets a valid move from the current player."""
    row_map = {'A': 0, 'B': 1, 'C': 2}
    while True:
        try:
            prompt = f"PLAYER {player}'s TURN | Enter a cell (e.g., A1, B2): "
            move_input = input(prompt).upper()

            if len(move_input) == 2:
                row_char, col_char = move_input[0], move_input[1]
                if row_char in row_map and col_char.isdigit():
                    row = row_map[row_char]
                    col = int(col_char) - 1

                    if 0 <= row <= 2 and 0 <= col <= 2:
                        move_index = row * 3 + col
                        if board[move_index].isdigit():
                            return move_index
                        else:
                            print("🚫 That spot is already taken! Try another one.")
                    else:
                        print("⚠️  Invalid cell coordinates. Row must be A, B, or C, and column must be 1, 2, or 3.")
                else:
                    print("⚠️  Invalid input format. Please use the format like A1, B2, C3.")
            else:
                print("⚠️  Invalid input format. Please enter a row and a column (e.g., A1).")
        except ValueError:
            print("⚠️  Invalid input. Please enter a valid cell.")

def main():
    """Main function to run the Tic Tac Toe game loop."""
    board = [str(i) for i in range(1, 10)]
    current_player = "X"
    game_is_running = True

    print("\n" + "="*30)
    print("     WELCOME TO TIC TAC TOE")
    print("="*30 + "\n")

    while game_is_running:
        print_board(board)
        
        move_index = get_player_move(board, current_player)
        board[move_index] = current_player

        if check_win(board, current_player):
            print_board(board)
            print("\n" + "*"*30)
            print("*          GAME OVER          *")
            win_message = f"PLAYER {current_player} WINS! 🎉"
            print(f"* {win_message:^26} *")
            print("*"*30)
            game_is_running = False
        elif check_tie(board):
            print_board(board)
            print("\n" + "*"*30)
            print("*          GAME OVER          *")
            tie_message = "IT'S A TIE!"
            print(f"* {tie_message:^26} *")
            print("*"*30)
            game_is_running = False
        else:
            # Switch to the other player
            current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    main()