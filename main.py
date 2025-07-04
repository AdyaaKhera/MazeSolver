import pygame
import math

window_width = 600  #setting window size
window = pygame.display.set_mode((window_width, window_width))
pygame.display.set_caption("Maze Solver")

#defining colors
white = (255, 255, 255) 
black = (0, 0, 0)      
green = (0, 255, 0)
red = (255, 0, 0)  
gridlines = (50, 50, 50)

rows = 30  #setting grid size 30x30

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


def draw(win, grid, rows, width): #function to draw the entire screen
    win.fill(black)

    for row in grid:
        for node in row:
            node.draw(win) #drawing all the nodes

    draw_grid(win, rows, width) #creating the grid
    pygame.display.update() #window gets updated from scratch everytime 


def main(win, window_width): #main loop
    grid = make_grid(rows, window_width)
    start = None
    end = None
    cell_size = window_width // rows #sizing each square
    run = True
    while run:
        draw(win, grid, rows, window_width) #this is where the window gets updated
        for event in pygame.event.get(): #checking if the user is trying to close the window
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]: #if left mouse button is pressed, we get the current position of the cursor in pixels
                pos = pygame.mouse.get_pos()
                row = pos[0] // cell_size
                col = pos[1] // cell_size
                #ensuring the mouse is within the limits of the grid
                if row < rows and col < rows:
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
                    if row < rows and col < rows:
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
