def xy_to_index(x, y):
  if y % 2 != 0:
    index = y * 5 + (4 - x)
  else:
    index = y * 5 + x


