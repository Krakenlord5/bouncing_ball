import pygame, sys, time
from random import choice, randint
from debug import debug

S_WIDTH = 600
S_HEIGHT = 600
FPS = 600
BALL_SIZE = 60

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.rect = self.image.get_rect(midbottom = (S_WIDTH // 2, S_HEIGHT))
        self.speed = 500
        self.gravity = self.gravity_start = -600
        self.weight = 0
        self.direction = self.direction_start = 600
        self.do_bounce = True
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.boing = pygame.mixer.Sound("C:\\Users\MSI\\Documents\\- Python codes\\audio\\boing2.wav")
        self.boing.set_volume(0.2)

    def check_collision(self):
        if self.rect.bottom > S_HEIGHT and self.gravity > 0:
            self.boing.play()
            self.weight += 30
            self.gravity = self.gravity_start + self.weight
            if -30 <= self.gravity <= 0 or self.gravity > 0: 
                self.gravity = 0
                self.speed = 0
                self.rect.bottom = S_HEIGHT
        if self.rect.top < 0 and self.gravity <= 0:
            self.boing.play()
            self.gravity = 200
            self.gravity_start = -600
        if self.rect.left < 0 and self.direction < 0: 
            self.boing.play()
            self.weight += 40
            self.direction = self.direction_start - self.weight
            if -30 <= self.direction < 0:
                self.direction = 0
                self.weight = 0
                self.rect.left = 0
        if self.rect.right > S_WIDTH and self.direction > 0:
            self.boing.play()
            self.weight += 40
            self.direction = -(self.direction_start) + self.weight
            if 0 < self.direction <= 30:
                self.direction = 0
                self.weight = 0
                self.rect.right = S_WIDTH

    def bounce(self, dt):
        if self.do_bounce:
            self.gravity += self.speed * dt
            self.pos.y += self.gravity * dt
            self.pos.x += self.direction * dt
            self.rect.y = round(self.pos.y)
            self.rect.x = round(self.pos.x)

    def grab(self, dx, dy):
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.do_bounce = False
                self.rect.center = pygame.mouse.get_pos()
                if self.rect.left < 0: self.rect.left = 0
                if self.rect.right > S_WIDTH: self.rect.right = S_WIDTH
                if self.rect.top < 0: self.rect.top = 0
                if self.rect.bottom > S_HEIGHT: self.rect.bottom = S_HEIGHT
                self.pos = pygame.math.Vector2(self.rect.topleft)
                self.gravity = self.gravity_start = dy
                if 0 < self.gravity_start < 350:
                    self.gravity_start = S_HEIGHT - self.rect.y
                if -350 < self.gravity_start < 0:
                    self.gravity_start = self.rect.y - S_HEIGHT 
                if self.gravity_start * -1 < self.gravity_start:
                    self.gravity_start = -(self.gravity_start)
                self.speed = 500
                self.weight = 0
                self.direction = self.direction_start = dx
                if self.direction_start * -1 > self.direction_start:
                    self.direction_start = -(self.direction_start)
            else:
                self.do_bounce = True
        else:
            self.do_bounce = True

    def update(self, dt, dx, dy):
        pygame.draw.circle(screen, "red", self.rect.center, BALL_SIZE // 2)
        self.check_collision()
        self.bounce(dt)
        self.grab(dx, dy)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
    clock = pygame.time.Clock()

    ball = pygame.sprite.GroupSingle(Ball())
    dx = dy = 0
    
    previous_time = time.time()
    while True:
        dt = time.time() - previous_time
        previous_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and FPS > 50: FPS -= 50
                if event.key == pygame.K_e and FPS < 1000: FPS += 50
                    
            if event.type == pygame.MOUSEMOTION:
                dx, dy = event.rel
                dx *= 70
                dy *= 70
                
        screen.fill("black")
        ball.draw(screen)
        ball.update(dt, dx, dy)
        debug(FPS)
        debug(dy, 40)
        debug(dx, 70)

        pygame.display.update()
        clock.tick(FPS)