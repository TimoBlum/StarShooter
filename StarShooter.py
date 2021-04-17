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
wave = 1
shots = 0
kills = 0
lost = False

EntitySpaceShips = [pygame.image.load("pics/small.jpg"), pygame.image.load("pics/medium.jpg"),
                    pygame.image.load("pics/boss.jpg"), pygame.image.load("pics/god.jpg"),
                    pygame.image.load("pics/firerate.png"), pygame.image.load("pics/healer.png"),
                    pygame.image.load("pics/quadshot.png"), pygame.image.load("pics/nuke.png"),
                    pygame.image.load("pics/helper.png")]
spaceShip = pygame.image.load("playerShip.jpg")
strechedSpaceShip = pygame.transform.scale(spaceShip, (Pwh, Pwh))

for i in range(1, 70):
    entityDroprate.append("small")
for i in range(1, 80):
    entityDroprate.append("medium")
for i in range(1, 10):
    entityDroprate.append("boss")
for i in range(1, 7):
    entityDroprate.append("firerate")
for i in range(1, 6):
    entityDroprate.append("healer")
for i in range(1, 4):
    entityDroprate.append("quadshot")
for i in range(1, 7):
    entityDroprate.append("helper")
for i in range(1, 2):
    entityDroprate.append("god")
for i in range(1, 3):
    entityDroprate.append("rocket")


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
        self.medkits = 1
        self.boosts = 1

    def draw(self):
        pygame.draw.rect(win, self.color, self.rect)
        win.blit(strechedSpaceShip, self.rect)
        self.rect = (self.x, self.y, self.wh, self.wh)

    def move(self):
        global FPS, HP
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_f]:
            if self.boosts == 1:
                self.boosts -= 1
                self.timer = 600
            else:
                textOnScreen(xy//2, xy//2, "No more fire rate boosts", "", 20, color=(180, 180, 180))
        if keys[pygame.K_s]:
            if self.medkits == 1:
                self.medkits -= 1
                HP = 100
            else:
                textOnScreen(xy//2, xy//2, "No more Medkits", "", 20, color=(180, 180, 180))
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
        global shots
        if self.timer <= 0:
            if yn(Frame, 10):
                if not self.quadshot:
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, 0))
                    shots += 1
                else:
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, 0, pic="pics/laser2.png"))
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, 1, pic="pics/laser2.png"))
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, 2, pic="pics/laser2.png"))
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, -1, pic="pics/laser2.png"))
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, -2, pic="pics/laser2.png"))
                    shots += 5
        elif self.timer >= 0:
            if yn(Frame, 5):
                if not self.quadshot:
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, 0, pic="pics/laser2.png"))
                    shots += 1
                else:
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, 0, pic="pics/laser2.png"))
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, 1, pic="pics/laser2.png"))
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, 2, pic="pics/laser2.png"))
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, -1, pic="pics/laser2.png"))
                    projectiles.append(projectile(self.x + self.wh // 2-(self.wh//10), self.y, -2, pic="pics/laser2.png"))
                    shots += 5


class Entity:
    def __init__(self, rank):
        global EntitySpaceShips
        self.rank = rank
        # TYPES OF ENEMIES
        self.vel = 1.5*random.random()
        if rank == "boss":
            self.w, self.h = 70, 70
            self.damage = 20
            self.health = 20
            self.maxhealth = 20
            self.color = [230, 0, 0]
            self.vel = 1.2*random.random()
            self.image = pygame.transform.scale(pygame.transform.rotate(EntitySpaceShips[2], 180), (self.w, self.h))
        elif rank == "medium":
            self.w, self.h = 50, 50
            self.health = 8
            self.maxhealth = 8
            self.damage = 8
            self.color = [255, 100, 100]
            self.vel = 1.5*random.random()
            self.image = pygame.transform.scale(pygame.transform.rotate(EntitySpaceShips[1], 180), (self.w, self.h))
        elif rank == "small":
            self.w, self.h = 30, 30
            self.health = 2
            self.maxhealth = 2
            self.damage = 3
            self.color = [255, 150, 150]
            self.vel = random.randint(1, 2)
            self.image = pygame.transform.scale(pygame.transform.rotate(EntitySpaceShips[0], 180), (self.w, self.h))
        elif rank == "god":
            self.w, self.h = 100, 100
            self.health = 45
            self.maxhealth = 45
            self.damage = 50
            self.color = [0, 0, 0]
            self.vel = 0.6
            self.image = pygame.transform.scale(pygame.transform.rotate(EntitySpaceShips[3], 180), (self.w, self.h))
        elif rank == "rocket":
            self.w, self.h = 20, 80
            self.health = 2
            self.maxhealth = 2
            self.damage = 50
            self.color = [0, 0, 0]
            self.vel = 2
            self.image = pygame.transform.scale(pygame.transform.rotate(EntitySpaceShips[7], 180), (self.w, self.h))
        elif rank == "firerate":
            self.w, self.h = 40, 40
            self.health = 5
            self.maxhealth = 5
            self.damage = 0
            self.color = (0, 0, 255)
            self.vel = 1.3
            self.image = pygame.transform.scale(EntitySpaceShips[4], (self.w, self.h))
        elif rank == "healer":
            self.w, self.h = 40, 40
            self.health = 5
            self.maxhealth = 5
            self.damage = 0
            self.color = (0, 255, 0)
            self.vel = 1.3
            self.image = pygame.transform.scale(EntitySpaceShips[5], (self.w, self.h))
        elif rank == "quadshot":
            self.w, self.h = 40, 40
            self.health = 5
            self.maxhealth = 5
            self.damage = 0
            self.color = (0, 255, 0)
            self.vel = 1.3
            self.image = pygame.transform.scale(EntitySpaceShips[6], (self.w, self.h))
        elif rank == "helper":
            self.w, self.h = 50, 50
            self.health = 5
            self.maxhealth = 5
            self.damage = 0
            self.color = [255, 100, 100]
            self.vel = 1.5
            self.image = pygame.transform.scale(pygame.transform.rotate(EntitySpaceShips[8], 180), (self.w, self.h))

        self.x = random.randint(0, xy - self.w)
        self.y = 0
        self.rect = (self.x, self.y, self.w, self.h)
        self.strafetime = random.randint(30, 60)
        self.timer = 0
        self.rl = 0
        self.firsttime = True

    def draw(self):
        self.removeIfDead()
        self.rect = (self.x, self.y, self.w, self.h)
        pygame.draw.rect(win, self.color, self.rect)
        if self.health != self.maxhealth:
            if self.rank == "god":
                displayhealthbar((self.x+self.w//2, self.y), self.health/self.maxhealth, 2)
            else:
                displayhealthbar((self.x+self.w//2, self.y), self.health/self.maxhealth, 1.5)
        win.blit(self.image, self.rect)

    def move(self):
        if self.rank != "rocket":
            if yn(Frame, self.strafetime):
                self.timer = 60
                self.rl = random.randint(-1, 1)
            if self.timer >= 0:
                if self.rl == -1 and self.x >= 0:
                    self.x -= 1
                elif self.rl == 1 and self.x+self.h <= xy:
                    self.x += 1
        self.y += self.vel

    def removeIfDead(self):
        """If it dies, it is removed"""
        global HP, winColor, FPS, kills
        if self.health <= 0:
            if self.rank == "firerate":
                if P.boosts == 1:
                    P.timer = 600
                else:
                    P.boosts += 1

            if self.rank == "healer":
                if P.medkits == 1:
                    HP = 100
                else:
                    P.medkits += 1

            if self.rank == "quadshot":
                P.quadshot = True
                P.quadshottimer = 300
                FPS = 100

            if self.rank == "helper":
                if self.firsttime:
                    self.image = pygame.transform.rotate(self.image, 180)
                    self.firsttime = False
                self.y -= self.vel*3
                if self.y <= 0:
                    del enemies[findPlace(self, enemies)]
                if yn(Frame, 5):
                    projectiles.append(projectile(self.x+self.w+2, self.y+self.h//2, 8, yvel=0, r=True, l=False))
                    projectiles.append(projectile(self.x-42, self.y+self.h//2, -8, yvel=0, r=False, l=True))
            else:
                del enemies[findPlace(self, enemies)]
            kills += 1


class projectile:
    def __init__(self, x, y, xvel, yvel=8, damage=1, pic="pics/laser.png", r=False, l=False):
        """things to shoot at enemies"""
        self.x = x
        self.y = y
        self.damage = damage
        self.num = num
        self.yvel = yvel
        self.xvel = xvel
        self.pic = pic
        self.image = pygame.image.load(self.pic)
        if r == False and l == False:
            self.w = 10
            self.h = 40
            self.strechedImage = pygame.transform.scale(pygame.transform.rotate(self.image, 90), (self.w, self.h))
        elif r == True and l == False:
            self.w = 40
            self.h = 10
            self.strechedImage = pygame.transform.scale(self.image, (self.w, self.h))
        elif r == False and l == True:
            self.w = 40
            self.h = 10
            self.strechedImage = pygame.transform.scale(pygame.transform.rotate(self.image, 180), (self.w, self.h))
        self.rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)

    def draw(self):
        self.rect = (self.x, self.y, self.w, self.h)
        self.removeIfDead()
        pygame.draw.rect(win, (255, 0, 0), self.rect)
        win.blit(self.strechedImage, self.rect)

    def removeIfDead(self):
        """If it dies, it is removed"""
        if self.y < 0:
            del projectiles[findPlace(self, projectiles)]

    def move(self):
        self.y -= self.yvel
        self.x += self.xvel


# CLASSES CLASSES CLASSES


P = Player((0, 255, 0))
enemies = [Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)]),
           Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)]),
           Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)]),
           Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)]),
           Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)]),
           Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)])]


