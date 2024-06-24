from typing import Optional, Any
import tkinter as tk


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
    pass


def draw_table(table: list[list[Any]], accents: Optional[set[Any]] = None) -> None:
    """
    draws the whole table from the list of cells
    :param table: The table to draw
    :param accents: set of cells to draw accentuated
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


if __name__ == '__main__':
    pass
