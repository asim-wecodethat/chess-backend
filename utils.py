def convert_position(position):
    """Convert a position like 'e2' into board indices (row, col)."""
    col = ord(position[0].lower()) - ord("a")
    row = 8 - int(position[1])
    return row, col


def convert_position_to_uci(row, col):
    """Convert board indices (row, col) into UCI format (e.g., 'e2')."""
    return chr(col + ord("a")) + str(8 - row)
