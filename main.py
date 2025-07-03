import pygame
import math

window_width = 600  #setting window size
window = pygame.display.set_mode((window_width, window_width))
pygame.display.set_caption("Maze Solver")

#defining colors
white = (255, 255, 255)  # wall
black = (0, 0, 0)        # background
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


def main(win, width): #main loop
    grid = make_grid(rows, width)

    run = True
    while run:
        draw(win, grid, rows, width) #this is where the window gets updated
        for event in pygame.event.get(): #checking if the user is trying to close the window
            if event.type == pygame.QUIT:
                run = False

    pygame.quit() #cleaning up the window


main(window, window_width)
