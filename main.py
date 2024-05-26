from settings import *
from scripts.Tetris import Tetris
from scripts.Info import Info
import asyncio

class Game:  
    def __init__(self):
        pg.init()
        pg.mixer.init()
        pg.display.set_caption("Tetris Game")

        self.sounds = self.load_sounds('sounds')
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.tetris = Tetris(self.sounds)
        self.info = Info(self.tetris)

    async def run(self):
        while True:
            self.events()  
            self.update()    
            self.render()         
            self.flip()
            await asyncio.sleep(0)

    def events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            self.tetris.events(e)

    def update(self):
        self.tetris.update()

    def render(self):
        self.screen.fill(BG_COLOR)
        self.tetris.render()
        self.info.render()

    def flip(self):
        pg.display.flip()
        self.clock.tick(FPS)
    

    def load_sounds(self, directory):
        sounds = {}
        for filename in os.listdir(directory):
            path = os.path.join(directory, filename)
            sound_name = os.path.splitext(filename)[0]
            sounds[sound_name] = pg.mixer.Sound(path)
        return sounds

if __name__ == "__main__":
    asyncio.run(Game().run())