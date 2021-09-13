import pygame
import time
import random
from pygame import font
from pygame.locals import *

SIZE = 40

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/snakefood.png").convert()
        self.block_x = SIZE * 3
        self.block_y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.block_x,self.block_y))
        pygame.display.flip()

    def move(self):
        self.block_x = random.randint(1,24) * SIZE
        self.block_y = random.randint(1,19) * SIZE
        
class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/snake.jpg").convert()
        self.block_x = [SIZE]*length
        self.block_y = [SIZE]*length
        self.direction = "down"

    def increase_length(self):
        self.length += 1
        self.block_x.append(-1)
        self.block_y.append(-1)

    #creating left, right, up, down movements
    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    #making automatic movement
    def walk(self):
        for i in range(self.length-1,0,-1):
            self.block_x[i] = self.block_x[i-1]
            self.block_y[i] = self.block_y[i-1]

        if self.direction == "up":
            self.block_y[0] -= SIZE
        if self.direction == "down":
            self.block_y[0] += SIZE
        if self.direction == "left":
            self.block_x[0] -= SIZE
        if self.direction == "right":
            self.block_x[0] += SIZE
        
        self.draw()

    #drawing block on screen
    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.block_x[i],self.block_y[i]))
        pygame.display.flip()

class Game:
    def __init__(self):
        
        pygame.init()
        pygame.display.set_caption("SNAKE GAME")
        #config of display
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    #collison detection
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False 

    def display_score(self):
        font = pygame.font.SysFont('arial', 25)
        score = font.render(f"Score: {(self.snake.length)-1}", True, (207, 0, 38))
        self.surface.blit(score, (10,10))
        pygame.display.flip()

    def render_bg(self):
        bg = pygame.image.load("resources/snakebg.jpg")
        self.surface.blit(bg, (0,0))

    def play(self):
        self.render_bg()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.update()

        #snake colliding with apple
        if self.is_collision(self.snake.block_x[0], self.snake.block_y[0], self.apple.block_x, self.apple.block_y):
            self.snake.increase_length()
            self.apple.move()

        #snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.block_x[0], self.snake.block_y[0], self.snake.block_x[i], self.snake.block_y[i]):
                raise "Game Over"

        #hits edges
        if not (0 <= self.snake.block_x[0] <= 1000 and 0 <= self.snake.block_y[0] <= 800):
            raise "Hit the boundry error"


    def show_game_over(self):
        self.render_bg()
        font = pygame.font.SysFont('arial', 25)
        line1 = font.render(f"Game Over. Your Score is: {(self.snake.length)-1}", True, (207, 0, 38))
        self.surface.blit(line1, (200,250))
        line2 = font.render(f"To play again, hit ENTER. To exit, press Escape", True, (207, 0, 38))
        self.surface.blit(line2, (200,300))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)


    def run(self):
        #event loop to make screen pop up
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                            
                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == pygame.QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            if self.snake.length > 30:
                time.sleep(.08)
            elif self.snake.length > 60:
                time.sleep(.06)
            else:
                time.sleep(.12)




if __name__ == "__main__":

    game = Game()
    game.run()
            