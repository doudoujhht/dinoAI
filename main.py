import pygame
import os
import random
import sys

pygame.init()

# variable globale
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "mcA1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "mcA2.png")),
           pygame.image.load(os.path.join("Assets/Dino", "mcA3.png")),
           pygame.image.load(os.path.join("Assets/Dino", "mcA4.png")),
           pygame.image.load(os.path.join("Assets/Dino", "mcA5.png")),
           pygame.image.load(os.path.join("Assets/Dino", "mcA6.png"))]

JUMPING = pygame.image.load(os.path.join("Assets/Dino", "mcA6.png"))

FONT = pygame.font.Font('freesansbold.ttf', 20)

BG = pygame.image.load(os.path.join("Assets/Other", "track.png"))

LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5

    def __init__(self, img=RUNNING[0]):
        self.image = img
        self.dino_run = True
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, img.get_width(), img.get_height())
        self.step_index = 0

    def update(self):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.step_index >= 10:
            self.step_index = 0

    def jump(self):
        """
        ca permet de faire sauter le dino je suis pas physicien so j'ai pas plus d'info mon but c'est le AI so ca j'ai
        juste copié
        :return: rien
        """
        self.image = JUMPING
        if self.dino_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

        if self.jump_vel <= -self.JUMP_VEL:
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.JUMP_VEL

    def run(self):
        """
        en gros le step index est un nombre de 0 à 10 quand il est entre 0 et 4 inclusivement on a le dino qui fait
        un pas vers la gauche ensuite de 5 a 9 on a le dino qui fait un pas vers la droite donnant l'illusion qu'il
        se deplace quand c'est a 10 on recommence ce qui fait semblant que le dino cours a l'infini
        :return: rien
        """
        self.image = RUNNING[self.step_index // 2]
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.image)


class Obstacle:
    def __init__(self, image, number_of_cactus):
        self.image = image
        self.type = number_of_cactus
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < - self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

    def get_mask(self):
        return pygame.mask.from_surface(self.image[self.type])


class SmallCactus(Obstacle):
    def __init__(self, image, number_of_cactus):
        super().__init__(image, number_of_cactus)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image, number_of_cactus):
        super().__init__(image, number_of_cactus)
        self.rect.y = 300


def remove(index):
    dinosaures.pop(index)


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, dinosaures
    clock = pygame.time.Clock()
    points = 0

    obstacles = []
    dinosaures = [Dinosaur()]

    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = FONT.render(f'Points: {str(points)}', True, (0, 0, 0))
        SCREEN.blit(text, (950, 50))

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))

        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill((255, 255, 255))

        for dinosaure in dinosaures:
            dinosaure.update()
            dinosaure.draw(SCREEN)

        if len(dinosaures) == 0:
            break

        if len(obstacles) == 0:
            rand_int = random.randint(0, 1)
            if rand_int == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0, 2)))
            elif rand_int == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0, 2)))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            for i, dinausore in enumerate(dinosaures):
                if dinausore.rect.colliderect(obstacle.rect):
                    remove(i)

        user_input = pygame.key.get_pressed()

        for i, dinosaure in enumerate(dinosaures):
            if user_input[pygame.K_SPACE]:
                dinosaure.dino_jump = True
                dinosaure.dino_run = False

        score()
        background()
        clock.tick(30)
        pygame.display.update()


main()