def textOnScreen(x, y, text1, text2, big, color=(220, 200, 200)):
    font = pygame.font.Font('freesansbold.ttf', big)
    txt = str(text1) + str(text2)
    text = font.render(txt, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    win.blit(text, textRect)


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
    width2 = HP * ((10*big*4)-8)
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


# REDRAW GAME WINDOW


def redrawWin():
    global Frame, HP, winColor, FPS, lost
    if not lost:
        win.fill(winColor)
        pygame.draw.line(win, (230, 230, 230), (P.x + P.wh // 2, P.y), (P.x + P.wh // 2, 0))

        textOnScreen(xy//2, 30, "Wave Nr. ", str(wave), 28)
        textOnScreen(xy//13, 30, "Medkits availiable: ", P.medkits, 15, color=(255, 80, 80))
        textOnScreen(xy//10+4, 50, "Fire rate boosts availiable: ", P.boosts, 15, color=(255, 80, 80))

        # Hitting enemies and enemies hitting your base
        if projectiles:
            for p in projectiles:
                p.draw(), p.move()
        P.move(), P.draw()
        for e in enemies:
            e.move(), e.draw()
            for p in projectiles:
                if detect(pygame.rect.Rect(p.rect), pygame.rect.Rect(e.rect)):
                    e.health -= p.damage
                    del projectiles[findPlace(p, projectiles)]
            if e.y + e.h >= xy:
                HP -= e.damage
                del enemies[findPlace(e, enemies)]

        displayhealthbar((P.x+P.wh//2, P.y), HP/100, 3)
        if HP <= 0:
            lost = True
    if lost:
        textOnScreen(xy//2, xy//2, "YOU LOST", "", 40, color=(255, 0, 0))
        textOnScreen(xy//12, 100, "enemies killed: ", str(kills), 18)
        textOnScreen(xy//15, 130, "Shots fired: ", str(shots), 18)
    pygame.display.update()
    Frame += 1


# MAIN


def main():
    global run, wave
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        if not enemies:
            for i in range(0, wave+8):
                enemies.append(Entity(entityDroprate[random.randint(0, len(entityDroprate) - 1)]))
            wave += 1

        if run:
            redrawWin()


main()
