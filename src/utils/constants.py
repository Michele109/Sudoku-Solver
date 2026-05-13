
# Supported grid sizes
SUPPORTED_GRID_SIZES = (9, 16)

def char_to_int(char: str):
    """ #tested
    Converts a character to its corresponding integer value for Sudoku.
    """
    if char == '0' or char == '.':
        return 0
    elif '1' <= char <= '9':
        return int(char)
    elif 'A' <= char <= 'G': # Assuming A=10, B=11, ..., G=16
        return ord(char) - ord('A') + 10
    return int(char)


def int_to_char(num: int):
    """ #tested
    Converts an integer value back to its character representation for Sudoku.
    """
    if num == 0:
        return '.'
    elif 1 <= num <= 9:
        return str(num)
    elif 10 <= num <= 16:
        return chr(num - 10 + ord('A'))
    return str(num)
