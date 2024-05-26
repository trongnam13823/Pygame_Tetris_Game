from settings import *
from scripts.Block import Block
from scripts.Brick import Brick

class Board:
    def __init__(self, rows, cols, size=BLOCK_SIZE, left=0, top=0):
        self.rows = rows
        self.cols = cols
        self.size = size

        self.cell_bg_color = (240, 240, 240)
        self.cell_bd_color = (210, 210, 210)
        self.border_color = self.cell_bd_color
        self.border_width = 10

        self.rect = pg.Rect(left, top, cols * size, rows * size)
        self.init_grid()
        

    def init_grid(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.full_rows = []
    
    def render(self, brick=None, shadow_block=None, shadow_row=None):
        self.draw_grid()
        self.draw_border()

        if isinstance(brick, Brick): 
            self.draw_brick(brick, brick.row, brick.col)

        if shadow_block and shadow_row:
            self.draw_shape(brick.shape, shadow_block, shadow_row, brick.col)
    
    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                left = self.rect.left + col * self.size
                top = self.rect.top + row * self.size
                
                if row < 2:
                    self.draw_cell(left, top, self.cell_bd_color)
                else:
                    self.draw_cell(left, top, self.cell_bg_color, self.cell_bd_color)

                self.draw_block(self.grid[row][col], row, col)

    def draw_border(self):
        width = self.border_width * 2
        pg.draw.rect(
            surface=pg.display.get_surface(),
            color=self.border_color,
            rect=self.rect.inflate(width, width),
            width=width // 2
        )                
    
    def center_screen(self):
        self.rect.center = pg.display.get_surface().get_rect().center
        return self
        
    def draw_cell(self, left, top, bg_color=None, border_color=None):
        if bg_color:
            pg.draw.rect(
                surface=pg.display.get_surface(),
                color=bg_color,
                rect=(left, top, self.size, self.size)
            )

        if border_color:
            pg.draw.rect(
                surface=pg.display.get_surface(),
                color=border_color,
                rect=(left, top, self.size, self.size),
                width=1
            )

    def draw_block(self, block, row, col):
        if isinstance(block, Block):
            left = self.rect.left + col * self.size
            top = self.rect.top + row * self.size
            block.rect.topleft = (left, top)
            block.render()

    def draw_brick(self, brick, row, col):
        if isinstance(brick, Brick):
            left = self.rect.left + col * self.size
            top = self.rect.top + row * self.size
            brick.rect.topleft = (left, top)
            brick.render()
    
    def draw_shape(self, shape, block, row, col):
        for r_index, row_shape in enumerate(shape):
            for c_index, element in enumerate(row_shape):
                if isinstance(element, Block):
                    self.draw_block(block, row + r_index, col + c_index)

    def save_brick(self, brick):
        if isinstance(brick, Brick):
            for r_index, row in enumerate(brick.shape):
                for c_index, element in enumerate(row):
                    if isinstance(element, Block):
                        element.bg_color[3] = 155
                        self.grid[brick.row + r_index][brick.col + c_index] = element
    
    def clear_full_rows(self):
        self.full_rows = []

        for r_index, row in enumerate(self.grid):
            if(all(row)): self.full_rows.append(r_index)

        for r_index in self.full_rows:
            self.grid.pop(r_index)
            self.grid.insert(0, [0 for _ in range(self.cols)])