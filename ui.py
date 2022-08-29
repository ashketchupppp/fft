from vector import Vec
from textual.widget import Widget
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.console import Group

from fft import FFT

class FFTUI(Widget):
    def __init__(self, fft: FFT, *args):
        self.fft = fft
        super().__init__(args)

    def map_row(self, row_num):
        row = self.fft.map[row_num].copy()
        for x in range(len(row)):
            # draw entity if there is one
            if self.fft.entities[Vec(row_num, x)]:
                row[x] = 'o/'

            # otherwise just add a space to the tile string
            if len(row[x]) < 2:
                row[x] += ' '

            # stylise the current entity
            row[x] = Text(row[x])
            row[x].stylize("bold")
        row.insert(0, str(row_num) + ' ')
        return ''.join([str(i) for i in row])

    def render(self):
        rows = []
        topRowCoordinates = [str(x) for x in list(range(len(self.fft.map[0])))]
        rows.append('  ' + ' '.join(topRowCoordinates))
        for y in range(len(self.fft.map)):
            rows.append(self.map_row(y))
        return Panel('\n'.join(rows))

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
