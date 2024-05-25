from random import randint, choice
import terminal_graphics as graphics
from time import sleep
from typing import Optional, Any, Callable

draw_intermediate = True
path: Optional[list["Cell"]] = None

directions_to_coordinates = {
    "up": (0, -1),
    "left": (-1, 0),
    "down": (0, 1),
    "right": (1, 0)
}


class PathError(Exception):
    def __init__(self, arg: str = ""):
        super().__init__(arg)


class Cell:
    """
    Cell class: defines a Cell that can be used for labyrinth creation, able to link itself to its neighbours.
    This is limited to 2D labyrinths with no diagonal movements.
    """
    def __init__(self, coordinates: tuple[int, int] = (0, 0), links: set["Cell"] = None) -> None:
        """
        Cell class builder
        :param coordinates: the coordinates of this cell. Expressed as a tuple (x, y)
        :param links: the set of cells this one is linked to upon creation. None by default.
        """
        if links is None:
            self.links = set()
        else:
            self.links: set["Cell"] = links
        self.coordinates: tuple[int, int] = coordinates

    def link_to(self, other: "Cell") -> None:
        """
        Links this Cell to another
        :param other: The Cell to link to
        :return: None
        """
        self.links.add(other)
        other.links.add(self)

    def get_nearby(self) -> dict[str:bool]:
        """
        Tells whether this Cell is linked to the one above, below, to the left and to the right of itself.
        :return: a dict, keys are "up", "left", "down", or "right", values are bools.
        """
        rt = {"up": False,
              "left": False,
              "down": False,
              "right": False}
        for elem in self.links:
            if change_pos(elem.coordinates, (0, 1)) == self.coordinates:
                rt["up"] = True
            elif change_pos(elem.coordinates, (1, 0)) == self.coordinates:
                rt["left"] = True
            elif change_pos(elem.coordinates, (0, -1)) == self.coordinates:
                rt["down"] = True
            elif change_pos(elem.coordinates, (-1, 0)) == self.coordinates:
                rt["right"] = True

        return rt


def change_pos(position: tuple[int, int], diff: tuple[int, int]) -> tuple[int, int]:
    """
    offsets position by diff
    :param position: the starting position, tuple (x, y)
    :param diff: position offset, tuple (x, y)
    :return: the offset position
    """
    return position[0] + diff[0], position[1] + diff[1]


def is_aligned(cell1: Cell, cell2: Cell) -> bool:
    """
    tells whether two cells are aligned or not
    :param cell1: first Cell
    :param cell2: second Cell
    :return: bool, True if cells are aligned, else False
    """
    return cell1.coordinates[0] == cell2.coordinates[0] or cell1.coordinates[1] == cell2.coordinates[1]


def find_4th(table: list[list[Cell]], cell1: Cell, cell2: Cell, cell3: Cell) -> Cell:
    """
    finds the fourth Cell in a square from the 3 other, regardless of what way they were entered in.
    :param table: The table containing all the cells
    :param cell1: first Cell of the square
    :param cell2: second Cell of the square
    :param cell3: third cell of the square
    :return: the 4th Cell object
    """
    pos1, pos2, pos3 = (cell1.coordinates, cell2.coordinates, cell3.coordinates)
    offset_12 = (pos1[0] - pos2[0], pos1[1] - pos2[1])
    offset_13 = (pos1[0] - pos3[0], pos1[1] - pos3[1])
    if 0 in offset_12:
        if 0 in offset_13:
            if offset_12[0] == 0:
                pos_rt = (pos3[0], pos2[1])
            else:
                pos_rt = (pos2[0], pos3[1])
        else:
            if offset_12[0] == 0:
                pos_rt = (pos3[0], pos1[1])
            else:
                pos_rt = (pos1[0], pos3[1])
    else:
        if 0 in offset_13:
            if offset_13[0] == 0:
                pos_rt = (pos2[0], pos1[1])
            else:
                pos_rt = (pos1[0], pos2[1])
        else:
            raise Exception("Impossible square!")

    cell_rt = table[pos_rt[0]][pos_rt[1]]
    return cell_rt


def create_table(side: int = 10) -> list[list[Cell]]:
    """
    Creates a square table, containing cells, with the right coordinates.
    :param side: The length and width of the table
    :return: a Table containing Cell objects
    """
    cell_table: list[list[Cell]] = []
    for x in range(side):
        cell_table.append([])
        for y in range(side):
            current = Cell((x, y))
            cell_table[x].append(current)
    return cell_table


