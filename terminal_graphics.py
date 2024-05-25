from typing import Any

bg_col = (0, 0, 0)
cell_col = (0, 255, 0)
accent_col = (255, 0, 0)

wall_width = 4
cell_size = 8
padding = 4


def draw_bg() -> None:
    """
    draws the background on top of the image
    """
    pass


def draw_cell(pos: tuple[int, int], toggle_accent: bool = False) -> None:
    """
    draws the cell at position pos, in accent color if toggle accent else in normal colour
    pos is the tuple of table coordinates
    :param pos: tuple of table positions, (x, y)
    :param toggle_accent: if True, uses accent color
    """
    pass


def draw_path(pos1: tuple[int, int], pos2: tuple[int, int]) -> None:
    """
    draws the path between pos1 and pos2, in table coordinates
    :param pos1: position of the first Cell
    :param pos2: position of the second Cell
    """


def draw_table(table: list[list[Any]]) -> None:
    """
    draws the whole table from the list of cells
    :param table:
    """
    pass


def draw_wrong() -> None:
    """
    draws a "move wrong" cue
    """
    pass


def un_draw_wrong() -> None:
    """
    removes the "move wrong" cue

    you can disable the "move wrong" cue by specifying a "wrong callback function"
    in the API constructor
    """
    pass


def display_victory() -> None:
    """
    displays a victory screen ayd exits the script.
    """
    pass
