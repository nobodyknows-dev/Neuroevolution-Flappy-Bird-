import pygame, random
from Non_Linear_AI import NonLinearNeuron

pygame.init()

'''
    Optimal weights to try
        child.AI.w1 = 1.0223058113521017
        child.AI.w2 = -0.01550866245161861
        child.AI.w3 = -0.09952109886054405
        child.AI.w4 = -1.0002656777172478
        child.AI.w5 = -0.21259455954435474
        child.AI.b  = -0.10831735706516332
'''

class Bird:
    def __init__(self, screen, transparency):
        self.x = 50
        self.y = 280
        self.vel_y = 0
        self.jump_timer = 20
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.AI = NonLinearNeuron()
        self.score = 0

        self.surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.transparency = transparency
        self.color = (0, 255, 100)

    def draw(self):
        self.surf.fill((0, 0, 0))
        pygame.draw.rect(self.surf, self.color, pygame.Rect(0, 0, 40, 40))
        self.surf.set_alpha(self.transparency)

        self.screen.blit(self.surf, (self.x, self.y))

    def update(self, pipe, dt):
        self.vel_y += 0.5 * 60 * dt
        self.jump_timer -= 1 * 60 * dt

        pred = self.AI.prediction(self.y/600, self.vel_y/20, pipe.x/600, pipe.h1/600, pipe.gap/600)
        if pred > 0.5 and self.jump_timer < 0:
            self.vel_y = -10
            self.jump_timer = 20

        self.y += self.vel_y * 60 * dt
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

    def update(self, dt):
        self.x -= 5 * 60 * dt

        self.rect1.topleft = (self.x, self.y1)
        self.rect2.topleft = (self.x, self.y2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Flappy AI?")
        self.clock = pygame.time.Clock()
        self.time = pygame.time.get_ticks()

        self.bird = []
        for _ in range(100):
            self.bird.append(Bird(self.screen, 50))
        self.new_bird = []
        self.dead_bird = []

        self.pipe_timer = 0
        self.pipe_list = [Pipe(self.screen)]

        self.score = 0
        self.gen = 1
        self.high_score = 0
        self.events = pygame.event.get()
        self.focused = False
        self.font = pygame.font.SysFont("Calibri", 20, True)
        self.font1 = pygame.font.SysFont("Calibri", 40, True)
        self.font2 = pygame.font.SysFont("Calibri", 10, True)

    def pipe_sys(self, dt):
        if len(self.dead_bird) >= 100:
            self.dead_bird.sort(key=lambda b:b.score, reverse=True)
            self.bird = self.dead_bird[:10]
            self.next_gen()
            self.gen += 1
            if self.high_score < self.score: self.high_score = self.score
            self.score = 0
            self.dead_bird = []

        if self.time - self.pipe_timer >= 1200:
            self.pipe_list.append(Pipe(self.screen))
            self.pipe_timer = self.time

        for pipe in self.pipe_list[:]:
            pipe.draw()
            pipe.update(dt)

            if pipe.x <= -40:
                self.pipe_list.remove(pipe)
                self.score += 1
                for bird in self.bird:
                    bird.score += 1

        for bird in self.bird:
            if self.pipe_list[0].rect1.colliderect(bird.rect) or self.pipe_list[0].rect2.colliderect(bird.rect):
                self.dead_bird.append(bird)
                self.bird.remove(bird)
                self.focus()

    def focus(self):
        if len(self.bird) > 0:
            if not self.focused:
                for bird in self.bird:
                    bird.transparency = 50
                    bird.color = (0, 255, 100)
                
            else:
                for bird in self.bird:
                    bird.transparency = 5
                self.bird[-1].transparency = 255
                self.bird[-1].color = (0, 0, 0)

    def next_gen(self):
        for bird in self.bird:
            bird.vel_y = 0
            bird.x = 50
            bird.y = 280
            bird.color = (0, 255, 100)
            bird.score = 0

            for _ in range(9):
                child = Bird(self.screen, 50)

                child.AI.w1 = bird.AI.w1 + random.uniform(-0.1, 0.1)
                child.AI.w2 = bird.AI.w2 + random.uniform(-0.1, 0.1)
                child.AI.w3 = bird.AI.w3 + random.uniform(-0.1, 0.1)
                child.AI.w4 = bird.AI.w4 + random.uniform(-0.1, 0.1)
                child.AI.w5 = bird.AI.w5 + random.uniform(-0.1, 0.1)
                child.AI.b  = bird.AI.b  + random.uniform(-0.1, 0.1)

                self.new_bird.append(child)
        
        self.bird.extend(self.new_bird)
        self.new_bird = []
        self.pipe_list = [Pipe(self.screen)]
        self.pipe_timer = self.time
        self.focus()

    def draw_text(self, text, x, y, color, font):
        img = font.render(text, True, color)
        self.screen.blit(img, (x, y))

    def draw_ui(self):
        self.draw_text(f"High Score : {self.high_score}", 10, 10, (0, 0, 0), self.font)
        self.draw_text(f"Score : {self.score}", 10, 30, (0, 0, 0), self.font)
        self.draw_text(f"Gen : {self.gen}", 10, 50, (0, 0, 0), self.font)
        self.draw_text(f"Alive : {len(self.bird)}", 10, 70, (0, 0, 0), self.font)
        self.draw_text("'M' : Focus mode", 200, 10, (0, 0, 0), self.font)
        if len(self.bird) > 0:
            self.draw_text(f"w1 : {self.bird[0].AI.w1}", 450, 10, (0, 0, 0), self.font2)
            self.draw_text(f"w2 : {self.bird[0].AI.w2}", 450, 20, (0, 0, 0), self.font2)
            self.draw_text(f"w3 : {self.bird[0].AI.w3}", 450, 30, (0, 0, 0), self.font2)
            self.draw_text(f"w4 : {self.bird[0].AI.w4}", 450, 40, (0, 0, 0), self.font2)
            self.draw_text(f"w5 : {self.bird[0].AI.w5}", 450, 50, (0, 0, 0), self.font2)
            self.draw_text(f"b : {self.bird[0].AI.b}", 450, 60, (0, 0, 0), self.font2)

    def update(self):
        run = True
        while run:
            self.events = pygame.event.get()
            dt = self.clock.tick(60) / 1000.0
            self.screen.fill((255, 255, 255))
            self.time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.focused = not self.focused
                        self.focus()

            if self.focused:
                self.draw_text("Focused on one", 200, 300, (220, 220, 220), self.font1)

            for bird in self.bird:
                bird.draw()
                bird.update(self.pipe_list[0] if self.pipe_list[0].x > 10 else self.pipe_list[1], dt)

            self.pipe_sys(dt)
            self.draw_ui()

            pygame.display.update()

        print(vars(self.bird[0].AI), self.bird[0].score)
        pygame.quit()

Game().update()
