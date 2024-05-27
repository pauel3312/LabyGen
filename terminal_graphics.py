from typing import Optional, Any

CHAR_CELL = "\u25A1"
CHAR_ACCENT_CELL = "\u2716"
CHAR_HORIZONTAL_PATH = "\u2550"
CHAR_VERTICAL_PATH = "\u2016"


def draw_bg() -> None:
    """
    draws the background on top of the image
    """
    pass


def draw_cell(pos: tuple[int, int], toggle_accent: bool = False) -> None:
    """
    draws the cell at position pos, in accent color if toggle accent else in normal colour
    pos is the tuple of table coordinates
    Not implemented on text version of the UI because not feasible with this input data
    and my limited terminal manipulation knowledge.
    :param pos: tuple of table positions, (x, y)
    :param toggle_accent: if True, uses accent color
    """
    pass


def draw_path(pos1: tuple[int, int], pos2: tuple[int, int]) -> None:
    """
    draws the path between pos1 and pos2, in table coordinates
    Not implemented on text version of the UI because not feasible with this input data
    and my limited terminal manipulation knowledge.
    :param pos1: position of the first Cell
    :param pos2: position of the second Cell
    """
    pass


def transpose(table: list[list[Any]]) -> list[list[Any]]:
    """
    Transposes a square table
    :param table: The table to transpose. will not be modified.
    :return: a new, transposed table
    """
    new = []
    for i in range(len(table[0])):
        new.append([])  # Screw mutable defaults man, I wanted this to be a one liner
    for line in table:
        for i, elem in enumerate(line):
            new[i].append(elem)
    return new


def draw_table(table: list[list[Any]], accents: Optional[set[Any]] = None) -> None:
    """
    draws the whole table from the list of cells
    :param table: The table to draw
    :param accents: set of cells to draw accentuated
    """
    table = transpose(table)
    if accents is None:
        accents = set()
    for i, line in enumerate(table):
        for j, cell in enumerate(line):
            if cell in accents:
                print(CHAR_ACCENT_CELL, end="")
            else:
                print(CHAR_CELL, end="")
            if j != len(line) - 1 and line[1+j] in cell.links:
                print(CHAR_HORIZONTAL_PATH, end="")
            else:
                print(" ", end="")
        print()

        if line != table[-1]:
            for j, cell in enumerate(line):
                if table[i+1][j] in cell.links:
                    print(CHAR_VERTICAL_PATH, end="")
                else:
                    print(" ", end="")
                print(" ", end="")
        print()


def draw_wrong() -> None:
    """
    draws a "move wrong" cue
    """
    print("Move wrong!")


def un_draw_wrong() -> None:
    """
    removes the "move wrong" cue

    you can disable the "move wrong" cue by specifying a "wrong callback function"
    in the API constructor
    """
    print("\n")


def display_victory() -> None:
    """
    displays a victory screen ayd exits the script.
    """
    print("you won!")


if __name__ == '__main__':
    print(transpose([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
