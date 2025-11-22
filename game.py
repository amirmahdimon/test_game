def print_board(board):
    """Prints the 3x3 tic-tac-toe board with a more detailed design."""
    print("\n")
    print("╔═══╦═══╦═══╗")
    print(f"║ {board[0]} ║ {board[1]} ║ {board[2]} ║")
    print("╠═══╬═══╬═══╣")
    print(f"║ {board[3]} ║ {board[4]} ║ {board[5]} ║")
    print("╠═══╬═══╬═══╣")
    print(f"║ {board[6]} ║ {board[7]} ║ {board[8]} ║")
    print("╚═══╩═══╩═══╝")
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
            prompt = f"PLAYER {player}'s TURN | Enter a number (1-9) > "
            move_str = input(prompt)
            move = int(move_str)
            if 1 <= move <= 9:
                if board[move - 1].isdigit():
                    return move - 1
                else:
                    print("🚫 That spot is already taken! Try another one.")
            else:
                print("⚠️  Invalid number. Please enter a number between 1 and 9.")
        except ValueError:
            print("⚠️  Invalid input. Please enter a number.")

def power(a, b):
    """Calculates the power of a number."""
    return a ** b

def main():
    """Main function to run the Tic Tac Toe game loop."""
    board = [str(i) for i in range(1, 10)]
    current_player = "X"
    game_is_running = True

    print("\n**************************")
    print("* WELCOME TO TIC TAC TOE *")
    print("**************************\n")

    while game_is_running:
        print_board(board)
        
        move_index = get_player_move(board, current_player)
        board[move_index] = current_player

        if check_win(board, current_player):
            print_board(board)
            print("**************************")
            print("*       GAME OVER        *")
            win_message = f"PLAYER {current_player} WINS! 🎉"
            print(f"* {win_message:^22} *")
            print("**************************")
            game_is_running = False
        elif check_tie(board):
            print_board(board)
            print("**************************")
            print("*       GAME OVER        *")
            tie_message = "IT'S A TIE!"
            print(f"* {tie_message:^22} *")
            print("**************************")
            game_is_running = False
        else:
            # Switch to the other player
            current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    main()