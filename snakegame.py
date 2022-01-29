import pygame
from pygame.locals import *
import time
import random

# program is fully working, next challenge will be exit game when snake hits the boudaries,
# speed up when eats the mouse, make the file
size = 40
background_color = (0, 0, 0)


class Mouse:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/mouse.sizedown.png").convert_alpha()
        self.parent_screen = parent_screen
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 24) * size
        self.y = random.randint(1, 19) * size


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/snake_block.jpg").convert()

        self.direction = "down"

        self.length = length
        self.x = [40] * length
        self.y = [40] * length
        #self.time_sleep = time_sleep

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    #def increase_speed(self):
        #self.time_sleep -= 0.1

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "up":
            self.y[0] -= size
        if self.direction == "down":
            self.y[0] += size
        if self.direction == "left":
            self.x[0] -= size
        if self.direction == "right":
            self.x[0] += size

        self.draw()

    def draw(self):
        self.parent_screen.fill(background_color)

        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((1000, 800))
        #self.boundary1 = pygame.draw.line(self.surface, "Blue", (10, 10), (990, 10), 30)
        #self.boundary2 = pygame.draw.line(self.surface, "Blue", (990, 10), (990, 790), 30)
        #self.boundary3 = pygame.draw.line(self.surface, "Blue", (990, 790), (10, 790), 30)
        #self.boundary4 = pygame.draw.line(self.surface, "Blue", (10, 790), (10, 10), 30)
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.mouse = Mouse(self.surface)
        self.mouse.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (850, 10))

    def play(self):
        self.snake.walk()
        self.mouse.draw()
        self.display_score()
        pygame.display.flip()

        # snake collision with food
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.mouse.x, self.mouse.y):
            self.snake.increase_length()
            self.mouse.move()


        # snake collision with himself
        for i in range(4, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Game over"

        #snake collision with boundaries
        #if self.is_collision(self.snake.x[0], self.snake.y[0], )

    def show_game_over(self):
        self.surface.fill(background_color)
        font = pygame.font.SysFont("arial", 50)
        line1 = font.render(f"GAME OVER! Your score is: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("Play again press Enter!", True, (255, 255, 255))
        self.surface.blit(line2, (250, 400))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.mouse = Mouse(self.surface)

    def run(self):
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

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.1)
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.run()
