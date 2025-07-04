import pygame
import math
from queue import PriorityQueue #used to sort items by priority
import time 

window_width = 600  #setting window size
window = pygame.display.set_mode((window_width, window_width))
pygame.display.set_caption("Maze Solver")

#defining colors
white = (255, 255, 255) 
black = (0, 0, 0)      
green = (0, 255, 0)
red = (255, 0, 0)  
blue = (0, 0, 255)
yellow = (255, 255, 0)
gridlines = (50, 50, 50)

rows = 30  #setting grid size 30x30

pygame.font.init() #setting up a font to display text
font = pygame.font.SysFont("Times New Roman", 18)

#this class will reprsent each square on the grid
class Node: 
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = row * width #row * width of one cell would give x coordinate on the grid
        self.y = col * width #same as obtaining x coordinate
        self.color = black
        self.width = width
        self.neighbors = []

    def __eq__(self, other): #to check if two nodes are equal
        return isinstance(other, Node) and self.row == other.row and self.col == other.col

    def __hash__(self): #to use object as dictionary key
        return hash((self.row, self.col))

    def get_pos(self): #function will return the position of an object
        return self.row, self.col

    def is_wall(self): #walls would be white colored so this function will check if the node is part of the wall
        return self.color == white

    def make_wall(self): #turns a node into a wall by changing its color to white
        self.color = white

    def draw(self, win): #function to draw the node
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def reset(self): #resets the node to background
        self.color = black
    
    def make_start(self): #creates a starting node
        self.color = green

    def make_end(self): #creates an ending node
        self.color = red

    def is_start(self): #checks if  a node is a starting node
        return self.color == green
    
    def is_end(self): #checks if a node is an ending node
        return self.color == red
    
    def update_neighbors(self, grid): #checking which nodes are not walls
        self.neighbors = [] 
        if self.row < rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < rows - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])


def make_grid(rows, width): #function to make the 30x30 grid
    grid = []
    gap = width // rows  
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap)
            grid[i].append(node)
    return grid #grid is the list of lists here


def draw_grid(win, rows, width): #function to draw the gridlines
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, gridlines, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, gridlines, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width, steps = 0, time_taken = 0): #function to draw the entire screen
    win.fill(black)

    for row in grid:
        for node in row:
            node.draw(win) #drawing all the nodes

    draw_grid(win, rows, width) #creating the grid
    draw_info(win, steps, time_taken)
    pygame.display.update() #window gets updated from scratch everytime 

def draw_info(win, steps, time_taken):
    text_surface = font.render(f"Steps: {steps}   Time: {time_taken:.2f}s", True, (255, 255, 255))
    win.blit(text_surface, (10, 10))  #rendering the text to the top left


def h(p1,p2): #calculating the least distance
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2) #returns the number of nodes to go up/down/left/right and not diagonally

def reconstruct_path(came_from, current, draw, steps, start_time): #retracting steps
    while current in came_from:
        current = came_from[current] #going one step back and turning the node yellow
        current.color = yellow
        steps += 1
        draw(steps, time.time() - start_time)

def a_star(draw, grid, start, end):
    count = 0
    steps = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start)) #adding tuple to the queue - start is the node that is actually being evaluated
    came_from = {}

    g_score = {node: float("inf") for row in grid for node in row} #setting all values to infinity
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos()) 

    open_set_hash = {start} #to check if the node is in priority queue because .get() won't work well with PriorityQueue

    start_time = time.time() #starting timer

    while not open_set.empty(): 
        current = open_set.get()[2] #gets the node with the lowest priority score and 2 is the index of the node in the tuple 
        open_set_hash.remove(current)

        if current == end: #checking if the node retrieved is the end node
            reconstruct_path(came_from, end, draw, steps, start_time)
            end.make_end()
            start.make_start()
            return True
    
        for neighbor in current.neighbors: #going through all non-wall nodes
            temp_g = g_score[current] + 1

            if temp_g < g_score[neighbor]: #checking the cost from current to neighbor and if that's less, then that's a better path
                came_from[neighbor] = current
                g_score[neighbor] = temp_g #updating f and g scores
                f_score[neighbor] = temp_g + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor)) #adding the cost to queue with the node
                    open_set_hash.add(neighbor)
                    neighbor.color = blue
        
        draw(steps, time.time() - start_time)

        if current != start and current != end:
            current.color = (100, 100, 100)

    return False


def main(win, window_width): #main loop
    grid = make_grid(rows, window_width)
    start = None
    end = None
    cell_size = window_width // rows #sizing each square
    run = True
    last_steps = 0
    last_time = 0
    while run:
        draw(win, grid, rows, window_width, last_steps, last_time) #this is where the window gets updated with the latest time and steps taken
        for event in pygame.event.get(): #checking if the user is trying to close the window
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    a_star(lambda steps, time_taken: draw(window, grid, rows, window_width, steps, time_taken), grid, start, end)
                    def update_draw(steps, time_taken):
                        nonlocal last_steps, last_time
                        last_steps = steps
                        last_time = time_taken
                        draw(win, grid, rows, window_width, steps, time_taken)
                    a_star(update_draw, grid, start, end)
                if event.key == pygame.K_r:  #resetting the grid when R is pressed
                    start = None
                    end = None
                    last_steps = last_time = 0
                    grid = make_grid(rows, window_width)
            if pygame.mouse.get_pressed()[0]: #if left mouse button is pressed, we get the current position of the cursor in pixels
                pos = pygame.mouse.get_pos()
                row = pos[0] // cell_size
                col = pos[1] // cell_size
                #ensuring the mouse is within the limits of the grid
                if 0 <= row < rows and 0 <= col < rows:
                    node = grid[row][col] #fetching the node object at the given position
                    if not start and node != end:
                        start = node 
                        node.make_start()
                    elif not end and node != start:
                        end = node
                        node.make_end()
                    elif node != start and node != end:
                        node.make_wall()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3: #if right mouse button is pressed, the wall will get removed
                    pos = pygame.mouse.get_pos()
                    row = pos[0] // cell_size
                    col = pos[1] // cell_size
                    #ensuring the mouse is within the limits of the grid
                    if 0 <= row < rows and 0 <= col < rows:
                        node = grid[row][col] #fetching the node object at the given position
                        if node == start:
                            start = None
                            node.reset()
                        elif node == end:
                            end = None
                            node.reset()
                        else:
                            node.reset()

    pygame.quit() #cleaning up the window


main(window, window_width)
