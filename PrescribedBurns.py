
from checking_ignition import *
from running_model import *
from collections import defaultdict
def plan_burn(f_grid, h_grid, i_threshold, town_cell):
    ''' Work out the best cells to start a planned burn to protect the town
    '''
    w_list = ['N', 'E', 'S', 'W', 'NE', 'NW', 'SE', 'SW', None]
    # Dealing with the factor of 2 decrease:
    i_thresholda = i_threshold * 2
    size = len(f_grid)
    prescribed = []
    dd= defaultdict(int)
    # Find the cells where a fire can be started without burning the town
    for y in range(size):
        for x in range(size):
            if f_grid[y][x] > 0:
                if (y, x) != town_cell:
                    model = run_model(f_grid, h_grid, i_thresholda, None,
                                      [(y, x)])
                 
                    if model[0][town_cell[1]][town_cell[0]] == (
                                          f_grid[town_cell[1]][town_cell[0]]):
                        prescribed.append(((y, x), model))
    counter = 0
    # See how many simulations with winds and fires in other cells that the 
    # Town burns in
    for coords in prescribed:
        dd[coords[0]] = 0
        for directions in w_list:
            for y in range(size):
                for x in range(size):
                    if (y, x) not in coords[0]:
                        if f_grid[y][x] > 0:
                            if (y, x) != town_cell:
                                counter +=1
                                fuel = coords[1][0]
                                model = run_model(fuel, h_grid, i_threshold,
                                                  directions, [(y, x)])        
                                if model[0][town_cell[1]][town_cell[0]] == 0:
                                    dd[coords[0]] += 1 
   
    minimum = (size ** 2 - 2) * 9
    output = []
    # Work out the minimum value for most effective burning 
    for keys in dd:
        if dd[keys] < minimum:
            minimum = dd[keys]
            output = []
            output.append(keys)
        elif dd[keys] == minimum:
            output.append(keys)
    return output


print(plan_burn([[2, 2], [1, 2]], [[1, 2], [1, 2]], 2, (1, 1)))
