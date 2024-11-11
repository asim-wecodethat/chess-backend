def convert_position(position):
    """Converts a position like 'e2' into board indices (row, col)."""
    col = ord(position[0].lower()) - ord("a")
    row = 8 - int(position[1])
    return row, col
