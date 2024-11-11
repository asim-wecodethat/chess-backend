from board_setup import ChessBoard
from utils import convert_position


def main():
    game = ChessBoard()
    while True:
        game.print_board()
        print(f"\nCurrent turn: {game.current_turn.capitalize()}")

        move_from = input(
            "Enter the piece position to move (e.g., 'e2') or 'quit' to exit: "
        )
        if move_from.lower() == "quit":
            break

        move_to = input("Enter the target position (e.g., 'e4') or 'quit' to exit: ")
        if move_to.lower() == "quit":
            break

        from_pos = convert_position(move_from)
        to_pos = convert_position(move_to)

        success, message = game.make_move(from_pos, to_pos)
        print(message)


if __name__ == "__main__":
    main()
