from settings import *
from scripts.Board import Board
from scripts.Brick import Brick
from scripts.Block import Block

class Tetris:
    def __init__(self, sounds):
        self.sounds = sounds
        self.board = Board(rows=22, cols=10).center_screen()
        self.shadow_block = Block()
        self.highest_score_path = "data\highest_score.txt"
        self.init_game()
        self.is_sound_on = True
        
    def init_game(self):
        # init brick
        self.next_brick = Brick()
        self.hold_brick = None
        self.init_brick()

        # init board
        self.board.init_grid()

        # init status
        self.is_game_over = False
        self.is_playing = False
        self.start = False
        self.is_hold = True

        # init ach
        self.level = 0
        self.score = 0
        self.lines = 0
        self.highest_score = self.get_highest_score()

        self.start_channel = pg.mixer.Channel(0)
        self.fall_channel = pg.mixer.Channel(1)
        self.clear_channel = pg.mixer.Channel(2)

    def init_brick(self):
        # swap next_brick and brick
        self.brick, self.next_brick  = self.next_brick, Brick()

        # set position on board
        width_center = (self.board.cols - self.brick.get_cols()) // 2
        self.brick.row, self.brick.col = 0, width_center

        # fall down
        self.is_fall_down_fast = False
        self.last_fall_down_time = pg.time.get_ticks()
        self.fall_down_nomal_interval = INIT_FALL_DOWN_INTERVAL
        
        # save brick
        self.is_move_down = False
        self.is_save_brick = False
        
    def events(self, e):
        if e.type == pg.KEYDOWN and e.key == pg.K_r:
            if not self.start:
                self.start = True
                self.play_sound_channel(self.start_channel, 'start')

            self.is_playing = not self.is_playing
            if self.is_game_over: self.init_game()
        
        if e.type == pg.KEYDOWN and e.key == pg.K_v:
            self.is_sound_on = not self.is_sound_on
            if not self.is_sound_on: pg.mixer.stop()

        if self.is_game_over: return
        if not self.is_playing: return

        self.on_fall_down_fast(e)
        self.on_move_x(e)
        self.on_rotate(e)
        self.on_teleport(e)
        self.on_hold(e)

    def update(self):
        if self.is_pause(): return

        self.handle_fall_down()

        if self.is_save_brick:
            self.is_hold = True
            self.board.save_brick(self.brick)
            self.board.clear_full_rows()
            self.check_game_over()
            
            if self.is_game_over: 
                self.check_highest_score()
            else:
                self.init_brick()
            
            self.play_sound('save')

            if self.board.full_rows:
                self.play_sound_channel(self.clear_channel, 'clear')

            if self.is_game_over:
                self.play_sound('gameover')
            
            self.update_ach()

    def render(self):
        self.board.render(self.brick, self.shadow_block, self.get_shadow_row())
    
    def on_fall_down_fast(self, e):
        if e.type == pg.KEYDOWN and e.key == pg.K_s:
            self.is_fall_down_fast = True
        if e.type == pg.KEYUP and e.key == pg.K_s:
            self.is_fall_down_fast = False
    
    def on_move_x(self, e):
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_a:
                self.play_sound('move')
                self.move("left")
            if e.key == pg.K_d:
                self.play_sound('move')
                self.move("right")
    
    def on_rotate(self, e):
        if e.type == pg.KEYDOWN and e.key == pg.K_w:
            self.play_sound('rotate')
            self.brick.rotate_right()
            if self.is_collide(): 
                self.brick.rotate_left()

    def on_teleport(self, e):
        if e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
            self.brick.row = self.get_shadow_row()
            self.is_save_brick = True
    
    def on_hold(self, e):
        if e.type == pg.KEYDOWN and e.key == pg.K_f:
            self.play_sound('rotate')
            if self.is_hold:
                self.handle_hold_brick_collision()
                if not self.hold_brick:
                    self.hold_current_brick()
                else:
                    self.swap_with_hold_brick()
                self.is_hold = False

    def is_pause(self):
        if self.is_playing and not self.is_game_over:
            self.board.border_color = BOARD_BORDER_COLOR_PLAY
        else:
            self.board.border_color = self.board.cell_bd_color
            return True
        
        return False

    def handle_fall_down(self):
        if self.is_fall_down(): 
            self.is_move_down = True
            self.move("down")
            
            if self.is_fall_down_fast:
                if not self.fall_channel.get_busy(): 
                    self.play_sound_channel(self.fall_channel, 'fall')

        self.is_move_down = False

    def check_game_over(self):
        if any(self.board.grid[1]):
            self.is_game_over = True

    def check_highest_score(self):
        if self.score > self.highest_score:
            self.set_highest_score(self.score)
    
    def update_ach(self):
        full_rows = len(self.board.full_rows)
        basic_point = [0, 100, 300, 600, 1200]

        self.score += int((1 + self.level * 0.5) * basic_point[full_rows])
        self.level = int(self.score // LEVEL_UP)
        self.lines += int(full_rows)
        self.fall_down_nomal_interval = max(MAX_FALL_DOWN_INTERVAL, INIT_FALL_DOWN_INTERVAL - self.level * 50)

        self.board.full_rows = []

    def is_fall_down(self):
        current_time = pg.time.get_ticks()

        fall_down_interval = [self.fall_down_nomal_interval / 1, self.fall_down_nomal_interval / 10][self.is_fall_down_fast]

        if current_time - self.last_fall_down_time >= fall_down_interval:
            self.last_fall_down_time = current_time
            return True
        
        return False

    def is_collide(self, shadow_row=None):
        for r_index, row in enumerate(self.brick.shape):
            for c_index, element in enumerate(row):
                if isinstance(element, Block):
                    block_row = self.brick.row + r_index
                    block_col = self.brick.col + c_index

                    if shadow_row: block_row = shadow_row + r_index

                    if self.is_out_of_bounds(block_row, block_col, bool(shadow_row)):
                        return True
                    
                    if self.is_occupied(block_row, block_col, bool(shadow_row)):
                        return True
        return False

    def is_out_of_bounds(self, row, col, is_shadow):
        if  col < 0 or col >= self.board.cols:
            return True

        if row >= self.board.rows:
            if not is_shadow: self.is_save_brick = True
            return True
        
        return False

    def is_occupied(self, row, col, is_shadow):
        if isinstance(self.board.grid[row][col], Block):
            if not is_shadow and self.is_move_down: 
                self.is_save_brick = True
            return True
        return False
    
    def move(self, direction):
        direction = {
            "left": {'row': 0, 'col': -1}, 
            "right": {'row': 0, 'col': 1}, 
            "down": {'row': 1, 'col': 0}
        }[direction]

        self.brick.row += direction['row']
        self.brick.col += direction['col']

        if self.is_collide():
            self.brick.col -= direction['col']
            self.brick.row -= direction['row']
    
    def handle_hold_brick_collision(self):
        if self.brick.col <= 0:
            self.brick.col = 0
        
        if self.brick.col + len(self.brick.shape[0]) >= self.board.cols:
            if not self.hold_brick:
                self.brick.col = self.board.cols - len(self.next_brick.shape[0])
            else:
                self.brick.col = self.board.cols - len(self.hold_brick.shape[0])

    def hold_current_brick(self):
        self.hold_brick = Brick(shape=self.brick.shape)
        self.brick.shape = self.next_brick.shape
        self.next_brick = Brick()

    def swap_with_hold_brick(self):
        self.hold_brick.shape, self.brick.shape = self.brick.shape, self.hold_brick.shape
    
    def get_shadow_row(self):
        row = self.brick.row

        while True:
            row += 1
            if self.is_collide(row):
                row -= 1
                return row
    
    def get_highest_score(self):
        try:
            with open(self.highest_score_path, "r") as file:
                content = file.read()
                return int(content)
        except FileNotFoundError:
            print("File not found.")
            return 0

    def set_highest_score(self, content):
        try:
            with open(self.highest_score_path, "w") as file:
                file.write(str(content))
        except Exception as e:
            print("Error:", e)
    
    def play_sound(self, sound):
        is_busy = self.start_channel.get_busy() or self.clear_channel.get_busy()

        if not is_busy:
            pg.mixer.stop()

        self.sounds[sound].play()

        if not self.is_sound_on: pg.mixer.stop()
    
    def play_sound_channel(self, channel, sound):
        channel.play(self.sounds[sound])
        if not self.is_sound_on: pg.mixer.stop()