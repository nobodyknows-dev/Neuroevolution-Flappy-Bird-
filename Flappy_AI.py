import pygame, random
from Non_Linear_AI import NonLinearNeuron

pygame.init()

class Bird:
    def __init__(self, screen):
        self.x = 50
        self.y = 280
        self.vel_y = 0
        self.jump_timer = 20
        self.screen = screen
        self.rect = pygame.Rect(self.x, self.y, 40, 40)
        self.AI = NonLinearNeuron()
        self.score = 0

    def draw(self):
        pygame.draw.rect(self.screen, (0, 255, 100), self.rect)

    def update(self, pipe):
        self.vel_y += 0.5
        self.jump_timer -= 1

        pred = self.AI.prediction(self.y/600, self.vel_y/20, pipe.x/600, pipe.h1/600, pipe.gap/600)
        if pred > 0.5 and self.jump_timer < 0:
            self.vel_y = -10
            self.jump_timer = 20

        self.y += self.vel_y
        self.y = min(560, max(0, self.y))
        self.rect.topleft = (self.x, self.y)

class Pipe:
    def __init__(self, screen):
        self.screen = screen
        self.x = 600
        self.width = 40

        self.y1 = 0
        self.h1 = random.randint(100, 300)

        self.gap = random.randint(150, 200)

        self.y2 = self.h1 + self.gap
        self.h2 = 600 - self.y2

        self.rect1 = pygame.Rect(self.x, self.y1, self.width, self.h1)
        self.rect2 = pygame.Rect(self.x, self.y2, self.width, self.h2)

    def draw(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect1)
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect2)

    def update(self):
        self.x -= 5

        self.rect1.topleft = (self.x, self.y1)
        self.rect2.topleft = (self.x, self.y2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 600))
        self.clock = pygame.time.Clock()
        self.time = pygame.time.get_ticks()

        self.bird = []
        for _ in range(1000):
            self.bird.append(Bird(self.screen))
        self.new_bird = []
        self.dead_bird = []

        self.pipe_timer = 0
        self.pipe_list = [Pipe(self.screen)]

    def pipe_sys(self):
        if len(self.dead_bird) >= 1000:
            self.dead_bird.sort(key=lambda b:b.score, reverse=True)
            self.bird = self.dead_bird[:1]
            self.next_gen()
            self.dead_bird = []

        if self.time - self.pipe_timer >= 1000:
            self.pipe_list.append(Pipe(self.screen))
            self.pipe_timer = self.time

        for pipe in self.pipe_list[:]:
            pipe.draw()
            pipe.update()

            if pipe.x <= 50:
                self.pipe_list.remove(pipe)
                for bird in self.bird:
                    bird.score += 1

        for bird in self.bird:
            if self.pipe_list[0].rect1.colliderect(bird.rect) or self.pipe_list[0].rect2.colliderect(bird.rect):
                self.dead_bird.append(bird)
                self.bird.remove(bird)

    def next_gen(self):
        for bird in self.bird:
            bird.vel_y = 0
            bird.x = 50
            bird.y = 280
              
        for bird in self.bird:
            for _ in range(999):
                child = Bird(self.screen)

                child.AI.w1 = bird.AI.w1 + random.uniform(-0.1, 0.1)
                child.AI.w2 = bird.AI.w2 + random.uniform(-0.1, 0.1)
                child.AI.w3 = bird.AI.w3 + random.uniform(-0.1, 0.1)
                child.AI.w4 = bird.AI.w4 + random.uniform(-0.1, 0.1)
                child.AI.w5 = bird.AI.w5 + random.uniform(-0.1, 0.1)
                child.AI.b  = bird.AI.b  + random.uniform(-0.1, 0.1)

                self.new_bird.append(child)
        
        self.bird.extend(self.new_bird)
        for bird in self.bird:
            bird.score = 0

        self.new_bird = []
        self.pipe_list = [Pipe(self.screen)]
        self.pipe_timer = self.time

    def draw_text(self, text, x, y):
        font = pygame.font.SysFont("Calibri", 40, True)
        img = font.render(text, True, (200, 200, 200))
        self.screen.blit(img, (x, y))

    def update(self):
        run = True
        while run:
            self.screen.fill((255, 255, 255))
            self.time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.draw_text(f"Alive : {len(self.bird)}", 250, 290)

            for bird in self.bird:
                bird.draw()
                bird.update(self.pipe_list[0])

            self.pipe_sys()

            pygame.display.update()
            self.clock.tick(60)

        print(vars(self.bird[0].AI), self.bird[0].score)
        pygame.quit()

Game().update()
