# from machine import Pin
import random


def xy_to_index(x, y):
  if y % 2 != 0:
    index = y * 5 + (4 - x)
  else:
    index = y * 5 + x
  return index

def random_cell():
  x = random.randint(0, 4)
  y = random.randint(0, 4)
  return (x, y)

def get_direction():
  # up = Pin(11, Pin.IN, Pin.PULL_UP)
  # down = Pin(12, Pin.IN, Pin.PULL_UP)
  # left = Pin(13, Pin.IN, Pin.PULL_UP)
  # right = Pin(14, Pin.IN, Pin.PULL_UP)
  typed = input("move? ")
  keymap = {"z": "up", "s": "down", "q": "left", "d": "right"}
  return keymap.get(typed)


finish = random_cell()

karel = random_cell()
while karel == finish:
  karel = random_cell()


def move(karel,direction):
  direction = get_direction()
  moves = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
  x, y = karel
  dx, dy = moves[direction]
  new_x = x + dx
  new_y = y + dy
  if 0 <= new_x <= 4 and 0 <= new_y <= 4:
    karel = (new_x, new_y)
  return karel


print(karel)