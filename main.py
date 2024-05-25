from random import randint, choice
import laby_gen_graphics as graphics
from time import sleep

draw_intermediate = True
path = None
ACCENT_COLOR = (255, 0, 0)

directions_to_coordinates = {
    "up": (0, -1),
    "left": (-1, 0),
    "down": (0, 1),
    "right": (1, 0)
}


class PathError(Exception):
    def __init__(self, arg=""):
        super().__init__(arg)


class cell():
    def __init__(self, coords=(0, 0), links=None):
        if links is None:
            self.links = set()
        else:
            self.links = links
        self.coords = coords

    def link_to(self, other):
        self.links.add(other)
        other.links.add(self)

    def get_nearby(self):
        rt = {"up": False,
              "left": False,
              "down": False,
              "right": False}
        for elem in self.links:
            if change_pos(elem.coords, (0, 1)) == self.coords:
                rt["up"] = True
            elif change_pos(elem.coords, (1, 0)) == self.coords:
                rt["left"] = True
            elif change_pos(elem.coords, (0, -1)) == self.coords:
                rt["down"] = True
            elif change_pos(elem.coords, (-1, 0)) == self.coords:
                rt["right"] = True

        return rt


def change_pos(position, diff):
    if len(position) != len(diff):
        raise IndexError("pos and diff are not the same len!")
    rt = []
    for i, pc in enumerate(position):
        rt.append(pc + diff[i])
    return tuple(rt)


def is_aligned(cell1, cell2):
    return cell1.coords[0] == cell2.coords[0] or cell1.coords[1] == cell2.coords[1]


def find_4th(table, cell1, cell2, cell3):
    pos1, pos2, pos3 = (cell1.coords, cell2.coords, cell3.coords)
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


def create_table(side=10):
    cell_table = []
    for x in range(side):
        cell_table.append([])
        for y in range(side):
            current = cell((x, y))
            cell_table[x].append(current)
    return cell_table


def to_set(table):
    set_out = set()
    for line in table:
        set_out = set_out.union(set(line))
    return set_out


def get_neighbours(table, cel):
    tmp = (change_pos(cel.coords, (0, 1)),
           change_pos(cel.coords, (1, 0)),
           change_pos(cel.coords, (0, -1)),
           change_pos(cel.coords, (-1, 0)))
    rtn = []
    for coord in tmp:
        if is_in_bounds(coord, table):
            rtn.append(table[coord[0]][coord[1]])
    return rtn


def is_in_bounds(pos, table):
    return pos[0] in range(len(table)) and pos[1] in range(len(table))


def is_in_end_space(table, elem, path):
    checked = set(path)
    target = table[-1][-1]
    todo = set((elem,))
    while len(todo) > 0:
        current = todo.pop()
        checked.add(current)
        if current == target:
            return True
        nbrs = get_neighbours(table, current)
        for nb in nbrs:
            if nb not in checked:
                todo.add(nb)
    return False


def get_authorized(table, path):
    current = path[-1]
    nxt = [change_pos(current.coords, (0, 1)),
           change_pos(current.coords, (1, 0)),
           change_pos(current.coords, (0, -1)),
           change_pos(current.coords, (-1, 0))]
    i = 0
    while i < len(nxt):
        if is_in_bounds(nxt[i], table) and table[nxt[i][0]][nxt[i][1]] not in path:
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
    if path[-1].coords == (len(table) - 1, len(table) - 1):
        return path
    auth_lst = []
    for elem in auth_lst_tpl:
        auth_lst.append(table[elem[0]][elem[1]])
    first = True
    while 1:
        if len(auth_lst) == 0:
            if draw_intermediate:
                graphics.draw_cell(path[-1].coords, )
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


def get_all_linked_near_unlinked(table):
    returns = set()
    done = set()
    todo = set((table[0][0],))
    while len(todo) > 0:
        current = todo.pop()
        done.add(current)
        for nb in get_neighbours(table, current):
            if len(nb.links) == 0:
                returns.add(current)
                if draw_intermediate:
                    graphics.draw_cell(current.coords, ACCENT_COLOR)
            elif nb not in done:
                todo.add(nb)
    return returns


def randomize(lst):
    nu = []
    lst = lst.copy()
    while len(lst) > 0:
        elem = choice(lst)
        lst.remove(elem)
        nu.append(elem)
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
                            break


def link_path(table, path):
    for i in range(len(path) - 1):
        path[i].link_to(path[i + 1])


class ChallengeLaby:
    def __init__(self, side: int = 10, dri: bool = False):
        global draw_intermediate
        draw_intermediate = dri
        self._table = create_table(side)
        self._path = full_recursive_path_creation(self._table)
        link_path(self._table, self._path)
        if dri:
            graphics.draw_table(self._table)
        create_ramifications(self._table)
        self.start = self._table[0][0]
        self.end = self._path[-1]
        graphics.draw_table(self._table)


class LabySolverAPI(ChallengeLaby):
    def __init__(self, side: int = 10, dri: bool = False, log: bool = False):
        super().__init__(side, dri)
        self.position = self.start.coords
        self.compute_near()
        self.log = log

    def win(self):
        graphics.display_victory()
        # TODO Log

    def compute_near(self):
        self.near = self._table[self.position[0]][self.position[1]].get_nearby()

    def compute_win(self):
        return self.position == self.end.coords

    def move(self, direction: str):
        if direction not in ("up", "left", "down", "right"):
            raise NameError("Invalid direction")
        if direction not in self.near:
            if draw_intermediate:
                graphics.draw_wrong()  # TODO
                sleep(.5)
                draw_table(self._table)
                draw_cell(self.position, ACCENT_COLOR)
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
    A = LabySolverAPI(12, True)
