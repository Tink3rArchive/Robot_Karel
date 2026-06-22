# Imports
from machine import Pin, I2S
import random
import neopixel
import time
import tm1637

# Hardware Setup
I2S_BCLK = Pin(18)
I2S_WS = Pin(19)
I2S_DIN = Pin(21)

display = tm1637.TM1637(clk=Pin(22), dio=Pin(23))

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

grid_pixel = Pin(16, Pin.OUT)
grid = neopixel.NeoPixel(grid_pixel, 25)

lonely_pixel = Pin(17, Pin.OUT) 
mode_light = neopixel.NeoPixel(lonely_pixel, 1)

# Constants
moves = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
mode_colour = {"easy" : (0, 255, 0), "inter" : (255, 255, 0), "hard" : (255, 0, 0)}
mode_text = {"easy" : "EASY", "inter" : "INTR", "hard" : "HARD"}
colour = {"red" : (255, 0, 0), "green" : (0, 255, 0), "blue" : (0, 0, 255), "white" : (10, 10, 10), "black" : (0, 0, 0)}
prev = {"up": 1, "down": 1, "left": 1, "right": 1}
map_select = {1 : "map1", 2 : "map2", 3 : "map3"}
colour_cycle = ["blue", "black", "green", "black", "red", "black"]


audio = I2S(
    0,
    sck=I2S_BCLK,
    ws=I2S_WS,
    sd=I2S_DIN,
    mode=I2S.TX, 
    bits=16,
    format=I2S.MONO,
    rate=44100,
    ibuf=20000,
  )

score = 0
state = "select"
deadline = time.ticks_ms()
prev_mode = ""


#Functions
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
  result = None
  for direction in moves:
    now = buttons[direction].value()
    if now == 0 and prev[direction] == 1:
      result = direction
    prev[direction] = now 
  return result

def move(karel,direction):
  x, y = karel
  nudge = moves.get(direction)
  if nudge is None:
    return karel
  dx, dy = nudge
  new_x = x + dx
  new_y = y + dy
  if 0 <= new_x <= 4 and 0 <= new_y <= 4:
    karel = (new_x, new_y)
    play_sound("step.wav")
  else:
    play_sound("bonk.wav")
  return karel

def draw(karel, finish):
  for y in range(5):
    for x in range(5):
      if (x, y) == karel:
        grid[xy_to_index(x, y)] = colour["blue"]
      elif (x, y) == finish:
        grid[xy_to_index(x, y)] = colour["green"]
      else:
        grid[xy_to_index(x, y)] = colour["white"]
  grid.write()
  
def victory():
  for name in colour_cycle:
    grid.fill(colour[name])
    grid.write()
    time.sleep_ms(500)

def mode_select():
  if switch["easy"].value() == 0 and switch["hard"].value() == 1:
    return "easy"
  elif switch["easy"].value() == 1 and switch["hard"].value() == 0:
    return "hard"
  else:
    return "inter"
  
def update_mode_light(mode):
  mode_light[0] = mode_colour[mode]
  mode_light.write()

def play_sound(filepath):
  wav = open(filepath, "rb")
  wav.seek(44)
  buf = bytearray(1024)
  while True:
    n = wav.readinto(buf)
    if n == 0:
      break
    audio.write(buf[:n])
  wav.close()

def update_display(mode):
  global prev_mode, deadline
  now = time.ticks_ms()
  if mode != prev_mode:
    deadline = time.ticks_add(now, 1000)
    prev_mode = mode
  if time.ticks_diff(now, deadline) < 0:
    display.show(mode_text[mode])
  else:
    display.number(score)

while True:
  mode = mode_select()
  update_mode_light(mode)
  update_display(mode)

  if state == "select":
    if buttons["start"].value() == 0:
      finish = random_cell()
      play_sound("plip.wav")
      karel = random_cell()
      while karel == finish:
        karel = random_cell()
      play_sound("plop.wav")
      state = "playing"

  elif state == "playing":
    direction = get_direction()
    karel = move(karel, direction)
    draw(karel, finish)
    if karel == finish: 
      state = "won"

  elif state == "won":
    play_sound("victory.wav")
    victory()
    score += 1
    state = "select"

  time.sleep_ms(20)

