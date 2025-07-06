import pygame, sys, time
from settings import *
from sprites import BG, Ground, Plane, Obstacle

class Game:
    def __init__(self):

        #setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()

        #sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        #scale factor
        bg_height = pygame.image.load("graphics/environment/background.png").get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height
        
        #sprite setup
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.plane = Plane(self.all_sprites, self.scale_factor / 1.8)

        #timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        #text
        self.font = pygame.font.Font("graphics/font/BD_Cartoon_Shout.ttf", 30)
        self.score = 0

    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask)\
        or self.plane.rect.top <= 0:
            pygame.quit()
            sys.exit()

    def display_score(self):
        self.score = pygame.time.get_ticks() // 1000

        score_surf = self.font.render(str(self.score), True, "Black")
        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 10))
        self.display_surface.blit(score_surf, score_rect)

    def run(self):
        last_time = time.time()
        while True:

            #delta time
            dt = time.time() - last_time
            last_time = time.time()

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.plane.jump()
                
                if event.type == self.obstacle_timer:
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor)

            #game logic
            self.display_surface.fill("black")
            self.all_sprites.update(dt)
            self.collisions()
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            pygame.display.update()
            self.clock.tick(FRAMERATE)

if __name__ == "__main__":
    game = Game()
    game.run()