from settings import *

class Block:
    def __init__(self, bg_color=None, left=0, top=0, size=BLOCK_SIZE, bd_color="black", bd_width=2):
        self.bg_color = bg_color
        self.bd_color = bd_color
        self.bd_width = bd_width
        self.scale = -4
        
        self.surf = pg.Surface((size, size), pg.SRCALPHA)
        self.surf.fill((0, 0, 0, 0))
        self.surf.set_alpha(255)
        self.rect = self.surf.get_rect(topleft=(left, top))
    
    def render(self):
        rect = self.rect.inflate(self.scale, self.scale)
        rect.centerx = self.rect.centerx - self.rect.left
        rect.centery = self.rect.centery - self.rect.top
        if self.bg_color: pg.draw.rect(self.surf, self.bg_color, rect)
        if self.bd_color and self.bd_width: 
            pg.draw.rect(self.surf, self.bd_color, rect, self.bd_width)
        
        pg.display.get_surface().blit(self.surf, self.rect)