# A 3D Array (2 Floors, 2 Apts, 2 Rooms)
building = [
    # Floor 0
    [
        [1, 2],  # Apt 0
        [3, 4]   # Apt 1 (Task: Fill this with 3 and 4)
    ],
    # Floor 1
    [
        [5, 6],  # Apt 0 (Task: Fill this with 5 and 6)
        [7, 8]   # Apt 1
    ]
]

for f in building:
    for a in f:
        for r in a:
            print(f"[{r}]", end = "")
# print(building[1][1][1])
