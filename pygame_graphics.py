from typing import Optional, Any
import pygame

BACKGROUND_COLOUR: pygame.color.Color = pygame.color.Color(4, 4, 4)
CELL_COLOUR: pygame.color.Color = pygame.color.Color(4, 255, 4)
ACCENT_COLOUR: pygame.color.Color = pygame.color.Color(255, 4, 4)
WALL_COLOUR: pygame.color.Color = pygame.color.Color(4, 4, 4)

cell_size: int = 10
wall_size: int = 4
wrong_cue_size = 20
init_done: bool = False
screen: Optional[pygame.surface]
clock: Optional[pygame.time.Clock]


def init(n_cells: int) -> None:
    global init_done, screen, clock
    size_x = n_cells * (cell_size + wall_size) + wall_size + wrong_cue_size
    size_y = n_cells * (cell_size + wall_size) + wall_size
    pygame.init()
    screen = pygame.display.set_mode((size_x, size_y))
    clock = pygame.time.Clock()
    init_done = True
    pygame.display.update()


def loop():
    while 1:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit(0)
        pygame.display.update()


def draw_bg() -> None:
    """
    draws the background on top of the image
    """
    screen.fill(BACKGROUND_COLOUR)
    pygame.display.update()


def draw_cell_links(cell: Any) -> None:
    for nb in cell.links:
        draw_path(cell.coordinates, nb.coordinates)


def draw_cell(pos: tuple[int, int], toggle_accent: bool = False) -> None:
    """
    draws the cell at position pos, in accent color if toggle accent else in normal colour
    pos is the tuple of table coordinates
    Not implemented on text version of the UI because not feasible with this input data
    and my limited terminal manipulation knowledge.
    :param pos: tuple of table positions, (x, y)
    :param toggle_accent: if True, uses accent color
    """
    pygame.draw.rect(screen, ACCENT_COLOUR if toggle_accent else CELL_COLOUR,
                     (pos[0] * (cell_size + wall_size) + wall_size,
                      pos[1] * (cell_size + wall_size) + wall_size,
                      cell_size, cell_size))
    pygame.display.update()


def draw_path(pos1: tuple[int, int], pos2: tuple[int, int]) -> None:
    """
    draws the path between pos1 and pos2, in table coordinates
    Not implemented on text version of the UI because not feasible with this input data
    and my limited terminal manipulation knowledge.
    :param pos1: position of the first Cell
    :param pos2: position of the second Cell
    """
    h, w = cell_size, cell_size
    if pos2[0] + pos2[1] < pos1[0] + pos1[1]:
        pos1, pos2 = pos2, pos1
    x = pos1[0] * (cell_size + wall_size) + wall_size
    y = pos1[1] * (cell_size + wall_size) + wall_size
    if pos1[0] == pos2[0]:
        w += wall_size
    else:
        h += wall_size
    pygame.draw.rect(screen, CELL_COLOUR, (x, y, h, w))
    pygame.display.update()


"""    diff = (pos1[0]-pos2[0], pos1[1]-pos2[1])
    if abs(diff[0]) + abs(diff[1]) != 1:
        raise Exception("wrong neighbours")
    if diff[0] == 0:
        x = pos1[0] * (cell_size + wall_size) + wall_size
        h = cell_size
        w = cell_size + wall_size
        if diff[1] > 0:
            y = pos2[1] * (cell_size + wall_size) + wall_size
        else:
            y = pos1[1] * (cell_size + wall_size) + wall_size
    else:
        y = pos1[1] * (cell_size + wall_size) + wall_size
        h = cell_size + wall_size
        w = cell_size
        if diff[0] > 0:
            x = pos2[0] * (cell_size + wall_size) + wall_size
        else:
            x = pos1[0] * (cell_size + wall_size) + wall_size
    pygame.draw.rect(screen, CELL_COLOUR, (x, y, w, h))
    pygame.display.update()
"""


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
    if not init_done:
        init(len(table))
    draw_bg()
    for x, line in enumerate(table):
        for y, cell in enumerate(line):
            pygame.display.update()
            if accents is None:
                draw_cell((x, y))
                draw_cell_links(cell)
            else:
                draw_cell((x, y), cell in accents)
                draw_cell_links(cell)
    pygame.display.update()


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
    init(30)
    draw_bg()
    test_table = [[0, ] * 30, ] * 30
    draw_table(test_table)
    draw_path((0, 0), (0, 1))
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        pygame.display.flip()
