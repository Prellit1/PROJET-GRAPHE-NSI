def distance(xy: tuple, xy2: tuple):
    distance = 0
    for id in range(len(xy)):
        distance += (xy[id] - xy2[id])**2
    return distance ** 0.5