from typing import Optional, Any
import pygame
from time import sleep

BACKGROUND_COLOUR: pygame.color.Color = pygame.color.Color(4, 4, 4)
CELL_COLOUR: pygame.color.Color = pygame.color.Color(4, 255, 4)
ACCENT_COLOUR: pygame.color.Color = pygame.color.Color(255, 4, 4)
WALL_COLOUR: pygame.color.Color = pygame.color.Color(4, 4, 4)

cell_size: int = 12
wall_size: int = 3
wrong_cue_size = 60
init_done: bool = False
screen: Optional[pygame.Surface]


def translate(pt: tuple[int, int], matrix: tuple[int, int]) -> tuple[int, int]:
    return pt[0]+matrix[0], pt[1]+matrix[1]


WRONG_CROSS_SURFACE: pygame.surface = pygame.Surface((wrong_cue_size-wall_size, wrong_cue_size-wall_size))
WRONG_CROSS_RECT = WRONG_CROSS_SURFACE.get_rect()
wrong_cross_points: list[tuple[int, int]] = [WRONG_CROSS_RECT.topleft,
                                             translate(WRONG_CROSS_RECT.topleft,
                                                       (0, int((wrong_cue_size-wall_size)/6))),
                                             translate(WRONG_CROSS_RECT.midleft,
                                                       (int((wrong_cue_size-wall_size)/3), 0)),
                                             translate(WRONG_CROSS_RECT.bottomleft,
                                                       (0, -int((wrong_cue_size-wall_size)/6))),
                                             WRONG_CROSS_RECT.bottomleft,
                                             translate(WRONG_CROSS_RECT.bottomleft,
                                                       (int((wrong_cue_size-wall_size)/6), 0)),
                                             translate(WRONG_CROSS_RECT.midbottom,
                                                       (0, -int((wrong_cue_size-wall_size)/3))),
                                             translate(WRONG_CROSS_RECT.bottomright,
                                                       (-int((wrong_cue_size-wall_size)/6), 0)),
                                             WRONG_CROSS_RECT.bottomright,
                                             translate(WRONG_CROSS_RECT.bottomright,
                                                       (0, -int((wrong_cue_size-wall_size)/6))),
                                             translate(WRONG_CROSS_RECT.center,
                                                       (int((wrong_cue_size-wall_size)/6), 0)),
                                             translate(WRONG_CROSS_RECT.topright,
                                                       (0, int((wrong_cue_size-wall_size)/6))),
                                             WRONG_CROSS_RECT.topright,
                                             translate(WRONG_CROSS_RECT.topright,
                                                       (-int((wrong_cue_size-wall_size)/6), 0)),
                                             translate(WRONG_CROSS_RECT.center,
                                                       (0, -int((wrong_cue_size-wall_size)/6))),
                                             translate(WRONG_CROSS_RECT.topleft,
                                                       (int((wrong_cue_size-wall_size)/6), 0))]


def init(n_cells: int) -> None:
    global init_done, screen
    size_x = n_cells * (cell_size + wall_size) + wall_size + wrong_cue_size
    size_y = n_cells * (cell_size + wall_size) + wall_size
    pygame.init()
    screen = pygame.display.set_mode((size_x, size_y))
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


def draw_cell(pos: tuple[int, int], toggle_accent: bool = False, update_display: bool = True) -> None:
    """
    draws the cell at position pos, in accent color if toggle accent else in normal colour
    pos is the tuple of table coordinates
    Not implemented on text version of the UI because not feasible with this input data
    and my limited terminal manipulation knowledge.
    :param pos: tuple of table positions, (x, y)
    :param toggle_accent: if True, uses accent color
    :param update_display: Determines if the display should be updated after drawing
    """
    pygame.draw.rect(screen, ACCENT_COLOUR if toggle_accent else CELL_COLOUR,
                     (pos[0] * (cell_size + wall_size) + wall_size,
                      pos[1] * (cell_size + wall_size) + wall_size,
                      cell_size, cell_size))
    if update_display:
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
                draw_cell((x, y), update_display=False)
                draw_cell_links(cell)
            else:
                draw_cell((x, y), cell in accents, False)
                draw_cell_links(cell)
    pygame.display.update()


def draw_wrong() -> None:
    """
    draws a "move wrong" cue
    """
    pygame.draw.polygon(WRONG_CROSS_SURFACE, ACCENT_COLOUR, wrong_cross_points)
    screen.blit(WRONG_CROSS_SURFACE, translate(screen.get_rect().topright, (-wrong_cue_size, 0)))
    pygame.display.update()


def un_draw_wrong() -> None:
    """
    removes the "move wrong" cue

    you can disable the "move wrong" cue by specifying a "wrong callback function"
    in the API constructor
    """
    WRONG_CROSS_SURFACE.fill(BACKGROUND_COLOUR)
    screen.blit(WRONG_CROSS_SURFACE, translate(screen.get_rect().topright, (-wrong_cue_size, 0)))
    pygame.display.update()


def display_victory() -> None:
    """
    displays a victory screen ayd exits the script.
    """
    draw_bg()
    font = pygame.font.SysFont('Castellar', 48)
    txt = font.render('You won!', True, CELL_COLOUR)
    txt_rect = txt.get_rect()
    x = screen.get_rect().centerx-txt_rect.centerx
    y = screen.get_rect().centery-txt_rect.centery
    screen.blit(txt, (x, y))
    pygame.display.flip()

    sleep(3)
    exit(0)


if __name__ == '__main__':
    init(30)
    pygame.draw.polygon(WRONG_CROSS_SURFACE, ACCENT_COLOUR, wrong_cross_points)
    screen.blit(WRONG_CROSS_SURFACE, (0, 0))
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        pygame.display.flip()
