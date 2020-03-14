
def heightcheck(a, b, h_grid, i, j):
    ''' Calculates the score based on the height of the cells
    '''
    heightcell = h_grid[i][j]
    heightadj = h_grid[b][a]
    if heightadj < heightcell:
        calculatednum = 2
    elif heightadj == heightcell:
        calculatednum = 1
    elif heightadj > heightcell:
        calculatednum = 0.5
    return calculatednum

    
def wind_addition(w_direction, a, i, j, h_grid, i_threshold):
    ''' If there is a direction of wind, it takes three more cells into 
    consideration 
    '''
    if w_direction is not None:   
        # setting up the windkey dictionary
        north = {'x': (1, -1), 'y': (0, 0)}    
        east = {'x': (0, 0), 'y': (1, -1)}
        south = {'x': (1, -1), 'y': (0, 0)}
        west = {'x': (0, 0), 'y': (1, -1)}
        ne = {'x': (-1, 0), 'y': (0, 1)}
        nw = {'x': (1, 0), 'y': (0, 1)}
        se = {'x': (-1, 0), 'y': (0, -1)}
        sw = {'x': (1, 0), 'y': (0, -1)}
        windkey = {'N': [(0, -2), north], 'E': [(2, 0), east],
                   'S': [(0, 2), south], 'W': [(-2, 0), west],
                   'NE': [(2, -2), ne], 'NW': [(-2, -2), nw], 
                   'SE': [(2, 2), se], 'SW': [(-2, 2), sw]}
        # Take wind direction into account accounting for new adj cells
        if w_direction in windkey:
            adjacents = a[0]
            burningpos = a[1]
            change = windkey[w_direction][0]
            # Initial cell transormation
            xpos = j + change[0]
            ypos = i + change[1]
            if (xpos, ypos) in burningpos:
                adjacents.append(heightcheck(xpos, ypos, h_grid, i, j)) 
            # Second cell due to wind tranformation
            adjacentnew = windkey[w_direction][1]
            newxpos = xpos + adjacentnew['x'][0]
            newypos = ypos + adjacentnew['y'][0]

            if newxpos >= 0 and newypos >= 0:
                if (newxpos, newypos) in burningpos:
                    adjacents.append(heightcheck(newxpos, 
                                                 newypos, h_grid, i, j)) 
            # Next cell due to wind
            newxposy = xpos + adjacentnew['x'][1]
            newyposy = ypos + adjacentnew['y'][1]
            if newxposy >= 0 and newyposy >= 0:            
                if (newxposy, newyposy) in burningpos:
                    adjacents.append(heightcheck(newxposy, 
                                                 newyposy, h_grid, i, j)) 
            # Calculates the total impacting the cell
            total = 0          
            for values in adjacents:
                total += values
            if total >= i_threshold:
                return 'True'
            else:
                return False
        else:
            return False
    else:
        return False
        
          
def adjacent_addition(b_grid, i, j, i_threshold, h_grid):
    '''Works out whether the cell is adjacent to the coordinates'''
    x = 0 
    y = 0
    burningpos = []
    # Works out the coords of the burning cells and adds to a list
    for positions in b_grid:
        x = 0
        for cells in positions:
            if cells:
                burningpos.append((x, y))
            x+=1
        y+=1
    adjacents = []
    # Works out the adjacent cells and gets their effective impact
    for a, b in burningpos:
        xdiff, ydiff = j - a, i - b
        if abs(xdiff) <= 1 and abs(ydiff) <= 1:
            adjacents.append(heightcheck(a, b, h_grid, i, j))
    # Calculates the total effective impacts
    total = 0          
    for values in adjacents:
        total += values
    if total >= i_threshold:
        return 'True'
    else:
        return (adjacents, burningpos)
    
    
def check_ignition(b_grid, f_grid, h_grid, i_threshold, w_direction, i, j):   
    ''' Checks the ignition and returns True if it ignites
    '''
    # Check the fuel is more than 0
    if f_grid[i][j] <= 0:
        return False
    # Check that it isnt burning
    if b_grid[i][j]:
        return False
    # Check i_threshold is valid
    if i_threshold <= 0:
        return True
       
        
    adjignite = adjacent_addition(b_grid, i, j, i_threshold, h_grid)
    if adjignite == 'True':
        return True
    else:
        windignite = wind_addition(w_direction, adjignite, i, j,
                                   h_grid, i_threshold)
        if windignite == 'True':
            return True
        else:
            return False
