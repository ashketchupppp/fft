from textual.app import App
from textual.widget import Widget
from rich.panel import Panel
from rich.columns import Columns

from fft import FFT
from character import Character
from vector import Vec
from ui import FFTUI, Info

def run_model():
    def create_game():
        entities = [
            Character(Vec(1, 1), move_range=2),
            Character(Vec(5, 5), move_range=2)
        ]
        game = FFT(10, 10, entities)
        return game

    game = create_game()
    replay = []

    # set the game up to record all the game actions
    def record(func):
        def wrapper(*args):
            replay.append(args)
            func(*args)
        return wrapper
    
    game.take_turn = record(game.take_turn)

    # run the model here, interacting with the game
    for i in range(10):
        entity = game.current_turns_entity()
        try:
            game.take_turn('move', entity.pos + Vec(1, 1))
        except:
            pass

    return (create_game(), replay)

game, replay = run_model()

class UIWidget(Widget):
    def render(self):
        widgets = [
            FFTUI(game),
            Info(game)
        ]
        return Panel(Columns(widgets))

    async def on_mount(self):
        self.set_interval(0.2, self.refresh)

class UI(App):
    def take_turn(self):
        if not 'current_action' in vars(self):
            self.current_action = 0
        if not self.current_action >= len(replay):
            try:
                game.take_turn(*replay[self.current_action])
            except FFT.PositionOutsideMap:
                pass
            self.current_action += 1

    async def on_mount(self):
        self.set_interval(1, self.take_turn)
        await self.view.dock(UIWidget(game), edge="top")

ui = UI()
ui.run()
print(replay)