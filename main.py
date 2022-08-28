from html import entities
from textual.app import App

from fft import FFT
from character import Character
from vector import Vec

from ui import FFTUI, Info

entities = [
    Character(Vec(0, 0), speed=2),
    Character(Vec(1, 1), speed=1)
]

game = FFT(10, 10, entities)

class Main(App):
    async def on_mount(self):
        widgets = [
            FFTUI(game),
            Info(game)
        ]
        await self.view.dock(*widgets, edge="top")

if __name__ == '__main__':
    main = Main(game)
    Main.run()
