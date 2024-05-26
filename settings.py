import pygame as pg, sys, random, os

FPS = 60

WIDTH = 640
HEIGHT = 600

BG_COLOR = (255, 255, 255)

BLOCK_SIZE = 24

BOARD_BORDER_COLOR_PLAY = (180, 180, 180)

LEVEL_UP = 2000
INIT_FALL_DOWN_INTERVAL = 1000
MAX_FALL_DOWN_INTERVAL = 150 

BRICKS = {
  'O': {
    'shape': [
      [1, 1],
      [1, 1],
    ],
    'color': [255, 215, 0, 255]  # Vàng đậm
  },

  'J': {
    'shape': [
      [1, 0, 0],
      [1, 1, 1],
      [0, 0, 0],
    ],
    'color': [0, 100, 255, 255]  # Xanh dương
  },

  'L': {
    'shape': [
      [0, 0, 1],
      [1, 1, 1],
      [0, 0, 0],
    ],
    'color': [255, 140, 0, 255]  # Cam sáng
  },

  'S': {
    'shape': [
      [0, 1, 1],
      [1, 1, 0],
      [0, 0, 0],
    ],
    'color': [50, 205, 50, 255]  # Xanh lá cây sáng
  },

  'Z': {
    'shape': [
      [1, 1, 0],
      [0, 1, 1],
      [0, 0, 0],
    ],
    'color': [255, 20, 60, 255]  # Đỏ tươi
  },

  'T': {
    'shape': [
      [0, 1, 0],
      [1, 1, 1],
      [0, 0, 0],
    ],
    'color': [200, 0, 255, 255]  # Tím sáng
  },

  'I': {
    'shape': [
      [0, 0, 0, 0],
      [1, 1, 1, 1],
      [0, 0, 0, 0],
      [0, 0, 0, 0],
    ],
    'color': [0, 255, 255, 255]  # Xanh ngọc bích
  },
}