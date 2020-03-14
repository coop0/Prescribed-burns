from checking_ignition import *
import copy

def nexttime(f_grid, h_grid, i_threshold, w_direction, b_grid,
             gridsize, count):    
    ''' Calculates b_grid and f_grid at the timestamp t+1
    '''
    nextb_grid = []
    # Create a new burning grid
    for a in range(gridsize):
        temp = []
        for b in range(gridsize):
            if b_grid[a][b]:
                temp.append(True)
            else:
                ignite = check_ignition(b_grid, f_grid, h_grid, i_threshold,
                                        w_direction, a, b)
                if ignite:
                    temp.append(True)
                else:
                    temp.append(False)
                
        nextb_grid.append(temp)
    # Take away the fuel from the burning cells of the last timestamp    
    for i in range(gridsize):
        for j in range(gridsize):
            if b_grid[i][j]:
                f_grid[i][j] += -1
                if f_grid[i][j] == 0:
                    nextb_grid[i][j] = False
                else:
                    nextb_grid[i][j] = True
                    count += 1
    return nextb_grid
       
def run_model(f_grid, h_grid, i_threshold, w_direction, burn_seeds):
    ''' From the inputs work out the final burning state and the amount of
    cells that were burned before the fire dies out
    '''
    gridsize = len(f_grid)
    b_grid = []
    count = 0 
    oldf_grid = copy.deepcopy(f_grid)
    # Set up a False b_grid
    for ycoord in range(gridsize):
        conjunction = []
        for xcoord in range(gridsize):
            conjunction.append(False)
        b_grid.append(conjunction)
    # Make the cells in b_grid true if they are in burn_seeds
 
    for (x, y) in burn_seeds:
        b_grid[x][y]= True

    completed = False
    # Loop until there are no burning cells left
    while not completed:

        completed = True
        b_grid = nexttime(f_grid, h_grid, i_threshold, w_direction, b_grid,
                          gridsize, count)
        # Check the grid to see if there are any burning cells
        for List in b_grid:
            for elements in List:
                if elements:
                    completed = False
    cells = 0
    # Calculate the number of changes made to f_grid
    for y in range(gridsize):
        for x in range(gridsize):
            if f_grid[y][x] != oldf_grid[y][x]:
                cells += 1                
    return f_grid, cells      
