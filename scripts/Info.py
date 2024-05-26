from settings import *
from scripts.Brick import Brick

class Info:
    def __init__(self, tetris):
        self.tetris = tetris
        self.font = 'font/PressStart2P.ttf'  
        self.screen = pg.display.get_surface()
        self.is_screen_guide = False
    
    def render(self):
        self.draw_next_area()
        self.draw_hold_area()
        self.draw_ach_area()

    def draw_next_area(self):
        board = self.tetris.board
        next_brick = self.tetris.next_brick
        
        self.draw_brick_area('NEXT', next_brick, board.rect.left, board.rect.top, 2, 4)

    def draw_hold_area(self):
        board = self.tetris.board
        hold_brick = self.tetris.hold_brick

        self.draw_brick_area('HOLD', hold_brick, board.rect.left, HEIGHT * 0.3, 4, 4)
    
    def draw_ach_area(self):
        left = self.tetris.board.rect.right + BLOCK_SIZE * 2
        top = self.tetris.board.rect.top

        texts_and_values = [
            ('LEVEL:', self.tetris.level),
            ('LINES:', self.tetris.lines),
            ('SCORE:', self.tetris.score),
            ('SPEED:', self.tetris.fall_down_nomal_interval),
            ('HIGHEST SCORE:', self.tetris.highest_score)
        ]

        for text, value in texts_and_values:
            text_size, text_color, value_color = 10, (120, 120, 120), (0, 0, 0)
            if text == 'HIGHEST SCORE:':
                text_size, text_color, value_color = 9, (0, 0, 0), (255, 100, 100)
                top += 50

            text_surface, text_rect = self.create_text(text, text_size, left, top, text_color)
            value_surface, value_rect = self.create_text(value, 20, left, text_rect.bottom + 10, value_color)

            self.screen.blit(text_surface, text_rect)
            self.screen.blit(value_surface, value_rect)
            top = value_rect.bottom + 50

    def draw_brick_area(self, title, brick, left, top, row, col):
        text_surface, text_rect = self.create_text(title, 20)
        area_rect = pg.Rect(0, 0, BLOCK_SIZE * (col + 0.5), BLOCK_SIZE * (row + 0.5))

        text_rect.top = top
        area_rect.top = text_rect.bottom + 6
        area_rect.right = left - BLOCK_SIZE * 2
        text_rect.right = area_rect.centerx + text_rect.width / 2

        self.screen.blit(text_surface, text_rect)
        pg.draw.rect(self.screen, (100, 100, 100), area_rect, 2)

        if isinstance(brick, Brick):
            new_shape = self.remove_zero_rows_and_columns(brick.shape)
            _brick = Brick(shape=new_shape)
            _brick.rect.center = area_rect.center
            _brick.render()
    
    def create_text(self, text, size, left=0, top=0, color=(0, 0, 0), font=None):
        if font is None:
            font = self.font

        font_object = pg.font.Font(font, size)
        text_surface = font_object.render(str(text), True, color)
        text_rect = text_surface.get_rect()
        text_rect.left = left
        text_rect.top = top

        return text_surface, text_rect

    def remove_zero_rows_and_columns(self, matrix):
        num_rows = len(matrix)
        num_cols = len(matrix[0])

        # Step 1: Find rows and columns containing only zeros
        not_zero_rows = set()
        not_zero_cols = set()
        
        for r_index, row in enumerate(matrix):
            if any(row):
                not_zero_rows.add(r_index)
        
        transpose_matrix = [list(row) for row in zip(*matrix)]
        for c_index, col in enumerate(transpose_matrix):
            if any(col):
                not_zero_cols.add(c_index)
                
        # Step 2: Build the new matrix
        new_matrix = []
        for i in range(num_rows):
            if i in not_zero_rows:
                new_row = []
                for j in range(num_cols):
                    if j in not_zero_cols:
                        new_row.append(matrix[i][j])
                if new_row: 
                    new_matrix.append(new_row)
        return new_matrix
