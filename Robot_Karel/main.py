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

def move(karel,direction):
  moves = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
  x, y = karel
  nudge = moves.get(direction)
  if nudge is None:
    return karel
  dx, dy = nudge
  new_x = x + dx
  new_y = y + dy
  if 0 <= new_x <= 4 and 0 <= new_y <= 4:
    karel = (new_x, new_y)
  return karel

def draw(karel, finish):
  for y in range(5):
    row = ""
    for x in range(5):
      if (x, y) == karel:
        row += "K"
      elif (x, y) == finish:
        row += "F"
      else:
        row += "."
    print(row)
  print()

finish = random_cell()

karel = random_cell()
while karel == finish:
  karel = random_cell()

draw(karel, finish)
while karel != finish:
  karel = move(karel, get_direction())
  draw(karel, finish)

print("Karel made it!")