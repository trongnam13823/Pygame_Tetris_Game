from settings import *
from scripts.Block import Block

class Brick:
    def __init__(self, left=0, top=0, size=BLOCK_SIZE, shape=None):
        self.shape = shape or self.random_shape()
        self.rect = pg.Rect(left, top, self.get_cols() * size, self.get_rows() * size)

    def render(self):
        for r_index, row in enumerate(self.shape):
            for c_index, element in enumerate(row):
                if isinstance(element, Block): 
                    element.rect.top = self.rect.top + r_index * BLOCK_SIZE
                    element.rect.left = self.rect.left + c_index * BLOCK_SIZE
                    element.render()

    def random_shape(self):
        type = random.choice(list(BRICKS.keys()))
        shape = BRICKS[type]['shape'].copy()
        color = BRICKS[type]['color'].copy()

        for r_index, row in enumerate(shape):
            for c_index, element in enumerate(row):
                if not element: continue

                shape[r_index][c_index] = Block(color)

        return shape
    
    def get_cols(self):
        if self.shape is None: return 0
        return len(self.shape[0])
    
    def get_rows(self):
        if self.shape is None: return 0
        return len(self.shape)
    
    def rotate_left(self):
        self.shape = [list(row) for row in zip(*self.shape)][::-1]

    def rotate_right(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
