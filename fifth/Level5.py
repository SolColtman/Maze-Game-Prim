import pygame
from sys import exit
import time
from os import environ
import os
from tkinter import Tk

tempWindow=Tk()  # finds resolution of screen
monitor_width=tempWindow.winfo_screenwidth()
monitor_height=tempWindow.winfo_screenheight()
#print(monitor_width, monitor_height)
tempWindow.withdraw()

score=os.path.dirname(os.getcwd())+"/Maze-Game-Prim/score.txt"
config=os.path.dirname(os.getcwd())+"/Maze-Game-Prim/config.txt"
f = open(config, 'r')  # gets configuration from local txt file
lines = f.readlines()
colour = str(lines[0])
mazeSize = int(lines[1])
blockSize = int(lines[2])
screenHeight = blockSize*mazeSize
screenWidth = blockSize*mazeSize
f.close()

font_size=25
x_axis_modifier=0

if mazeSize==8:
    font_size=30
    x_axis_modifier-=10
if mazeSize==10:
    font_size=35
    x_axis_modifier-=15
if mazeSize==15:
    font_size=35
    x_axis_modifier-=55
if mazeSize==20:
    font_size=40
    x_axis_modifier-=75
if mazeSize==25:
    font_size=40
    x_axis_modifier-=120
if mazeSize==35:
    font_size=40
    x_axis_modifier-=180


font_location=os.path.dirname(os.getcwd())+"/Maze-Game-Prim/alarm_clock.ttf"
pygame.font.init()  # initialises font selection
my_font=pygame.font.Font(font_location, font_size)
screen_text=my_font.render("test", True, (255,45,0))


environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (((monitor_width/2)-(screenWidth/2)), ((monitor_height/2)-(screenHeight/2)))  # chooses where window is generated (x,y)

if colour[0] == "b":  # translates colour choice into rgb code
    colour = (0, 0, 255)
elif colour[0] == "p":
    colour = (128, 0, 128)
elif colour[0] == "g":
    colour = (0, 255, 0)
elif colour[0] == "y":
    colour = (255, 255, 0)
if colour[0] == "o":
    colour = (255, 69, 0)

white = (255, 255, 255)
black = (0, 0, 0)
red = (255,45,0)


def timestamp():
    t=time.localtime()
    return time.strftime('%H:%M:%S', t)

class Player(pygame.sprite.Sprite):  # makes Player an object (uses already existing pygame framework)
    def __init__(self, game, x, y):
        self.groups=game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game=game
        self.image=pygame.Surface((blockSize, blockSize))  # creates what the player will look like
        self.image.fill(colour)  # creates sprite the colour the user selected
        self.rect=self.image.get_rect()
        self.x=x
        self.y=y

    def movement(self, dx=0, dy=0):
        if self.collide(dx, dy)==False:
            self.x+=dx
            self.y+=dy

    def collide(self, dx=0, dy=0):  # checks in next move will overlap with a wall
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def update(self):
        self.rect.x=self.x*blockSize
        self.rect.y=self.y*blockSize

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups=game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game=game
        self.image=pygame.Surface((blockSize, blockSize))
        self.image.fill(black)
        self.rect=self.image.get_rect()
        self.x=x
        self.y=y
        self.rect.x=x*blockSize
        self.rect.y=y*blockSize

class EndBlock(Wall):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image.fill(red)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screenWidth, screenHeight+75), pygame.NOFRAME)
        self.clock = pygame.time.Clock()
        self.startTime = pygame.time.get_ticks()
        pygame.mixer.init()
        pygame.display.set_caption("Maze Game")
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.last = pygame.time.get_ticks()
        self.cooldown = 5000
        self.load()


    def load(self):
        self.map = []
        map_location=os.path.dirname(os.getcwd())+"/Maze-Game-Prim/map.txt"
        file=open(map_location, 'r')
        for line in file:
            self.map.append(line)
        file.close()

    def setup_game(self):
        self.all_sprites=pygame.sprite.Group()
        self.walls=pygame.sprite.Group()
        for row, tiles in enumerate(self.map):
            for column, tile in enumerate(tiles):  # creates nested loop
                if tile=='w':
                    Wall(self, column, row)
                if tile=='P':
                    self.player=Player(self, column, row)
                if tile=='E':
                    self.endblock=EndBlock(self, column, row)

        #print("- Maze generation successful... | " + timestamp())

    def clear(self):
        try:
            self.screen.fill(black)
            pygame.display.flip()
        except pygame.error:
            pass  # stops unnecessary errors from interrupting program

    def run(self):
        start_ticks = pygame.time.get_ticks()

        self.playing=True
        while self.playing:
            try:
                self.seconds = (pygame.time.get_ticks() - start_ticks) / 1000
                if self.seconds > 60:  # if more than 60 seconds close the game
                    self.clear()
                elif (self.player.x==mazeSize-2 and self.player.y==mazeSize-2) or (self.player.x==mazeSize-3 and self.player.y==mazeSize-1) or (self.player.x==mazeSize-1 and self.player.y==mazeSize-1):  # if player position matches a block that surrounds the endblock
                    self.endblock.image.fill((0, 255, 0))  # makes endblock green
                    self.player.image.fill(white)  # make player invisible
                    self.player.x+=10
                    self.player.y+=10  # when player reaches end block, they are moved to outside the maze
                    self.final_time=self.seconds
                    #print(self.final_time)
                    self.seconds+=60
                    self.quit()
                else:
                    pygame.display.flip()
                    self.movement()
                    self.update()
                    self.draw()
            except pygame.error:
                self.playing=False


    def quit(self):
        file=open(score, "a+")
        if mazeSize==8:
            file.write("1: "+str(self.final_time)+"\n")
        elif mazeSize==10:
            file.write("2: "+str(self.final_time)+"\n")
        elif mazeSize==15:
            file.write("3: "+str(self.final_time)+"\n")
        elif mazeSize==20:
            file.write("4: " + str(self.final_time) + "\n")
        elif mazeSize==25:
            file.write("5: " + str(self.final_time) + "\n")
        elif mazeSize==35:
            file.write("6: " + str(self.final_time) + "\n")
        file.close()
        pygame.quit()

    def update(self):  # updates position of all sprites
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(white)
        self.all_sprites.draw(self.screen)  # puts walls and player on screen
        self.screen.blit(my_font.render(str(self.seconds), True, (0, 0, 0)), ((screenWidth//2)-((screenWidth//3)+(x_axis_modifier)), (screenHeight+25)))
        pygame.display.flip()

    def movement(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.movement(dx=-1)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.movement(dx=1)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.movement(dy=-1)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.movement(dy=1)

def run():
    import fifth.algorithm5  # opens other python file and makes new maze
    main=Game()
    main.setup_game()
    main.run()