def get_neighbours(table: list[list[Cell]], cel: Cell) -> list[Cell]:
    """
    From an initial cell, gets all the neighbouring ones.
    :param table: Table containing all Cells
    :param cel: the initial Cell
    :return: a list of the neighbouring Cells
    """
    tmp = (change_pos(cel.coordinates, (0, 1)),
           change_pos(cel.coordinates, (1, 0)),
           change_pos(cel.coordinates, (0, -1)),
           change_pos(cel.coordinates, (-1, 0)))
    rtn = []
    for coord in tmp:
        if is_in_bounds(coord, table):
            rtn.append(table[coord[0]][coord[1]])
    return rtn


def is_in_bounds(pos: tuple[int, int], table: list[list[Any]]) -> bool:
    """
    bounds check for table coordinates
    :param pos: tuple (x, y) of coordinates to check
    :param table: table to check bounds for
    :return: bool, True if in bounds.
    """
    return pos[0] in range(len(table)) and pos[1] in range(len(table))


def is_in_end_space(table: list[list[Cell]], elem: Cell, primary_path: list[Cell]) -> bool:
    """
    checks whether a Cell can reach the coordinates [-1, -1] in the table, without passing through the Path
    :param table: the table in which we need to check
    :param elem: the starting Cell
    :param primary_path: the Path not to be crossed
    :return: bool, True if the Cell can reach the coordinates.
    """
    checked: set[Cell] = set(primary_path)
    target: Cell = table[-1][-1]
    todo: set[Cell] = {(elem,)}
    while len(todo) > 0:
        current: Cell = todo.pop()
        checked.add(current)
        if current == target:
            return True
        neighbours: list[Cell] = get_neighbours(table, current)
        for nb in neighbours:
            if nb not in checked:
                todo.add(nb)
    return False


def get_authorized(table: list[list[Cell]], primary_path: list[Cell]) -> list[tuple[int, int]]:
    """
    gets all the positions a Cell can be linked to next
    :param table: the table in which to check
    :param primary_path: the Path not to be crossed
    :return: the list of available next moves
    """
    current: Cell = primary_path[-1]
    nxt: list[tuple[int, int]] = [change_pos(current.coordinates, (0, 1)),
                                  change_pos(current.coordinates, (1, 0)),
                                  change_pos(current.coordinates, (0, -1)),
                                  change_pos(current.coordinates, (-1, 0))]
    i = 0
    while i < len(nxt):
        if is_in_bounds(nxt[i], table) and table[nxt[i][0]][nxt[i][1]] not in primary_path:
            i += 1
            continue
        else:
            nxt.pop(i)
    return nxt


def full_recursive_path_creation(table: list[list[Cell]]) -> list[Cell]:
    """
    recursively creates a Path for the labyrinth.
    :param table: The starting table in which this creates the path
    :return: list of Cells constituting the Path
    """
    global path
    path: list[Cell] = [table[0][0], ] if path is None else path
    auth_lst_tpl: list[tuple[int, int]] = get_authorized(table, path)
    if path[-1].coordinates == (len(table) - 1, len(table) - 1):
        return path
    auth_lst = []
    for elem in auth_lst_tpl:
        auth_lst.append(table[elem[0]][elem[1]])
    first = True
    while 1:
        if len(auth_lst) == 0:
            if draw_intermediate:
                graphics.draw_cell(path[-1].coordinates, )
            path.pop(-1)
            raise PathError("Path impossible!")
        else:
            if first and len(auth_lst) == 2:
                if is_aligned(auth_lst[0], auth_lst[1]) or \
                   find_4th(table, auth_lst[0], auth_lst[1], path[-1]) in path:
                    if is_in_end_space(table, auth_lst[0], path):
                        current: Cell = auth_lst[0]
                    else:
                        current: Cell = auth_lst[1]
                else:
                    first = False
                    current: Cell = choice(auth_lst)
            else:
                first = False
                current: Cell = choice(auth_lst)
            auth_lst.remove(current)
            if draw_intermediate:
                graphics.draw_cell(current.coordinates, True)
            try:
                path.append(current)
                full_recursive_path_creation(table)
            except PathError:
                continue
            return path


def randomize(lst: list[Any]) -> list[Any]:
    """
    randomizes a list of objects
    :param lst: list to randomize
    :return: randomized list
    """
    nu: list[Any] = []
    lst = lst.copy()
    while len(lst) > 0:
        nu.append(lst.pop(randint(0, len(lst) - 1)))
    return nu


