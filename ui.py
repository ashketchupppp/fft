from typing import List

from textual.widget import Widget
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text

from fft import FFT
from character import Character

def pad_to_len(string, padlen, padchar = ' '):
    return string + (padchar * (len(string) - padlen))

def joinr(joinstr, rich_text_list):
    ''' Joins regular strings with a list of rich.text.Text objects '''
    final = Text('')
    for text in rich_text_list:
        final = final + Text(joinstr) + text
    return final

def str_insert_replace(target_str, repl_str, index = 1):
    # assumes that repl_str at index is not longer that target_str :(
    result = list(target_str)
    c = index
    for ch in repl_str:
        result[c] = ch
        c += 1
    return ''.join(result)

def create_tile_grid_slots(w, h):
    grid = []
    for y in range(h + 2):
        grid.append([])
        for x in range(w + 2):
            grid[y].append('   ')
    return grid

def add_coord_rows(grid_slots):
    for i in range(1, len(grid_slots[0])):
        grid_slots[0][i] = str_insert_replace(grid_slots[0][i], str(i - 1))
    for i in range(1, len(grid_slots)):
        grid_slots[i][0] = str_insert_replace(grid_slots[i][0], str(i - 1))
    return grid_slots

def add_tiles(grid_slots, tilemap):
    dx, dy = (1, 1)
    for y in range(len(tilemap)):
        for x in range(len(tilemap[y])):
            grid_slots[y + dy][x + dx] = str_insert_replace(grid_slots[y + dy][x + dx], tilemap[y][x])
    return grid_slots

def add_characters(grid_slots, entities: List[Character]):
    dx, dy = (1, 1)
    for e in entities:
        y, x = (dx + e.pos.y, dy + e.pos.x)
        # assume square grid here
        if y <= len(grid_slots) and x <= len(grid_slots):
            grid_slots[y][x] = str_insert_replace(grid_slots[y][x], 'o/')
    return grid_slots

def draw_map(fft: FFT):
    # create the grid "slots"
    grid_slots = create_tile_grid_slots(fft.map.h, fft.map.w)

    # modify the grid slots inplace with the coords/tiles/characters
    grid_slots = add_coord_rows(grid_slots)
    # grid_slots = add_tiles(grid_slots, fft.map)
    grid_slots = add_characters(grid_slots, fft.entities)

    # highlight current entity and its coordinates
    current_entity = fft.current_turns_entity()
    hy, hx = (current_entity.pos.y + 1, current_entity.pos.x + 1)
    grid_slots[hy][hx] = (grid_slots[hy][hx], 'bold magenta')
    grid_slots[0][hx] = (grid_slots[0][hx], 'bold magenta')
    grid_slots[hy][0] = (grid_slots[hy][0], 'bold magenta')

    # highlight 

    # highlight movement range
    # ╭────╮
    # │    │  
    # ╰────╯

    return grid_slots

class Map(Widget):
    def __init__(self, fft: FFT, *args):
        self.fft = fft
        super().__init__(args)

    def render(self):
        map_tile2d = draw_map(self.fft)
        return Panel(joinr('\n', [Text.assemble(*row) for row in map_tile2d]))

class Info(Widget):
    def __init__(self, fft: FFT, *args):
        self.fft = fft
        super().__init__(args)

    def render(self):
        current_entity = self.fft.current_turns_entity()
        info = [
            Panel(str(current_entity.pos)),
            Panel(f'hp: {current_entity.hp}'),
            *[Panel(action) for action in self.fft.available_actions(current_entity)]
        ]
        return Panel(Columns(info))
