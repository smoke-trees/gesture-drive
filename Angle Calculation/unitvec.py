import numpy as np

def calc_unit_vector(l):
    all_v = []

    # from point i to j, so j-i
    for i in l:
        current_v = []
        for j in l:
            if i == None or j == None:
                unit_v = (None, None)
            else:
                magnitude = ((j[0] - i[0]) ** 2 + (j[1] - i[1]) ** 2)**(1/2)
                if magnitude == 0:
                    unit_v = (0, 0)
                else:
                    unit_v = ((j[0] - i[0]) / magnitude, (j[1] - i[1]) / magnitude)
            current_v.append(unit_v)
        all_v.append(current_v)
    # print(all_v, len(all_v))
    return all_v