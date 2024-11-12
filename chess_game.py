from board_setup import ChessBoard
from utils import convert_position  # noqa: F401


def select_difficulty():
    """Prompt user to select a difficulty level."""
    print("\nSelect difficulty level:")
    print("1. Beginner")
    print("2. Intermediate")
    print("3. Professional")
    print("4. Top Star")

    while True:
        try:
            choice = int(input("Enter your choice (1-4): "))
            if choice == 1:
                return "beginner"
            elif choice == 2:
                return "intermediate"
            elif choice == 3:
                return "professional"
            elif choice == 4:
                return "top_star"
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Please enter a valid number.")


def main():
    print("Welcome to Chess Game!")
    difficulty = select_difficulty()

    game = ChessBoard(
        stockfish_path="C:/Users/muham/Desktop/stockfish/stockfish-windows-x86-64-avx2",
        difficulty=difficulty,
    )

    print(f"\nGame started with {difficulty} difficulty!")
    print("White pieces: ♔ ♕ ♖ ♗ ♘ ♙")
    print("Black pieces: ♚ ♛ ♜ ♝ ♞ ♟")
    print("\nEnter moves in algebraic notation (e.g., 'e2' to 'e4')")

    while True:
        game.print_board()
        print(f"Current turn: {game.current_turn}")

        if game.current_turn == "white":
            try:
                move_from = input(
                    "Enter the piece position to move (e.g., 'e2') or 'quit' to exit: "
                )
                if move_from.lower() == "quit":
                    break

                move_to = input(
                    "Enter the target position (e.g., 'e4') or 'quit' to exit: "
                )
                if move_to.lower() == "quit":
                    break

                # Convert chess notation to board indices
                from_col = ord(move_from[0].lower()) - ord("a")
                from_row = 8 - int(move_from[1])
                to_col = ord(move_to[0].lower()) - ord("a")
                to_row = 8 - int(move_to[1])

                success, message = game.make_move(
                    (from_row, from_col), (to_row, to_col)
                )
                print(message)

                if not success:
                    continue

            except (IndexError, ValueError) as e:  # noqa: F841
                print("Invalid input format. Please use the format 'e2'.")
                continue

        else:
            # Computer's turn
            print("Computer is thinking...")
            if not game.make_computer_move():
                print("Computer failed to make a move.")
                break


if __name__ == "__main__":
    main()
