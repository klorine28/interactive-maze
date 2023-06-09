import pygame, sys
from collections import deque
from tkinter import messagebox, Tk


#code and understanding from: http://www.pygame.org/project/767/  ,  https://www.pygame.org/project/5609  ,  https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame   , www.pygame.org/wiki, https://www.codeproject.com/Articles/509517/FirstWins-Pathfinding-Algorithm
#window size
size = (width, height) = 720, 720
#initialize pygame
pygame.init()

goals = pygame.display.set_mode(size)
clock = pygame.time.Clock()
#set grid size change to desired
y, x = 10, 10
#set x and y parameters for grid
w = width//y
h = height//x
#create grid,path and explored cells all lists to store values ie positions
grid = [ ]
queue, explored_cells = deque(), []
path = []
#the game
class location:
    #definespostition as well as obstacles and both explored and unexplored 
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors_cells = []
        self.prev = None
        self.wall = False
        self.explored_cells = False
        if (i+j)%7 == 0:
            self.wall == True
    #define shape of the grid as well as looks   
    def show_game(self, goals, col, shape= 1):
        if self.wall == True:
            col = (0, 0, 0)
        if shape == 1:
            pygame.draw.rect(goals, col, (self.x*w, self.y*h, w-1, h-1))
    #defines legal moves the agent can make 8 moves 4 cardinal 4 diagonal stores changes in grid 
    def cardinal_directions(self, grid):
        if self.x < y - 1:
            self.neighbors_cells.append(grid[self.x+1][self.y])
        if self.x > 0:
            self.neighbors_cells.append(grid[self.x-1][self.y])
        if self.y < x - 1:
            self.neighbors_cells.append(grid[self.x][self.y+1])
        if self.y > 0:
            self.neighbors_cells.append(grid[self.x][self.y-1])
        if self.x < y - 1 and self.y < x - 1:
            self.neighbors_cells.append(grid[self.x+1][self.y+1])
        if self.x < y - 1 and self.y > 0:
            self.neighbors_cells.append(grid[self.x+1][self.y-1])
        if self.x > 0 and self.y < x - 1:
            self.neighbors_cells.append(grid[self.x-1][self.y+1])
        if self.x > 0 and self.y > 0:
            self.neighbors_cells.append(grid[self.x-1][self.y-1])

#defines current position in relation to x and y
def place_wall(pos, state):
    i = pos[0] // w
    j = pos[1] // h
    grid[i][j].wall = state

def place(pos):
    i = pos[0] // w
    j = pos[1] // h
    return w, h
#appends current position 
for i in range(y):
    arr = []
    for j in range(x):
        arr.append(location(i, j))
    grid.append(arr)
#movement in the defined position 
for i in range(y):
    for j in range(x):
        grid[i][j].cardinal_directions(grid)

#state goal start end and obstacles Walls    
start = grid[0][0]
#for random end select randint x>x0 and y>y0
end = grid[x-1][y-1]
start.wall = False
end.wall = False

queue.append(start)
start.explored_cells = True
#defines serching for goal 
def main():
    flag = False
    noflag = True
    startflag = False

    while True:
        #allows for the manual placement of walls in the clicked grid cell 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 3):  
                    place_wall(pygame.mouse.get_pos(), event.button==1)
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0] or event.buttons[2]:
                    place_wall(pygame.mouse.get_pos(), event.buttons[0])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    startflag = True
        # actual serching code that checks if flag or goal is found and updates the agents position also checks for valid moves in the grid
        if startflag:
            if len(queue) > 0:
                current = queue.popleft()
                if current == end:
                    temp = current
                    while temp.prev:
                        path.append(temp.prev)
                        temp = temp.prev 
                    if not flag:
                        flag = True
                        print("Done")
                    elif flag:
                        continue
                if flag == False:
                    for i in current.neighbors_cells:
                        if not i.explored_cells and not i.wall:
                            i.explored_cells = True
                            i.prev = current
                            queue.append(i)
            #when flag is unreachable 
            else:
                if noflag and not flag:
                    Tk().wm_withdraw()
                    messagebox.show_gameinfo("No Solution", "There was no solution" )
                    noflag = False
                else:
                    continue

        #sets game colours and envoierment colours
        goals.fill((0, 20, 20))
        for i in range(y):
            for j in range(x):
                location = grid[i][j]
                location.show_game(goals, (255,255,255))
                if location in path:
                    location.show_game(goals, (173,255,47))
                elif location.explored_cells:
                    location.show_game(goals, (255,255,224))
                if location in queue and not flag:
                    location.show_game(goals, (44, 62, 80))
                    location.show_game(goals, (193,255,47), 0)
                if location == start:
                    location.show_game(goals, (0,255,0))
                if location == end:
                    location.show_game(goals, (255,0,0))
                
                
        pygame.display.flip()


main()
