import pygame, random

pygame.init()

xy = 1000
win = pygame.display.set_mode((xy, xy))
run = True
Frame = 0
clock = pygame.time.Clock()
projectiles = []
enemyProjectiles = []
entityDroprate = []
friendlyDroprate = []
FPS = 60
num = 0
winColor = [255, 255, 255]
HP = 100
Pwh = 50

EntitySpaceShips = [pygame.image.load("pics/small.jpg"), pygame.image.load("pics/medium.jpg"),
                    pygame.image.load("pics/boss.jpg"), pygame.image.load("pics/god.jpg"),
                    pygame.image.load("pics/firerate.png"), pygame.image.load("pics/healer.png"),
                    pygame.image.load("pics/quadshot.png")]
spaceShip = pygame.image.load("playerShip.jpg")
strechedSpaceShip = pygame.transform.scale(spaceShip, (Pwh, Pwh))

for i in range(1, 70):
    entityDroprate.append("small")
for i in range(1, 80):
    entityDroprate.append("medium")
for i in range(1, 10):
    entityDroprate.append("boss")
for i in range(1, 8):
    entityDroprate.append("firerate")
for i in range(1, 7):
    entityDroprate.append("healer")
for i in range(1, 5):
    entityDroprate.append("quadshot")
entityDroprate.append("god")

# CLASSES CLASSES CLASSES


class Player:
    def __init__(self, color):
        self.wh = Pwh
        self.x = xy // 2
        self.y = xy - 2 * self.wh
        self.color = color
        self.rect = (self.x, self.y, self.wh, self.wh)
        self.vel = 4
        self.firerate = 10
        self.timer = 0
        self.quadshot = False
        self.quadshottimer = 0

    def draw(self):
        pygame.draw.rect(win, self.color, self.rect)
        win.blit(strechedSpaceShip, self.rect)
        self.rect = (self.x, self.y, self.wh, self.wh)

    def move(self):
        global FPS
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_d] and self.x < xy - self.wh - self.vel:
            self.x += self.vel
        if keys[pygame.K_a] and self.x > self.vel:
            self.x -= self.vel

        if self.timer > 0:
            self.timer -= 1  # timer that is being run down
        if self.quadshot > 0:
            self.quadshottimer -= 1

        if self.quadshottimer <= 0:
            self.quadshot = False
            FPS = 60

    def shoot(self):
        if self.timer <= 0:
            if yn(Frame, 10):
                if not self.quadshot:
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, True, 0))
                else:
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, True, 0))
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, True, 1))
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, True, 2))
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, True, -1))
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, True, -2))
        elif self.timer >= 0:
            if yn(Frame, 5):
                if not self.quadshot:
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, True, 0))
                else:
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, True, 0))
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, True, 1))
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, True, 2))
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, True, -1))
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, True, -2))


