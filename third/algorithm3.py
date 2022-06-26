import random
import os

config = os.path.dirname(os.getcwd()) + "/Code/config.txt"
f = open(config, 'r')  # gets configuration from local txt file
lines = f.readlines()
mazeSize = int(lines[1])
blockSize = int(lines[2])
screenHeight = blockSize * mazeSize
screenWidth = blockSize * mazeSize
f.close()


class MazeGenerator:
    def __init__(self):  # creating all variables to be used throughout process
        self.cell = 'c'
        self.wall = 'w'
        self.unvisited = 'u'
        self.maze = []
        self.walls = []

    def surroundingCells(self, randomWall):  # checks that every wall used doesn't have more than one cell around it
        s_cells = 0
        if self.maze[randomWall[0] - 1][randomWall[1]] == 'c':
            s_cells += 1
        if self.maze[randomWall[0] + 1][randomWall[1]] == 'c':
            s_cells += 1
        if self.maze[randomWall[0]][randomWall[1] - 1] == 'c':
            s_cells += 1
        if self.maze[randomWall[0]][randomWall[1] + 1] == 'c':
            s_cells += 1

        return s_cells

    def createMaze(self):  # creates the maze before it's shown on screen
        for x in range(0, mazeSize):
            line = []
            for i in range(0, mazeSize):
                line.append(self.unvisited)  # creates 2d array
            self.maze.append(line)

        startingheight, startingwidth = int(random.randint(1, (mazeSize - 2))), int(
            random.randint(1, (mazeSize - 2)))  # random starting positions for the algorithm
        self.maze[startingheight][startingwidth] = self.cell
        self.walls.append([startingheight - 1, startingwidth])  # adds surrounding cells to list 'walls'
        self.walls.append([startingheight, startingwidth - 1])
        self.walls.append([startingheight, startingwidth + 1])
        self.walls.append([startingheight + 1, startingwidth])

        self.maze[startingheight - 1][startingwidth] = self.wall  # changes cells around starting location to walls
        self.maze[startingheight][startingwidth - 1] = self.wall
        self.maze[startingheight][startingwidth + 1] = self.wall
        self.maze[startingheight + 1][startingwidth] = self.wall

        return self.maze, self.walls

    def algorithm(self):  # Prim's randomised algorithm that carves out random, perfect maze from grid
        while self.walls:  # while there are self.walls, pick random wall from list
            randomWall = self.walls[int(random.random() * len(self.walls)) - 1]

            if randomWall[1] != 0:  # left wall
                if self.maze[randomWall[0]][randomWall[1] - 1] == 'u' and self.maze[randomWall[0]][
                    randomWall[1] + 1] == 'c':
                    s_cells = self.surroundingCells(randomWall)
                    if s_cells < 2:
                        self.maze[randomWall[0]][randomWall[1]] = 'c'

                        if randomWall[0] != 0:  # upper
                            if self.maze[randomWall[0] - 1][randomWall[1]] != 'c':
                                self.maze[randomWall[0] - 1][randomWall[1]] = 'w'
                            if [randomWall[0] - 1, randomWall[1]] not in self.walls:
                                self.walls.append([randomWall[0] - 1, randomWall[1]])

                        if randomWall[0] != mazeSize - 1:  # bottom
                            if self.maze[randomWall[0] + 1][randomWall[1]] != 'c':
                                self.maze[randomWall[0] + 1][randomWall[1]] = 'w'
                            if [randomWall[0] + 1, randomWall[1]] not in self.walls:
                                self.walls.append([randomWall[0] + 1, randomWall[1]])

                        if randomWall[1] != 0:  # left
                            if self.maze[randomWall[0]][randomWall[1] - 1] != 'c':
                                self.maze[randomWall[0]][randomWall[1] - 1] = 'w'
                            if [randomWall[0], randomWall[1] - 1] not in self.walls:
                                self.walls.append([randomWall[0], randomWall[1] - 1])

                    for wall in self.walls:
                        if wall[0] == randomWall[0] and wall[1] == randomWall[1]:
                            self.walls.remove(wall)
                    continue  # returns to while loop

            if randomWall[0] != 0:  # upper
                if self.maze[randomWall[0] - 1][randomWall[1]] == 'u' and self.maze[randomWall[0] + 1][
                    randomWall[1]] == 'c':
                    s_cells = self.surroundingCells(randomWall)
                    if s_cells < 2:
                        self.maze[randomWall[0]][randomWall[1]] = 'c'

                        if randomWall[0] != 0:  # upper
                            if self.maze[randomWall[0] - 1][randomWall[1]] != 'c':
                                self.maze[randomWall[0] - 1][randomWall[1]] = 'w'
                            if [randomWall[0] - 1, randomWall[1]] not in self.walls:
                                self.walls.append([randomWall[0] - 1, randomWall[1]])

                        if randomWall[1] != 0:  # left
                            if self.maze[randomWall[0]][randomWall[1] - 1] != 'c':
                                self.maze[randomWall[0]][randomWall[1] - 1] = 'w'
                            if [randomWall[0], randomWall[1] - 1] not in self.walls:
                                self.walls.append([randomWall[0], randomWall[1] - 1])

                        if randomWall[1] != mazeSize - 1:  # right
                            if self.maze[randomWall[0]][randomWall[1] + 1] != 'c':
                                self.maze[randomWall[0]][randomWall[1] + 1] = 'w'
                            if [randomWall[0], randomWall[1] + 1] not in self.walls:
                                self.walls.append([randomWall[0], randomWall[1] + 1])

                    for wall in self.walls:
                        if wall[0] == randomWall[0] and wall[1] == randomWall[1]:
                            self.walls.remove(wall)
                    continue  # returns to while loop

            if randomWall[0] != mazeSize - 1:  # bottom
                if self.maze[randomWall[0] + 1][randomWall[1]] == 'u' and self.maze[randomWall[0] - 1][
                    randomWall[1]] == 'c':
                    s_cells = self.surroundingCells(randomWall)
                    if s_cells < 2:
                        self.maze[randomWall[0]][randomWall[1]] = 'c'

                        if randomWall[0] != mazeSize - 1:  # bottom
                            if self.maze[randomWall[0] + 1][randomWall[1]] != 'c':
                                self.maze[randomWall[0] + 1][randomWall[1]] = 'w'
                            if [randomWall[0] + 1, randomWall[1]] not in self.walls:
                                self.walls.append([randomWall[0] + 1, randomWall[1]])

                        if randomWall[1] != 0:  # left
                            if self.maze[randomWall[0]][randomWall[1] - 1] != 'c':
                                self.maze[randomWall[0]][randomWall[1] - 1] = 'w'
                            if [randomWall[0], randomWall[1] - 1] not in self.walls:
                                self.walls.append([randomWall[0], randomWall[1] - 1])

                        if randomWall[1] != mazeSize - 1:  # right
                            if self.maze[randomWall[0]][randomWall[1] + 1] != 'c':
                                self.maze[randomWall[0]][randomWall[1] + 1] = 'w'
                            if [randomWall[0], randomWall[1] + 1] not in self.walls:
                                self.walls.append([randomWall[0], randomWall[1] + 1])

                    for wall in self.walls:  # resets the walls list
                        if wall[0] == randomWall[0] and wall[1] == randomWall[1]:
                            self.walls.remove(wall)
                    continue  # returns to while loop

            if randomWall[1] != mazeSize - 1:  # right
                if self.maze[randomWall[0]][randomWall[1] + 1] == 'u' and self.maze[randomWall[0]][
                    randomWall[1] - 1] == 'c':
                    s_cells = self.surroundingCells(randomWall)
                    if s_cells < 2:
                        self.maze[randomWall[0]][randomWall[1]] = 'c'

                        if randomWall[1] != mazeSize - 1:  # right
                            if self.maze[randomWall[0]][randomWall[1] + 1] != 'c':
                                self.maze[randomWall[0]][randomWall[1] + 1] = 'w'
                            if [randomWall[0], randomWall[1] + 1] not in self.walls:
                                self.walls.append([randomWall[0], randomWall[1] + 1])

                        if randomWall[0] != mazeSize - 1:  # bottom
                            if self.maze[randomWall[0] + 1][randomWall[1]] != 'c':
                                self.maze[randomWall[0] + 1][randomWall[1]] = 'w'
                            if [randomWall[0] + 1, randomWall[1]] not in self.walls:
                                self.walls.append([randomWall[0] + 1, randomWall[1]])

                        if randomWall[0] != 0:  # upper
                            if self.maze[randomWall[0] - 1][randomWall[1]] != 'c':
                                self.maze[randomWall[0] - 1][randomWall[1]] = 'w'
                            if [randomWall[0] - 1, randomWall[1]] not in self.walls:
                                self.walls.append([randomWall[0] - 1, randomWall[1]])

                    for wall in self.walls:
                        if wall[0] == randomWall[0] and wall[1] == randomWall[1]:
                            self.walls.remove(wall)

                    continue  # returns to while loop

            for wall in self.walls:  # resets the walls list
                if wall[0] == randomWall[0] and wall[1] == randomWall[1]:
                    self.walls.remove(wall)

        for x in range(0, mazeSize):
            for i in range(0, mazeSize):
                if self.maze[x][i] == 'u':
                    self.maze[x][i] = 'w'  # replaces 'u' with 'w'

        for x in range(0, mazeSize):  # removes corresponding blocks
            if self.maze[1][x] == 'c':
                self.maze[0][x] = 'c'
                break

        for i in range(mazeSize - 1, 0, -1):  # removes corresponding blocks
            if self.maze[mazeSize - 2][i] == 'c':
                self.maze[mazeSize - 1][i] = 'c'
                break

    def writeMaze(self):
        self.maze[1][1] = 'P'  # places player on first square
        self.maze[0][1] = 'w'
        self.maze[1][2] = 'c'
        self.maze[mazeSize - 1][mazeSize - 2] = 'E'  # makes end square the letter E
        self.maze[mazeSize - 1][mazeSize - 3] = 'c'
        self.maze[mazeSize - 1][mazeSize - 4] = 'c'
        for x in range(0, (mazeSize - 1)):
            self.maze[0][x] = 'w'

        map = os.path.dirname(os.getcwd()) + "/Code/map.txt"
        file = open(map, 'w')
        for x in range(0, len(self.maze)):
            for y in range(0, len(self.maze[x])):
                if self.maze[x][y] == 'w' or self.maze[x][y] == 'c' or self.maze[x][y] == 'P' or self.maze[x][y] == 'E':
                    file.write(self.maze[x][y])
            file.write("\n")
        file.write('w' * mazeSize)  # adds bottom barrier
        file.close()

    def start(self):
        main.createMaze()
        main.algorithm()
        main.writeMaze()


main = MazeGenerator()
main.start()