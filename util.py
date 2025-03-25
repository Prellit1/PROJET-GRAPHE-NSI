def distance(xy: tuple, xy2: tuple):
    distance2 = 0
    for id in range(len(xy)):
        distance2 += (xy[id] - xy2[id])**2
    #print(distance2**0.5, xy, xy2)
    return distance2