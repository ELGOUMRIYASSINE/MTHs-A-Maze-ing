value = int("A", 16)
value = format(value, '04b')
print(value)
value = [int(x) for x in value]
west, south, east, north = value
print(west)
print(south)
print(east)
print(north)

