import pygame, random

pygame.init()

xy = 1000
win = pygame.display.set_mode((xy, xy))
run = True
Frame = 0
clock = pygame.time.Clock()
projectiles = []
enemyProjectiles = []
droprate = []
FPS = 60
num = 0
winColor = [255, 255, 255]
HP = 100

for i in range(1, 70):
    droprate.append("small")
for i in range(1, 80):
    droprate.append("medium")
for i in range(1, 10):
    droprate.append("boss")
for i in range(1, 10):
    droprate.append("firerate")
droprate.append("god")


# CLASSES CLASSES CLASSES


class Player:
    def __init__(self, color):
        self.wh = 30
        self.x = xy // 2
        self.y = xy - 2 * self.wh
        self.color = color
        self.rect = (self.x, self.y, self.wh, self.wh)
        self.vel = 4
        self.firerate = 10
        self.time = 0

    def draw(self):
        pygame.draw.rect(win, self.color, self.rect)
        self.rect = (self.x, self.y, self.wh, self.wh)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_d] and self.x < xy - self.wh - self.vel:
            self.x += self.vel
        if keys[pygame.K_a] and self.x > self.vel:
            self.x -= self.vel

        self.time -= 1  # timer that is being run down
        print(self.time)
        if self.time >= 0:
            self.color = (200, 0, 0)
        if self.time <= 0:
            self.color = (0, 255, 0)

    def shoot(self):
        if self.time <= 0:
            if yn(Frame, 10):
                projectiles.append(projectile(self.x + self.wh // 3, self.y, True))
        elif self.time >= 0:
            if yn(Frame, 5):
                projectiles.append(projectile(self.x + self.wh // 3, self.y, True))


class Entity:
    def __init__(self, rank):
        self.rank = rank

        # TYPES OF ENEMIES
        if rank == "firerate":
            self.wh = 40
            self.health = 7
            self.color = (173, 216, 230)
            self.sh = 1
            self.vel = 1.5*random.random()
        elif rank == "boss":
            self.wh = 70
            self.health = 25
            self.color = [230, 0, 0]
            self.sh = 20
            self.vel = 1.2*random.random()
        elif rank == "medium":
            self.wh = 50
            self.health = 13
            self.color = [255, 100, 100]
            self.sh = 10
            self.vel = 1.5*random.random()
        elif rank == "small":
            self.wh = 30
            self.health = 3
            self.color = [255, 150, 150]
            self.sh = 5
            self.vel = 2*random.random()
        elif rank == "god":
            self.wh = 50
            self.health = 30
            self.sh = 1
            self.color = [0, 0, 0]
            self.vel = 1.5*random.random()

        self.x = random.randint(0, xy - self.wh)
        self.y = 0
        self.rect = (self.x, self.y, self.wh, self.wh)
        self.shadows = [self.rect]
        self.strafetime = random.randint(30, 60)
        self.timer = 0
        self.rl = 0

        # SHADOWING
        if not self.rank == "firerate" or"god":
            for s in range(self.sh):
                self.shadows.append(self.rect)

    def draw(self):
        self.removeIfDead()
        del self.shadows[0]
        self.shadows.append(self.rect)
        c = [255, 255, 255]
        for s in self.shadows:
            pygame.draw.rect(win, c, s)
            c[1] -= 8
            c[2] -= 8
        self.rect = (self.x, self.y, self.wh, self.wh)
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        if yn(Frame, self.strafetime):
            self.timer = 60
            self.rl = random.randint(-1, 1)
        if self.timer >= 0:
            if self.rl == -1 and self.x >= 0:
                self.x -= 1
            elif self.rl == 1 and self.x+self.wh <= xy:
                self.x += 1
        self.y += self.vel

    def removeIfDead(self):
        """If it dies, it is removed"""
        if self.health <= 0:
            if self.rank == "firerate":
                P.time = 600
            del enemies[findPlace(self, enemies)]


class projectile:
    def __init__(self, x, y, ud):
        """things to shoot at enemies"""
        self.x = x
        self.y = y
        self.wh = 10
        self.damage = 1
        self.num = num
        self.ud = ud
        self.shadows = []
        self.rect = pygame.rect.Rect(self.x, self.y, self.wh, self.wh)
        for s in range(5):
            self.shadows.append(self.rect)

    def draw(self):
        self.rect = (self.x, self.y, self.wh, self.wh)
        del self.shadows[0]
        self.shadows.append(self.rect)
        grey = [255, 255, 255]
        for s in self.shadows:
            pygame.draw.rect(win, grey, s)
            grey[1] -= 50
            grey[2] -= 50
        pygame.draw.rect(win, (255, 0, 0), self.rect)

    def move(self):
        if self.ud:
            self.y -= 8
        else:
            self.y += 8


# CLASSES CLASSES CLASSES


P = Player((0, 255, 0))
enemies = [Entity(droprate[random.randint(0, len(droprate) - 1)]),
           Entity(droprate[random.randint(0, len(droprate) - 1)])]


def detect(rect1, rect2):
    """useless, i know"""
    if rect1.colliderect(rect2):
        return True


def yn(a, c):
    # decide if something, whether float or int is the same number
    b = a // c
    bb = a / c
    if b - bb == 0:
        return True
    else:
        return False


def displayhealthbar(point, HP, big):
    """Looks pretty bad, but it just makes a health bar"""
    x1 = point[0] - 20*big
    y1 = point[1] - 40*(0.4*big)
    width1 = 10*big*4
    height1 = 30*(0.4*big)
    x2 = point[0] - 20 * big + 4
    y2 = point[1] - 40*(0.4*big) + 4
    width2 = HP * (10*big*4)-8
    height2 = 30*(0.4*big)-8
    pygame.draw.rect(win, (230, 230, 230), (x1, y1, width1, height1))
    pygame.draw.rect(win, (0, 255, 0), (x2, y2, width2, height2))


def findPlace(s, lst):
    """returns the place in which the item is found in the given list"""
    counter = 0
    for i in lst:
        if i == s:
            return counter
        else:
            counter += 1


def redrawWin():
    global Frame, HP, winColor
    win.fill(winColor)
    pygame.draw.line(win, (230, 230, 230), (P.x + P.wh // 2, P.y), (P.x + P.wh // 2, 0))
    if projectiles:
        for p in projectiles:
            p.draw(), p.move()
    for e in enemies:
        e.move(), e.draw()
        for p in projectiles:
            if detect(pygame.rect.Rect(p.rect), pygame.rect.Rect(e.rect)):
                e.health -= 1
                del projectiles[findPlace(p, projectiles)]
        if e.y + e.wh >= xy:
            HP -= e.health
            winColor[1] -= e.health
            winColor[2] -= e.health
            del enemies[findPlace(e, enemies)]

    displayhealthbar((P.x+P.wh//2, P.y), HP/100, 3)
    P.move(), P.draw()
    if HP <= 0:
        win.fill((255, 0, 0))
    pygame.display.update()
    Frame += 1


# MAIN


def main():
    global run
    diff = 2
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        if not enemies:
            for i in range(0, diff):
                enemies.append(Entity(droprate[random.randint(0, len(droprate) - 1)]))
            diff += 1
        if run:
            redrawWin()


main()
