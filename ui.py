from fft import FFT
from textual.widget import Widget
from rich.panel import Panel

class FFTUI(Widget):
    def __init__(self, fft: FFT, *args):
        self.fft = fft
        super().__init__(args)

    def render(self):
        return Panel(str(self.fft))

class Info(Widget):
    def __init__(self, fft: FFT, *args):
        self.fft = fft
        super().__init__(args)

    def render(self):
        return Panel(','.join(self.fft.available_actions(self.fft.current_turns_entity())))