#importing libraries
import pygame, random, time 
from queue import PriorityQueue #to create a priority list according to costs

#setup
rows = 25
cell_size = 24
padding_bottom = 80
margin = 40
window_width = cell_size * rows * 2 + margin
window_height = cell_size * rows + padding_bottom
fps = 60

#colors
BLACK  = (20, 20, 20)
WHITE  = (230, 230, 230)
GRAY   = (70, 70, 70)
GREEN  = (0, 200, 0)
RED    = (200, 50, 50)
BLUE   = (50, 100, 255)
YELLOW = (255, 255, 0)

#setting up pygame display
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Maze Solver Simulation")
font = pygame.font.SysFont("Consolas", 16)

#creating the node class to depict each square on the grid
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = BLACK
        self.neighbors = []
        self.is_wall = False
        self.is_robot = False

    def get_pos(self):
        return self.row, self.col

    def reset(self): #resets a node as non-wall square
        self.color = BLACK
        self.is_wall = False
        self.is_robot = False

    def make_start(self): #creating the start node
        self.color = GREEN

    def make_end(self): #end node
        self.color = RED

    def make_wall(self): #making wall by changing the color to white
        self.color = WHITE
        self.is_wall = True

    def make_path(self):  #final path chosen by the algorithm will show up in blue, excluding the starting and ending nodes
        if self.color not in (GREEN, RED):
            self.color = BLUE

    def make_visited(self):  #nodes that are explored but not final path excluding the start and end would be colored gray
        if self.color not in (GREEN, RED):
            self.color = GRAY

    def make_robot(self):  #declaring the node as robot at that position
        self.is_robot = True

    def draw(self, win, offset):  
        pygame.draw.rect(win, self.color, (self.col * cell_size + offset, self.row * cell_size, cell_size, cell_size))
        if self.is_robot: #drawing the robot as a circle
            pygame.draw.circle(win, YELLOW, (self.col * cell_size + offset + cell_size // 2, self.row * cell_size + cell_size // 2), cell_size // 3)

    def update_neighbors(self, grid):  #adding 4-directional neighbors to a list if they are not walls
        self.neighbors = []
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < rows and 0 <= c < rows and not grid[r][c].is_wall:
                self.neighbors.append(grid[r][c])

#creating the grid
def make_grid():  
    return [[Node(i, j) for j in range(rows)] for i in range(rows)]

def draw_grid(win, grid, offset): 
    for row in grid:
        for node in row:
            node.draw(win, offset) #drawing the cells
    for i in range(rows): #drawing the gridlines
        pygame.draw.line(win, GRAY, (offset, i * cell_size), (offset + rows * cell_size, i * cell_size))
        for j in range(rows):
            pygame.draw.line(win, GRAY, (offset + j * cell_size, 0), (offset + j * cell_size, rows * cell_size))

def draw_controls():  #function key at the bottom
    labels = ["E: Explore", "P: Plan (A*)", "R: Reset"]
    for i, text in enumerate(labels):
        surface = font.render(text, True, WHITE)
        screen.blit(surface, (10, rows * cell_size + 10 + 24 * i))

def draw_screen(full_grid, robot_grid):  #drawing two grids with labels and updating it everytime
    screen.fill(BLACK)
    draw_grid(screen, full_grid, 0)
    draw_grid(screen, robot_grid, rows * cell_size + margin)
    draw_controls()
    pygame.display.update()

def h(p1, p2):  #function to calculate the manhattan distance
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw_fn):  #tracing path back from end point by unpacking the list, giving it the value of current node
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw_fn()
        time.sleep(0.01)

def a_star(draw_fn, grid, start, end):  #implementing A* 
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row} #setting values to infinity before calculating minimum cost
    f_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start} #same as open_set, just easy to iterate through

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:  #if end node reached, retracing the path
            reconstruct_path(came_from, end, draw_fn)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors: #checking costs when neighbors are used
            temp_g = g_score[current] + 1
            if temp_g < g_score[neighbor]:  #better path scenario-the one with the lower cost
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor)) #adding it to priority queue
                    open_set_hash.add(neighbor)
                    neighbor.make_visited() #marking neighbor as visited
        draw_fn()
    return False  

def explore_robot(full_grid, robot_grid, start, end):  #robot exploration- robot enters blind with no idea of the generated maze
    from queue import Queue
    q = Queue()
    q.put(start)
    visited = {start}
    came_from = {}

    while not q.empty():
        current = q.get()

        #clearing any previous robot nodes
        for row in robot_grid:
            for node in row:
                node.is_robot = False

        current.make_robot()

        if current == end:
            return came_from  #exploration complete

        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            r, c = current.row + dr, current.col + dc
            if 0 <= r < rows and 0 <= c < rows:
                neighbor = full_grid[r][c]
                if not neighbor.is_wall and robot_grid[r][c] not in visited:
                    visited.add(robot_grid[r][c])
                    q.put(robot_grid[r][c])
                    came_from[robot_grid[r][c]] = current
                elif neighbor.is_wall:
                    robot_grid[r][c].make_wall()  #mapping all the walls onto the robot grid
        draw_screen(full_grid, robot_grid)
        time.sleep(0.01)
    return came_from  

def generate_maze(grid):
    visited = [[False for _ in range(rows)] for _ in range(rows)]

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < rows and not visited[r][c]

    def carve_path(r, c):
        visited[r][c] = True
        grid[r][c].reset() 

        #shuffling directions to randomize maze shape
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc):
                wall_r, wall_c = r + dr // 2, c + dc // 2
                grid[wall_r][wall_c].reset()  
                carve_path(nr, nc)

    #initializing all nodes as walls first
    for i in range(rows):
        for j in range(rows):
            grid[i][j].make_wall()

    #starting from a random odd cell
    start_r = random.randrange(1, rows, 2)
    start_c = random.randrange(1, rows, 2)
    carve_path(start_r, start_c)

    #picking two random odd positions in the maze as start and end and then turning them into their respective nodes
    while True:
        sr, sc = random.randrange(1, rows, 2), random.randrange(1, rows, 2)
        er, ec = random.randrange(1, rows, 2), random.randrange(1, rows, 2)
        if (sr, sc) != (er, ec):
            break

    grid[sr][sc].make_start()
    grid[er][ec].make_end()

    return grid[sr][sc], grid[er][ec] 

def main():
    full_grid = make_grid()
    robot_grid = make_grid()

    start, end = generate_maze(full_grid)

    robot_grid[start.row][start.col].make_start() #copying the start and end nodes to the robot grid
    robot_grid[end.row][end.col].make_end()

    came_from_explore = {}
    run = True
    while run:
        draw_screen(full_grid, robot_grid) #drawing both screens
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:  #exploring the maze when E is pressed
                    came_from_explore = explore_robot(full_grid, robot_grid, start, end)
                    for row in robot_grid:
                        for node in row:
                            node.update_neighbors(robot_grid)

                if event.key == pygame.K_p and came_from_explore:  #mapping out the shortest path when P is pressed
                    for row in robot_grid:
                        for node in row:
                            node.update_neighbors(robot_grid)
                    a_star(lambda: draw_screen(full_grid, robot_grid), robot_grid, robot_grid[start.row][start.col], robot_grid[end.row][end.col])

                if event.key == pygame.K_r:  #resetting the maze when R is pressed
                    main()
    pygame.quit()

main()
