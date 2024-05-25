from random import randint, choice
import laby_gen_graphics as graphics
from time import sleep
from typing import Optional

draw_intermediate = True
path: Optional[list["Cell"]] = None
ACCENT_COLOR = (255, 0, 0)

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
    def __init__(self, coordinates: tuple[int, int] = (0, 0), links: set["Cell"] = None) -> None:
        if links is None:
            self.links = set()
        else:
            self.links: set["Cell"] = links
        self.coordinates: tuple[int, int] = coordinates

    def link_to(self, other: "Cell") -> None:
        self.links.add(other)
        other.links.add(self)

    def get_nearby(self) -> dict[str:bool]:
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
    return position[0] + diff[0], position[1] + diff[1]


def is_aligned(cell1: Cell, cell2: Cell) -> bool:
    return cell1.coordinates[0] == cell2.coordinates[0] or cell1.coordinates[1] == cell2.coordinates[1]


def find_4th(table: list[list[Cell]], cell1: Cell, cell2: Cell, cell3: Cell) -> Cell:
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
    cell_table: list[list[Cell]] = []
    for x in range(side):
        cell_table.append([])
        for y in range(side):
            current = Cell((x, y))
            cell_table[x].append(current)
    return cell_table

# TODO type hinting


def to_set(table):
    set_out = set()
    for line in table:
        set_out = set_out.union(set(line))
    return set_out


def get_neighbours(table, cel):
    tmp = (change_pos(cel.coordinates, (0, 1)),
           change_pos(cel.coordinates, (1, 0)),
           change_pos(cel.coordinates, (0, -1)),
           change_pos(cel.coordinates, (-1, 0)))
    rtn = []
    for coord in tmp:
        if is_in_bounds(coord, table):
            rtn.append(table[coord[0]][coord[1]])
    return rtn


def is_in_bounds(pos, table):
    return pos[0] in range(len(table)) and pos[1] in range(len(table))


def is_in_end_space(table, elem, primary_path: list[Cell]):
    checked: set[Cell] = set(primary_path)
    target: Cell = table[-1][-1]
    todo: set[Cell] = {(elem,)}
    while len(todo) > 0:
        current = todo.pop()
        checked.add(current)
        if current == target:
            return True
        neighbours = get_neighbours(table, current)
        for nb in neighbours:
            if nb not in checked:
                todo.add(nb)
    return False


def get_authorized(table, primary_path):
    current = primary_path[-1]
    nxt = [change_pos(current.coordinates, (0, 1)),
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


def has_unlinked_neighbours(table, cel):
    for nb in get_neighbours(table, cel):
        if len(nb.links) == 0:
            return True
    return False


def full_recursive_path_creation(table):
    global path
    path = [table[0][0], ] if path is None else path
    auth_lst_tpl = get_authorized(table, path)
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
                        current = auth_lst[0]
                    else:
                        current = auth_lst[1]
                else:
                    first = False
                    current = choice(auth_lst)
            else:
                first = False
                current = choice(auth_lst)
            auth_lst.remove(current)
            if draw_intermediate:
                graphics.draw_cell(current.coords, ACCENT_COLOR)
            try:
                path.append(current)
                full_recursive_path_creation(table)
            except PathError:
                continue
            return path


def randomize(lst):
    nu = []
    lst = lst.copy()
    while len(lst) > 0:
        nu.append(lst.pop(randint(0, len(lst) - 1)))
    return nu


def create_ramifications(table):
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


def link_path(primary_path):
    for i in range(len(primary_path) - 1):
        primary_path[i].link_to(primary_path[i + 1])


class ChallengeLabyrinth:
    def __init__(self, side: int = 10, dri: bool = False):
        global draw_intermediate
        draw_intermediate = dri
        self._table = create_table(side)
        self._path = full_recursive_path_creation(self._table)
        link_path(self._path)
        if dri:
            graphics.draw_table(self._table)
        create_ramifications(self._table)
        self.start = self._table[0][0]
        self.end = self._path[-1]
        graphics.draw_table(self._table)


class LabyrinthSolverAPI(ChallengeLabyrinth):
    def __init__(self, side: int = 10, dri: bool = False, log: bool = False):
        graphics.draw_bg()
        super().__init__(side, dri)
        self.position = self.start.coordinates
        self.near: dict[str:bool] = {}
        self.compute_near()
        self.log = log
        graphics.draw_cell(self.position, ACCENT_COLOR)

    @staticmethod
    def win():
        graphics.display_victory()
        # TODO Log, Timer, nb_cps
        exit(0)

    def compute_near(self):
        self.near = self._table[self.position[0]][self.position[1]].get_nearby()

    def compute_win(self):
        return self.position == self.end.coordinates

    def move(self, direction: str, wrong_callback: Optional[type(exit)] = None):
        if wrong_callback is None:
            wait = True
        else:
            wait = False
        graphics.draw_cell(self.position)
        if direction not in ("up", "left", "down", "right"):
            raise NameError("Invalid direction")
        if self.near[direction] is False:
            if draw_intermediate:
                graphics.draw_cell(self.position, ACCENT_COLOR)
                graphics.draw_wrong()
                if wait:
                    sleep(.5)
                else:
                    wrong_callback()
                graphics.undraw_wrong()
            return False
        else:
            self.position = change_pos(self.position, directions_to_coordinates[direction])
            self.compute_near()
            if draw_intermediate:
                graphics.draw_cell(self.position, ACCENT_COLOR)
            if self.compute_win():
                self.win()
            return True


if __name__ == "__main__":
    A = LabyrinthSolverAPI(12, True)
