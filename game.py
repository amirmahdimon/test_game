def print_board(board):
    """Prints the 3x3 tic-tac-toe board."""
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def check_win(board, player):
    """Checks if the current player has won."""
    win_conditions = [
        # Rows
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        # Columns
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        # Diagonals
        [0, 4, 8], [2, 4, 6]
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
    while True:
        try:
            move_str = input(f"Player {player}, enter your move (1-9): ")
            move = int(move_str)
            if 1 <= move <= 9:
                if board[move - 1].isdigit():
                    return move - 1
                else:
                    print("This spot is already taken. Please choose another one.")
            else:
                print("Invalid input. Please enter a number between 1 and 9.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    """Main function to run the Tic Tac Toe game loop."""
    board = [str(i) for i in range(1, 10)]
    current_player = "X"
    game_is_running = True

    print("Welcome to Tic Tac Toe!")

    while game_is_running:
        print_board(board)
        
        move_index = get_player_move(board, current_player)
        board[move_index] = current_player

        if check_win(board, current_player):
            print_board(board)
            print(f"Congratulations! Player {current_player} wins!")
            game_is_running = False
        elif check_tie(board):
            print_board(board)
            print("The game is a tie!")
            game_is_running = False
        else:
            # Switch to the other player
            current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    main()