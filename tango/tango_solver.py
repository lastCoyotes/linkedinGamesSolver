# tango solver in python

# TODO: retrieve puzzle by date and subsequent future puzzles and format it into the SUMO/EXEQ arrays below

# rules of linkedin's tango game:
# each row and column must contain 3 moons and 3 suns
# you cannot have 3 of the same symbol in a row
# some cells have "=" or "x" between neighboring cells
# - = means the adjacent cells are the same symbol
# - x means the adjacent cells are the opposite symbol

# some tips from me playing:
# if a row or column already contain 3 of a symbol, fill the rest of that row/column with the opposite symbol
# if there is already two of the same kind of symbol adjacent to each other. place the opposite symbol on either (if possible) ends of that sequence

# on linkedin's site: click once for sun, twice for moon

# future proof for this python script, think about the order of inputs to put into a solver for this program
# dont worry about how we would retrieve the data yet or how that might be formatted, the logic will still apply to solving the initial state

# because of the =/x symbols on the board, you cant simply store a single 2D array of symbols. 
# another method is saving multiple 2D arrays, one to save the sun/moon's, another to save the =/x's
#   - the sun moon array can stay as a 6x6
#   - the =/x array alternates between 5 and 6 (6 by 11 in size) [5,6,5,6,5,6,5,6,5,6,5], most of which is empty

# today's tango puzzle 2/16/26:
# SUn MOon
SUMO = [
    [' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' '],
    ['S', 'M', 'S', 'S', 'M', 'M'],
    ['M', 'S', 'S', 'M', 'S', 'M'],
    [' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ']
]

# the drawback of storing it in a list like this is there will be some verbose logic to determine if were checking vertical neighbors or horizontal neighbors

# (E)X EQuals
EXEQ = [
    ['', '', '=', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '=', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '=', '', ''],
    ['', '', '', '', '', ''],
    ['', '', 'x', '', '']
]

# EXEQ[n%2==0] lists store symbols for horizontal cells
#   EXEQ[''][k] where k is the min value between the two cells it lies between
#   e.g. EXEQ[0][0] is between SUMO[0][0] and SUMO [0][1]
#       note how the first value in SUMO is the same and the second differs by 1
# EXEQ[n%2==1] lists store symbols for vertical cells
#   EXEQ[''][k] where k is the same value as the two cells its between
#   e.g. EXEQ[1][0] is between SUMO[0][0] and SUMO[1][0]
#       note how the second value in SUMO stays the same and the first differs by 1

expected = [
    ['S', 'M', 'S', 'S', 'M', 'M'],
    ['M', 'S', 'M', 'M', 'S', 'S'],
    ['S', 'M', 'S', 'S', 'M', 'M'],
    ['M', 'S', 'S', 'M', 'S', 'M'],
    ['M', 'S', 'M', 'M', 'S', 'S'],
    ['S', 'M', 'M', 'S', 'M', 'S']
]

# what slows me down about this set up is that neighboring cells will require some extra steps vs storing everything like a bidirectional graph, where the edges can contain "weights" which is the = or x sign
# 

# follow logic of any = or x symbols
# search for doubles
# place the opposite symbol before and after the sequence of doubles (if possible)
# if any row or column contain 3 of a symbol, fill the rest of that row/column with the opposite symbol

# repeat until no cells in SUMO array are empty

def solve_tango(SUMO, EXEQ):

    # Solves the Tango puzzle using constraint propagation and backtracking.
    
    # Args:
    #     SUMO: 6x6 grid with 'S' (sun), 'M' (moon), or ' ' (empty)
    #     EXEQ: 11-element list alternating between horizontal (len 5) and vertical (len 6) constraints
    
    # Returns:
    #     Solved 6x6 grid or None if no solution exists
    
   
    
    # Deep copy to avoid modifying input
    grid = [row[:] for row in SUMO]
    
    def get_constraint(r1, c1, r2, c2):
        """Get constraint between two adjacent cells"""
        if r1 == r2:  # Horizontal
            row_idx = r1 * 2
            col_idx = min(c1, c2)
            return EXEQ[row_idx][col_idx] if row_idx < len(EXEQ) else ''
        else:  # Vertical
            row_idx = min(r1, r2) * 2 + 1
            col_idx = c1
            return EXEQ[row_idx][col_idx] if row_idx < len(EXEQ) else ''
    
    def is_valid_placement(r, c, symbol):
        """Check if placing symbol at (r,c) violates any constraints"""
        temp = grid[r][c]
        grid[r][c] = symbol
        
        # Check row/column counts
        row_s = grid[r].count('S')
        row_m = grid[r].count('M')
        col_s = sum(1 for i in range(6) if grid[i][c] == 'S')
        col_m = sum(1 for i in range(6) if grid[i][c] == 'M')
        
        if row_s > 3 or row_m > 3 or col_s > 3 or col_m > 3:
            grid[r][c] = temp
            return False
        
        # Check no three in a row horizontally
        for i in range(4):
            if grid[r][i] == grid[r][i+1] == grid[r][i+2] != ' ':
                grid[r][c] = temp
                return False
        
        # Check no three in a row vertically
        for i in range(4):
            if grid[i][c] == grid[i+1][c] == grid[i+2][c] != ' ':
                grid[r][c] = temp
                return False
        
        # Check adjacent constraints
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for nr, nc in neighbors:
            if 0 <= nr < 6 and 0 <= nc < 6 and grid[nr][nc] != ' ':
                constraint = get_constraint(r, c, nr, nc)
                if constraint == '=':
                    if grid[r][c] != grid[nr][nc]:
                        grid[r][c] = temp
                        return False
                elif constraint == 'x':
                    if grid[r][c] == grid[nr][nc]:
                        grid[r][c] = temp
                        return False
        
        grid[r][c] = temp
        return True
    
    def propagate():
        """Apply constraint propagation rules"""
        changed = True
        while changed:
            changed = False
            for r in range(6):
                for c in range(6):
                    if grid[r][c] != ' ':
                        continue
                    
                    # Try each symbol
                    valid_symbols = []
                    for symbol in ['S', 'M']:
                        if is_valid_placement(r, c, symbol):
                            valid_symbols.append(symbol)
                    
                    # If only one valid symbol, place it
                    if len(valid_symbols) == 1:
                        grid[r][c] = valid_symbols[0]
                        changed = True
                    elif len(valid_symbols) == 0:
                        return False  # No valid placement
        return True
    
    def solve():
        """Backtracking solver"""
        if not propagate():
            return False
        
        # Find next empty cell
        for r in range(6):
            for c in range(6):
                if grid[r][c] == ' ':
                    for symbol in ['S', 'M']:
                        if is_valid_placement(r, c, symbol):
                            grid[r][c] = symbol
                            if solve():
                                return True
                            grid[r][c] = ' ' # backtracking step
                    return False
        return True  # All cells filled
    
    if solve():
        return grid
    return None

def unicode_print(grid):
    for row in grid:
        print(' '.join('☼' if cell == 'S' else '☾' if cell == 'M' else cell for cell in row))

solution = solve_tango(SUMO, EXEQ)

print(solution)
unicode_print(solution)
print()

for row in solution:
    print(' '.join(row))