def create_ramifications(table: list[list[Cell]]) -> None:
    """
    creates ramifications for the labyrinth, links directly the Cells of the given table to one another.
    :param table: Input table, with pre-linked initial path.
    :return: None.
    """
    empty_left = True
    while empty_left:
        empty_left = False
        for line in randomize(table):
            for cel in randomize(line):
                if len(cel.links) == 0:
                    empty_left = True
                    for nb in randomize(get_neighbours(table, cel)):
                        if len(nb.links) != 0:
                            cel.link_to(nb)
                            if draw_intermediate:
                                graphics.draw_path(cel.coordinates, nb.coordinates)
                            break


def link_path(primary_path: list[Cell]) -> None:
    """
    links the elements of a Path list to one another
    :param primary_path: the path to link
    :return: None.
    """
    for i in range(len(primary_path) - 1):
        primary_path[i].link_to(primary_path[i + 1])


class ChallengeLabyrinth:
    """
    labyrinth class. Creates a labyrinth.
    """
    def __init__(self, side: int = 10, dri: bool = False):
        """
        Labyrinth class builder
        :param side: length of the labyrinth
        :param dri: defines whether the labyrinth building process shall be drawn.
        """
        global draw_intermediate
        draw_intermediate: bool = dri
        self._table: list[list[Cell]] = create_table(side)
        self._path: list[Cell] = full_recursive_path_creation(self._table)
        link_path(self._path)
        if dri:
            graphics.draw_table(self._table)
        create_ramifications(self._table)
        self.start: Cell = self._table[0][0]
        self.end: Cell = self._path[-1]
        graphics.draw_table(self._table)


class LabyrinthSolverAPI(ChallengeLabyrinth):
    """
    Exposes a ChallengeLabyrinth to another program, giving the ability to move a cursor through the labyrinth and
    to get the directions this cell is linked in.
    """
    def __init__(self, side: int = 10,
                 dri: bool = False,
                 drm: bool = False,
                 log: bool = False,
                 wrong_callback: Optional[Callable] = None):
        """
        API class builder
        :param side: the length and width of the labyrinth
        :param dri: defines whether the labyrinth building process shall be drawn.
        :param drm: defines whether the labyrinth solving process shall be drawn
        :param log: defines whether the solving process will be logged. TODO
        :param wrong_callback: function callback for wrong move.
        if set to none and drm is False, this will trigger a display warning.
        """
        super().__init__(side, dri)
        graphics.draw_bg()
        self.draw_movements: bool = drm
        self.position: tuple[int, int] = self.start.coordinates
        self.near: dict[str:bool] = {}
        self.compute_near()
        self.wrong_callback = wrong_callback
        self.log = log
        graphics.draw_cell(self.position, True)

    @staticmethod
    def win() -> None:
        """
        displays a victory screen and exits
        :return: None
        """
        graphics.display_victory()
        exit(0)

    def compute_near(self) -> None:
        """
        Computes nearby cells
        :return: None
        """
        self.near = self._table[self.position[0]][self.position[1]].get_nearby()

    def compute_win(self) -> bool:
        """
        Computes whether the algorithm has solved the labyrinth
        :return: bool, True if labyrinth is solved
        """
        return self.position == self.end.coordinates

    def move(self, direction: str) -> bool:
        """
        Moves the cursor in the specified direction
        :param direction: The direction to move in. "up", "left", "down", or "right"
        :return: True if movement was successful, else False.
        """
        if self.wrong_callback is None:
            wait = True
        else:
            wait = False
        if self.draw_movements:
            graphics.draw_cell(self.position)
        if direction not in ("up", "left", "down", "right"):
            raise NameError("Invalid direction")
        if self.near[direction] is False:
            if self.draw_movements:
                graphics.draw_cell(self.position, True)
                if wait:
                    graphics.draw_wrong()
                    sleep(.5)
                    graphics.un_draw_wrong()
                else:
                    self.wrong_callback()
            return False
        else:
            self.position = change_pos(self.position, directions_to_coordinates[direction])
            self.compute_near()
            if self.draw_movements:
                graphics.draw_cell(self.position, True)
            if self.compute_win():
                self.win()
            return True


if __name__ == "__main__":
    Labyrinth = LabyrinthSolverAPI(12, True)
