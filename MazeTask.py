import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# Maze representation: 0 = walkable corridor, 1 = solid wall
grid = np.array([
    [1,0,1,1,1,1,1,1,1,0,1,1], # (0,1), (0,9)
    [1,0,1,1,1,1,1,1,1,0,1,1], # (1,1), (1,9)
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,1,1,1],
    [1,0,0,0,1,1,1,1,1,1,1,1],
    [1,0,1,0,1,1,1,0,1,1,1,1],
    [1,0,1,0,0,0,1,0,1,1,1,1],
    [1,0,1,1,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,0,1],
    [0,0,1,1,1,1,1,0,0,0,0,1]
], dtype=int)

# Define source and destination points
source = (10, 0)
destination = (6, 7)

# Phase 1: Identify all accessible cells in the grid
def identify_accessible_cells(grid):
    """Scan the grid and collect all walkable positions"""
    accessible = []
    height, width = grid.shape
    for row in range(height):
        for col in range(width):
            if grid[row, col] == 0:  # 0 indicates a passable area
                accessible.append((row, col))
    return accessible

# Phase 2: Find adjacent nodes for a given position
def get_adjacent_nodes(position, grid):
    """Returns list of valid adjacent positions (cardinal directions)"""
    adjacent = []
    row, col = position
    height, width = grid.shape
    
    # Four cardinal directions: North, South, West, East
    movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in movements:
        next_row, next_col = row + dr, col + dc
        # Validate bounds and confirm it's not a wall
        if 0 <= next_row < height and 0 <= next_col < width and grid[next_row, next_col] == 0:
            adjacent.append((next_row, next_col))
    
    return adjacent

# Phase 3: Build connectivity structure
def build_adjacency_structure(grid):
    """Construct a graph where each cell maps to its adjacent cells"""
    connectivity = defaultdict(list)
    cells = identify_accessible_cells(grid)
    
    for cell in cells:
        adjacent = get_adjacent_nodes(cell, grid)
        connectivity[cell] = adjacent
    
    return connectivity

# Phase 4: Perform depth-first search
def depth_first_search(connectivity, source, destination):
    """
    Execute DFS algorithm to find a valid route.
    Returns ordered sequence of positions from source to destination.
    """
    explored = set()
    route = []
    
    def explore_dfs(current_position):
        if current_position in explored:
            return False
        
        explored.add(current_position)
        route.append(current_position)
        
        if current_position == destination:
            return True
        
        for adjacent_cell in connectivity[current_position]:
            if explore_dfs(adjacent_cell):
                return True
        
        route.pop()
        return False
    
    if explore_dfs(source):
        return route
    else:
        return None

# Execute pathfinding algorithm
print("[Phase 1] Scanning grid for accessible cells...")
cells = identify_accessible_cells(grid)
print(f"   >> Identified {len(cells)} accessible positions")

print("\n[Phase 2-3] Building connectivity graph...")
connection_map = build_adjacency_structure(grid)
print(f"   >> Connectivity structure created ({len(connection_map)} cells)")

print("\n[Phase 4] Executing depth-first search algorithm...")
route = depth_first_search(connection_map, source, destination)

if route:
    print(f"   >> SUCCESS: Route discovered! Total steps: {len(route)}")
    print(f"\n[Route Details] From {source} to {destination}:")
    for idx, coord in enumerate(route):
        print(f"     Step {idx}: {coord}")
else:
    print("   >> FAILED: No valid path exists!")

# Phase 5: Render visual representation
fig, (plot1, plot2) = plt.subplots(1, 2, figsize=(16, 7))

# Display 1: Original grid layout
plot1.imshow(grid, cmap="gray_r", interpolation="nearest")
height, width = grid.shape
plot1.set_xticks(np.arange(-0.5, width, 1), minor=True)
plot1.set_yticks(np.arange(-0.5, height, 1), minor=True)
plot1.grid(which="minor", color="gray", linestyle="-", linewidth=0.8)
plot1.tick_params(which="minor", bottom=False, left=False)
plot1.text(source[1], source[0], "START", ha="center", va="center", color="blue", fontsize=14, fontweight="bold")
plot1.text(destination[1], destination[0], "END", ha="center", va="center", color="red", fontsize=14, fontweight="bold")
plot1.set_xticks([])
plot1.set_yticks([])
plot1.set_title("Grid Layout", fontsize=14, fontweight="bold")

# Display 2: Solution visualization
plot2.imshow(grid, cmap="gray_r", interpolation="nearest")
plot2.set_xticks(np.arange(-0.5, width, 1), minor=True)
plot2.set_yticks(np.arange(-0.5, height, 1), minor=True)
plot2.grid(which="minor", color="gray", linestyle="-", linewidth=0.8)
plot2.tick_params(which="minor", bottom=False, left=False)

if route:
    route_row_coords = [p[0] for p in route]
    route_col_coords = [p[1] for p in route]
    plot2.plot(route_col_coords, route_row_coords, color="green", linewidth=3, marker="o", 
               markersize=6, markerfacecolor="lime", markeredgecolor="darkgreen", 
               label="Discovered Path", alpha=0.7)
    
    plot2.text(source[1], source[0], "START", ha="center", va="center", color="blue", 
               fontsize=14, fontweight="bold")
    plot2.text(destination[1], destination[0], "END", ha="center", va="center", color="red", 
               fontsize=14, fontweight="bold")
    plot2.legend(loc="upper right")

plot2.set_xticks([])
plot2.set_yticks([])
plot2.set_title(f"DFS Solution (Steps: {len(route) if route else 'N/A'})", 
                fontsize=14, fontweight="bold")

plt.tight_layout()
plt.savefig('maze_dfs_solution.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n[Complete] Path visualization exported to maze_dfs_solution.png")