class Entity:
    def __init__(self, rank):
        global EntitySpaceShips
        self.rank = rank
        # TYPES OF ENEMIES
        self.vel = 1.5*random.random()
        if rank == "boss":
            self.wh = 70
            self.damage = 20
            self.health = 17
            self.color = [230, 0, 0]
            self.vel = 1.2*random.random()
            self.image = pygame.transform.scale(pygame.transform.rotate(EntitySpaceShips[2], 180), (self.wh, self.wh))
        elif rank == "medium":
            self.wh = 50
            self.health = 8
            self.damage = 10
            self.color = [255, 100, 100]
            self.vel = 1.5*random.random()
            self.image = pygame.transform.scale(pygame.transform.rotate(EntitySpaceShips[1], 180), (self.wh, self.wh))
        elif rank == "small":
            self.wh = 30
            self.health = 2
            self.damage = 3
            self.color = [255, 150, 150]
            self.vel = 2*random.random()
            self.image = pygame.transform.scale(pygame.transform.rotate(EntitySpaceShips[0], 180), (self.wh, self.wh))
        elif rank == "god":
            self.wh = 50
            self.health = 40
            self.damage = 50
            self.color = [0, 0, 0]
            self.vel = 0.7
            self.image = pygame.transform.scale(pygame.transform.rotate(EntitySpaceShips[3], 180), (self.wh, self.wh))
        elif rank == "firerate":
            self.wh = 40
            self.health = 5
            self.damage = 0
            self.color = (0, 0, 255)
            self.vel = 1.3
            self.image = pygame.transform.scale(EntitySpaceShips[4], (self.wh, self.wh))
        elif rank == "healer":
            self.wh = 40
            self.health = 5
            self.damage = 0
            self.color = (0, 255, 0)
            self.vel = 1.3
            self.image = pygame.transform.scale(EntitySpaceShips[5], (self.wh, self.wh))
        elif rank == "quadshot":
            self.wh = 40
            self.health = 5
            self.damage = 0
            self.color = (0, 255, 0)
            self.vel = 1.3
            self.image = pygame.transform.scale(EntitySpaceShips[6], (self.wh, self.wh))

        self.x = random.randint(0, xy - self.wh)
        self.y = 0
        self.rect = (self.x, self.y, self.wh, self.wh)
        self.shadows = [self.rect]
        self.strafetime = random.randint(30, 60)
        self.timer = 0
        self.rl = 0

    def draw(self):
        self.removeIfDead()
        self.rect = (self.x, self.y, self.wh, self.wh)
        pygame.draw.rect(win, self.color, self.rect)
        win.blit(self.image, self.rect)

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
        global HP, winColor, FPS
        if self.health <= 0:
            if self.rank == "firerate":
                P.timer = 600
            if self.rank == "healer":
                HP = 100
                winColor = [255, 255, 255]
            if self.rank == "quadshot":
                P.quadshot = True
                P.quadshottimer = 300
                FPS = 100
            del enemies[findPlace(self, enemies)]


class projectile:
    def __init__(self, x, y, ud, xvel):
        """things to shoot at enemies"""
        self.x = x
        self.y = y
        self.wh = 10
        self.damage = 1
        self.num = num
        self.ud = ud
        self.shadows = []
        self.xvel = xvel
        self.rect = pygame.rect.Rect(self.x, self.y, self.wh, self.wh)
        for s in range(5):
            self.shadows.append(self.rect)

    def draw(self):
        self.rect = (self.x, self.y, self.wh, self.wh)
        self.removeIfDead()
        del self.shadows[0]
        self.shadows.append(self.rect)
        grey = [255, 255, 255]
        for s in self.shadows:
            pygame.draw.rect(win, grey, s)
            grey[1] -= 50
            grey[2] -= 50
        pygame.draw.rect(win, (255, 0, 0), self.rect)

    def removeIfDead(self):
        """If it dies, it is removed"""
        if self.y < 0:
            del projectiles[findPlace(self, projectiles)]

    def move(self):
        # Shooting up or down
        if self.ud:
            self.y -= 8
            self.x += self.xvel
        else:
            self.y += 8
            self.x += self.xvel

        # Bouncing off walls
        if self.x <= 0:
            self.xvel = - self.xvel
        if self.x + self.wh >= xy:
            self.xvel = - self.xvel


# CLASSES CLASSES CLASSES


P = Player((0, 255, 0))
enemies = [Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)]),
           Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)]),
           Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)]),
           Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)]),
           Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)]),
           Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)]),
           Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)]),
           Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)]),
           Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)]),
           Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)]),
           Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)]),
           Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)]),
           Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)])]


def decideIfEntity(name):
    if name in entityDroprate:
        return Entity(name)


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
    P.move(), P.draw()
    for e in enemies:
        e.move(), e.draw()
        for p in projectiles:
            if detect(pygame.rect.Rect(p.rect), pygame.rect.Rect(e.rect)):
                e.health -= 1
                del projectiles[findPlace(p, projectiles)]
        if e.y + e.wh >= xy:
            HP -= e.damage
            del enemies[findPlace(e, enemies)]

    displayhealthbar((P.x+P.wh//2, P.y), HP/100, 3)
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
                enemies.append(Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)]))
            diff += 1
        if run:
            redrawWin()


main()
