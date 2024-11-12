import subprocess


class ChessPiece:
    """Represents a chess piece with color and type attributes."""

    def __init__(self, color, piece_type):
        self.color = color
        self.piece_type = piece_type
        self.has_moved = False

    def __repr__(self):
        return f"{self.color} {self.piece_type}"


class ChessBoard:
    """Class representing the chess board and managing gameplay with Stockfish."""

    DIFFICULTY_SETTINGS = {
        "beginner": {"skill_level": 3, "depth": 5},
        "intermediate": {"skill_level": 10, "depth": 10},
        "professional": {"skill_level": 15, "depth": 15},
        "top_star": {"skill_level": 20, "depth": 20},
    }

    def __init__(
        self,
        stockfish_path="C:/Users/muham/Desktop/stockfish/stockfish-windows-x86-64-avx2",
        difficulty="intermediate",
    ):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = "white"
        self.stockfish_path = stockfish_path
        self.difficulty = difficulty
        self.setup_board()
        self.stockfish_process = self.initialize_stockfish()
        self.configure_difficulty(difficulty)

    def initialize_stockfish(self):
        """Initialize the Stockfish chess engine process."""
        try:
            process = subprocess.Popen(
                [self.stockfish_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1,
            )
            # Send UCI command and wait for response
            process.stdin.write("uci\n")
            process.stdin.flush()
            while True:
                output = process.stdout.readline().strip()
                if "uciok" in output:
                    print("Stockfish initialized successfully!")
                    break
            return process
        except FileNotFoundError:
            raise Exception("Stockfish executable not found. Check your path.")

    def configure_difficulty(self, difficulty):
        """Configure Stockfish settings based on difficulty level."""
        if difficulty not in self.DIFFICULTY_SETTINGS:
            raise ValueError(
                f"Invalid difficulty level. Choose from: {list(self.DIFFICULTY_SETTINGS.keys())}"
            )

        settings = self.DIFFICULTY_SETTINGS[difficulty]

        # Configure Stockfish settings
        commands = [
            "setoption name Skill Level value {}".format(settings["skill_level"]),
            "setoption name UCI_LimitStrength value true",
        ]

        for command in commands:
            self.send_to_stockfish(command)

        self.search_depth = settings["depth"]
        print(f"Difficulty set to {difficulty}")
        print(f"Skill Level: {settings['skill_level']}")
        print(f"Search Depth: {settings['depth']}")

    def setup_board(self):
        """Set up the board with the initial positions of all pieces."""
        piece_order = [
            "rook",
            "knight",
            "bishop",
            "queen",
            "king",
            "bishop",
            "knight",
            "rook",
        ]
        for col in range(8):
            self.board[1][col] = ChessPiece("black", "pawn")
            self.board[0][col] = ChessPiece("black", piece_order[col])
            self.board[6][col] = ChessPiece("white", "pawn")
            self.board[7][col] = ChessPiece("white", piece_order[col])

    def is_valid_move(self, from_pos, to_pos, piece):
        """Validates the basic movement logic for each piece."""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        if not self.is_valid_position(to_row, to_col):
            return False

        target_piece = self.get_piece(to_row, to_col)
        if target_piece and target_piece.color == piece.color:
            return False

        if piece.piece_type == "pawn":
            direction = 1 if piece.color == "black" else -1
            if to_col == from_col:
                if to_row == from_row + direction:
                    return not target_piece  # Normal move
                if not piece.has_moved and to_row == from_row + 2 * direction:
                    return not target_piece  # First double move
            elif abs(to_col - from_col) == 1 and to_row == from_row + direction:
                return target_piece is not None  # Capture move
            return False
        elif piece.piece_type == "rook":
            return from_row == to_row or from_col == to_col
        elif piece.piece_type == "knight":
            return abs(from_row - to_row) * abs(from_col - to_col) == 2
        elif piece.piece_type == "bishop":
            return abs(from_row - to_row) == abs(from_col - to_col)
        elif piece.piece_type == "queen":
            return (from_row == to_row or from_col == to_col) or (
                abs(from_row - to_row) == abs(from_col - to_col)
            )
        elif piece.piece_type == "king":
            return max(abs(from_row - to_row), abs(from_col - to_col)) == 1

        return False

    def get_fen(self):
        """Convert the current board state to FEN notation for Stockfish."""
        fen_rows = []
        for row in self.board:
            empty_count = 0
            fen_row = ""
            for piece in row:
                if piece is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    symbol = (
                        piece.piece_type[0].lower()
                        if piece.color == "black"
                        else piece.piece_type[0].upper()
                    )
                    if piece.piece_type == "knight":
                        symbol = "n" if piece.color == "black" else "N"
                    fen_row += symbol
            if empty_count > 0:
                fen_row += str(empty_count)
            fen_rows.append(fen_row)

        turn = "w" if self.current_turn == "white" else "b"
        return f"{'/'.join(fen_rows)} {turn} KQkq - 0 1"

    def send_to_stockfish(self, command):
        """Send a command to Stockfish and get the response."""
        self.stockfish_process.stdin.write(f"{command}\n")
        self.stockfish_process.stdin.flush()

        if "go" in command:
            while True:
                output = self.stockfish_process.stdout.readline().strip()
                if output.startswith("bestmove"):
                    return output.split()[1]
        return ""

    def get_computer_move(self):
        """Get the best move from Stockfish based on current difficulty settings."""
        fen = self.get_fen()
        self.send_to_stockfish(f"position fen {fen}")
        best_move = self.send_to_stockfish(f"go depth {self.search_depth}")
        return best_move

    def make_computer_move(self):
        """Execute the computer's move."""
        move = self.get_computer_move()
        if move:
            from_pos = (8 - int(move[1]), ord(move[0]) - ord("a"))
            to_pos = (8 - int(move[3]), ord(move[2]) - ord("a"))

            success, message = self.make_move(from_pos, to_pos)
            if success:
                print(f"Computer moved from {move[:2]} to {move[2:]}")
                return True
            else:
                print(f"Computer move failed: {message}")
        return False

    def make_move(self, from_pos, to_pos):
        """Execute a move on the board."""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        if not (
            self.is_valid_position(from_row, from_col)
            and self.is_valid_position(to_row, to_col)
        ):
            return False, "Invalid position"

        piece = self.get_piece(from_row, from_col)
        if not piece:
            return False, "No piece at the starting position"
        if piece.color != self.current_turn:
            return False, f"It's {self.current_turn}'s turn"

        if self.is_valid_move(from_pos, to_pos, piece):
            # Execute the move
            self.board[to_row][to_col] = piece
            self.board[from_row][from_col] = None
            piece.has_moved = True
            self.current_turn = "black" if self.current_turn == "white" else "white"
            return True, "Move successful"
        return False, "Invalid move"

    def is_valid_position(self, row, col):
        """Check if a position is within the board bounds."""
        return 0 <= row < 8 and 0 <= col < 8

    def get_piece(self, row, col):
        """Get the piece at a specific position."""
        return self.board[row][col] if self.is_valid_position(row, col) else None

    def print_board(self):
        """Display the current board state."""
        piece_symbols = {
            "white": {
                "king": "♔",
                "queen": "♕",
                "rook": "♖",
                "bishop": "♗",
                "knight": "♘",
                "pawn": "♙",
            },
            "black": {
                "king": "♚",
                "queen": "♛",
                "rook": "♜",
                "bishop": "♝",
                "knight": "♞",
                "pawn": "♟",
            },
        }
        print("\n  a b c d e f g h")
        for row in range(8):
            print(f"{8 - row}", end=" ")
            for col in range(8):
                piece = self.board[row][col]
                symbol = piece_symbols[piece.color][piece.piece_type] if piece else "·"
                print(symbol, end=" ")
            print(f"{8 - row}")
        print("  a b c d e f g h\n")
