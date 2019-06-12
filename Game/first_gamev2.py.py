"""
Make a simple apple colecting game using pygame.

Using pygame, create a game that uses classes and loops to make
a character that moves left and right, jumps, and colects "apples"
that falls from a tree to gain points.

Benjamin Holeman
"""
import pygame
import random
pygame.init()

win = pygame.display.set_mode((500,480))

pygame.display.set_caption("First Game")

walkRight = [
    pygame.image.load('R1.png'), pygame.image.load('R2.png'),
    pygame.image.load('R3.png'), pygame.image.load('R4.png'),
    pygame.image.load('R5.png'), pygame.image.load('R6.png'),
    pygame.image.load('R7.png'), pygame.image.load('R8.png'),
    pygame.image.load('R9.png')
    ]
walkLeft = [
    pygame.image.load('L1.png'), pygame.image.load('L2.png'),
    pygame.image.load('L3.png'), pygame.image.load('L4.png'),
    pygame.image.load('L5.png'), pygame.image.load('L6.png'),
    pygame.image.load('L7.png'), pygame.image.load('L8.png'),
    pygame.image.load('L9.png')
    ]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

score = 0

class player(object):
    """Class that is used to define the player."""

    def __init__(self, x, y, width,height):
        """
        All defining variables of player.

        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.hitbox = (self.x + 15, self.y + 5, 35, 60)

    def draw(self,win):
        """
        def that brings player into game.

        """
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.left:
            win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[self.walkCount//3], (self.x,self.y))
            self.walkCount +=1
        else:
            win.blit(char, (self.x,self.y))
        self.hitbox = (self.x + 15, self.y + 5, 35, 60)
        #pygame.draw.rect(win, (255,0,0), (self.hitbox),2)

    def hit(self):
        """
        def that makes apple collectible.

        """
        print('apple get')
        

class Apple():
    """Class that is used to make an apple and drop it"""
    
    def __init__(self,x,y,radius,color):
        """
        All defining variables of apple.

        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 10
        self.hitbox = (self.x + -10, self.y + -10, 20, 20)

    def draw(self,win):
        """
        def that brings apple into game.

        """
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
        self.hitbox = (self.x + -10, self.y + -10, 20, 20)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def hit(self):
        """
        def that helps apple be collectible.

        """
        print('apple get')
        pass

 
class tree(pygame.sprite.Sprite):
    """Class used to hide and help drop the apple using random"""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.xmin = 96
        self.xmax = 106
        self.xRange = random.randrange(self.xmin, self.xmax)
        self.ymin = 65
        self.ymax = 75
        self.yRange = random.randrange(self.ymin, self.ymax)
    def draw(self, win):
        """
        def that brings tree into game.

        """
        win.blit(pygame.image.load("tree_top.png"),(self.x, self.y))

def redrawGameWindow():
        """
        def that draws the window and everything on it.

        """
    win.blit(bg, (0,0))
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    win.blit(text, (390, 10))
    man.draw(win)
    for apple in apples:
        apple.draw(win)
    tree.draw(win)
    pygame.display.update()


#mainloop
font = pygame.font.SysFont('arial', 30, True)
man = player(300, 410, 64, 64)
apples = []
tree = tree(36, 55, 214, 238) 
run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for apple in apples:
        if (apple.y - apple.radius < man.hitbox[1] + man.hitbox[3]
            and apple.y + apple.radius > man.hitbox[1]
):
            if (apple.x + apple.radius > man.hitbox[0]
                and apple.x - apple.radius < man.hitbox[0] + man.hitbox[2]
):
                man.hit()
                score += 1
                apples.pop(apples.index(apple))
            
        if apple.y < 500 and apple.y > 0:
            apple.y += apple.vel
        else:
            apples.pop(apples.index(apple))

    if random.randrange(0, 100) < 5:
        apples.append(Apple(tree.xRange, tree.yRange, 5, (255, 0, 0)))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
    else:
        man.right = False
        man.left = False
        man.walkCount = 0
        
    if not(man.isJump):
        if keys[pygame.K_SPACE]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
            
    redrawGameWindow()

pygame.quit()
