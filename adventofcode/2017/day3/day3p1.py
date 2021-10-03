import numpy as np

input = 325489
print(np.sqrt(input))

edge = 1
max_square = edge**2

while input > max_square:
    edge += 2
    max_square = edge ** 2

print("Edge are", edge, "tiles long")
print("Ring before last has", (edge-2)**2, "tiles")
print("Outer ring is", edge**2 - (edge-2)**2, "tiles")
print("Of which on tile, is on", input - (edge-2)**2)

running_total = (edge-2)**2 + edge-1
print("Starting new spiral in bottom right and up, first edge has edge-1:", edge-1, "tiles, totalling", running_total, "tiles")
running_total += edge-1
print("Top right to top left gives", running_total)
running_total += edge-1
print("Top left to bottom left gives", running_total)
running_total += edge-1
print("Bottom left to bottom right gives", running_total, "which is equal to edge^2", edge**2)

print("Tile is thus in bottom edge")
bottom_left = (edge-2)**2 + (edge-1)*3
print("From bottom left to input square is: input", input, "- bottom_left", bottom_left, "=", input - bottom_left)
print("Maximum steps with this length edges would be equal to edge-1, hence", edge-1)
print("Since we are", input - bottom_left, "steps from corner, our steps are", edge - 1 - (input - bottom_left))
print("Answer:", edge - 1 - (input - bottom_left))
