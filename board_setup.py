class ChessPiece:
    def __init__(self, color, piece_type):
        self.color = color  # 'white' or 'black'
        self.piece_type = piece_type
        self.has_moved = False

    def __repr__(self):
        return f"{self.color} {self.piece_type}"


class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = "white"
        self.setup_board()

    def setup_board(self):
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

    def is_valid_position(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def get_piece(self, row, col):
        return self.board[row][col] if self.is_valid_position(row, col) else None

    def make_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        if not (
            self.is_valid_position(from_row, from_col)
            and self.is_valid_position(to_row, to_col)
        ):
            return False, "Invalid position"

        piece = self.get_piece(from_row, from_col)
        if not piece:
            return False, "No piece at starting position"
        if piece.color != self.current_turn:
            return False, f"It's {self.current_turn.capitalize()}'s turn"

        if self.is_valid_move(from_pos, to_pos, piece):
            self.board[to_row][to_col] = piece
            self.board[from_row][from_col] = None
            piece.has_moved = True
            self.switch_turn()
            return True, "Move successful"
        return False, "Invalid move"

    def switch_turn(self):
        self.current_turn = "black" if self.current_turn == "white" else "white"

    def is_valid_move(self, from_pos, to_pos, piece):
        """Validate move based on piece type"""
        move_validation = {
            "pawn": self._validate_pawn_move,
            "rook": self._validate_rook_move,
            "knight": self._validate_knight_move,
            "bishop": self._validate_bishop_move,
            "queen": self._validate_queen_move,
            "king": self._validate_king_move,
        }
        return move_validation.get(piece.piece_type, lambda *_: False)(
            from_pos, to_pos, piece
        )

    def _validate_pawn_move(self, from_pos, to_pos, piece):
        """Validate pawn moves"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        direction = -1 if piece.color == "white" else 1

        # Move forward by 1 square
        if to_col == from_col and to_row == from_row + direction:
            return self.get_piece(to_row, to_col) is None

        # Move forward by 2 squares on first move
        if (
            to_col == from_col
            and to_row == from_row + 2 * direction
            and not piece.has_moved
        ):
            return (
                self.get_piece(to_row, to_col) is None
                and self.get_piece(from_row + direction, from_col) is None
            )

        # Diagonal capture
        if abs(to_col - from_col) == 1 and to_row == from_row + direction:
            target_piece = self.get_piece(to_row, to_col)
            return target_piece is not None and target_piece.color != piece.color

        return False

    def _validate_rook_move(self, from_pos, to_pos, piece):
        """Validate rook moves"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        if from_row != to_row and from_col != to_col:
            return False

        # Check if the path is clear
        step_row = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        step_col = 0 if from_col == to_col else (1 if to_col > from_col else -1)

        row, col = from_row + step_row, from_col + step_col
        while row != to_row or col != to_col:
            if self.get_piece(row, col):
                return False
            row += step_row
            col += step_col

        return (
            self.get_piece(to_row, to_col) is None
            or self.get_piece(to_row, to_col).color != piece.color
        )

    def _validate_knight_move(self, from_pos, to_pos, piece):
        """Validate knight moves"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        if (abs(to_row - from_row), abs(to_col - from_col)) not in [(2, 1), (1, 2)]:
            return False
        target_piece = self.get_piece(to_row, to_col)
        return target_piece is None or target_piece.color != piece.color

    def _validate_bishop_move(self, from_pos, to_pos, piece):
        """Validate bishop moves"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        if abs(to_row - from_row) != abs(to_col - from_col):
            return False

        # Check if the path is clear
        step_row = 1 if to_row > from_row else -1
        step_col = 1 if to_col > from_col else -1

        row, col = from_row + step_row, from_col + step_col
        while row != to_row or col != to_col:
            if self.get_piece(row, col):
                return False
            row += step_row
            col += step_col

        return (
            self.get_piece(to_row, to_col) is None
            or self.get_piece(to_row, to_col).color != piece.color
        )

    def _validate_queen_move(self, from_pos, to_pos, piece):
        """Validate queen moves (combination of rook and bishop)"""
        return self._validate_rook_move(
            from_pos, to_pos, piece
        ) or self._validate_bishop_move(from_pos, to_pos, piece)

    def _validate_king_move(self, from_pos, to_pos, piece):
        """Validate king moves"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        if max(abs(to_row - from_row), abs(to_col - from_col)) > 1:
            return False

        # King can't move to a square occupied by a piece of the same color
        target_piece = self.get_piece(to_row, to_col)
        return target_piece is None or target_piece.color != piece.color

    def print_board(self):
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
        print("  a b c d e f g h")
        for row in range(8):
            print(f"{8 - row}", end=" ")
            for col in range(8):
                piece = self.board[row][col]
                symbol = piece_symbols[piece.color][piece.piece_type] if piece else "."
                print(symbol, end=" ")
            print(f"{8 - row}")
        print("  a b c d e f g h")
