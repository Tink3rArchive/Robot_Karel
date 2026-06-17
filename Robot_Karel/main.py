# from machine import Pin
import random
import neopixel


buttons = {
  "select" : Pin(4, Pin.IN, Pin.PULL_UP),
  "start" : Pin(5, Pin.IN, Pin.PULL_UP),
  "up" : Pin(13, Pin.IN, Pin.PULL_UP),
  "down" : Pin(14, Pin.IN, Pin.PULL_UP),
  "left" : Pin(25, Pin.IN, Pin.PULL_UP),
  "right" : Pin(26, Pin.IN, Pin.PULL_UP),
}

switch = {
  "easy" : Pin(32, Pin.IN, Pin.PULL_UP),
  "hard" : Pin(33, Pin.IN, Pin.PULL_UP),
}

# Neopixel Grid
grid_pixel = Pin(16, Pin.OUT)
grid = neopixel.NeoPixel(grid_pixel, 25)

# Lonely Neopixel
lonely_pixel = Pin(17, Pin.OUT)
mode_light = neopixel.NeoPixel(lonely_pixel, 1)


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

def mode_select():
  if switch["easy"].value() == 0 and switch["hard"].value() == 1:
    return "easy"
  elif switch["easy"].value() == 1 and switch["hard"].value() == 0:
    return "hard"
  else:
    return "inter"

finish = random_cell()

karel = random_cell()
while karel == finish:
  karel = random_cell()

draw(karel, finish)
while karel != finish:
  karel = move(karel, get_direction())
  draw(karel, finish)

print("Karel made it!")