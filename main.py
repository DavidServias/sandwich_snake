from pygame.locals import *
from random import randint
import pygame
import time


class Condiment:
    x = 0
    y = 0
    step = 50

    def __init__(self,x,y):
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y))


class Player:
    x = [50]
    y = [50]
    step = 50
    direction = 0
    length = 1
    width = 50
    updateCountMax = 2
    updateCount = 0

    def __init__(self, length):
        self.length = length
        for i in range(0,2000):
            self.x.append(-100)
            self.y.append(-100)
        # initial positions, no collision.
        self.x[1] = 1*50
        self.x[2] = 2*50

    def increment_length(self):
        self.length += 1

    def update(self):

        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:

            # update previous positions
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]

            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step

            print(self.x[0])

            self.updateCount = 0

    def moveRight(self):
        self.direction = 0

    def moveLeft(self):
        self.direction = 1

    def moveUp(self):
        self.direction = 2

    def moveDown(self):
        self.direction = 3

    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i]))


class Game:
    def isCollision(self,x1,y1,x2,y2,bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False


class App:

    windowWidth = 800
    windowHeight = 600
    player = 0
    condiment = 0
    condiment_delay = 20
    condiment_delay_cycles = 0

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._condiment_surf = None
        self.game = Game()
        self.player = Player(1)
        self.condiment = Condiment(5,5)
        self.delay = 100
        pygame.init()
        pygame.mixer.init()
        self.num_num = pygame.mixer.Sound('sound/num_num.wav')
        self.whistle = pygame.mixer.Sound('sound/whistle.wav')
        self.oops = pygame.mixer.Sound('sound/oops.wav')

        self.whistle_enabled = True
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        self.background_image = pygame.image.load("bg.png").convert()


    def on_init(self):

        pygame.mixer.music.load('sound/background_music.wav')
        pygame.mixer.music.play(-1)
        # pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._image_surf = pygame.image.load("sandwich.jpg").convert()
        self._condiment_surf = pygame.image.load("mayo.png").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def decrement_delay(self):
        self.delay = self.delay - 5

    def reset_condiment_delay(self):
        self.condiment_delay_cycles = 0
        self.condiment_delay = randint(10, 40)
        self.whistle_enabled = True

    def on_loop(self):
        self.player.update()
        # does snake eat condiment?
        for i in range(0,self.player.length):
            if self.game.isCollision(self.condiment.x,self.condiment.y,self.player.x[i], self.player.y[i],50):
                pygame.mixer.Sound.play(self.num_num)
                self.condiment.x = randint(2,9) * 50
                self.condiment.y = randint(2,9) * 50
                self.player.length = self.player.length + 1
                self.reset_condiment_delay()
                self.decrement_delay()

        # does snake collide with itself?
        for i in range(2,self.player.length):
            if self.game.isCollision(self.player.x[0],self.player.y[0],self.player.x[i], self.player.y[i],45):
                print("You lose! Collision: ")
                print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
                print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
                self.end_game()

        # does snake touch the edges?
        x_val = self.player.x[0]
        y_val = self.player.y[0]
        window_width = self.windowWidth
        window_height = self.windowHeight
        player_width = self.player.width
        if x_val > window_width - player_width or x_val < 0:
            self.end_game()
        if y_val > window_height - player_width or y_val < 0:
            self.end_game()

    def on_render(self):
        self._display_surf.blit(self.background_image, [0, 0])
        # self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._image_surf)
        if self.condiment_delay_cycles == self.condiment_delay:
            self.condiment.draw(self._display_surf, self._condiment_surf)
            if self.whistle_enabled:
                pygame.mixer.Sound.play(self.whistle)
                self.whistle_enabled = False
        else:
            self.condiment_delay_cycles += 1
        pygame.display.flip()

    def end_game(self):
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(self.oops)
        time.sleep(3)
        pygame.quit()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[K_RIGHT]):
                self.player.moveRight()

            if (keys[K_LEFT]):
                self.player.moveLeft()

            if (keys[K_UP]):
                self.player.moveUp()

            if (keys[K_DOWN]):
                self.player.moveDown()

            if (keys[K_ESCAPE]):
                self._running = False

            self.on_loop()
            self.on_render()
            pygame.display.update()
            time.sleep(self.delay/1000)

        self.on_cleanup()


if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
