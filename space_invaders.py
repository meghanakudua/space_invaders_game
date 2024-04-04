import pygame
import time
import random
from pygame import mixer
pygame.init()

#displaying screen , background, icon
screen = pygame.display.set_mode((800,600))
background = pygame.image.load("space2.jpg")
pygame.display.set_caption('SPACE INVADERS')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#loading images for start and exit button
startimg = pygame.image.load('start-button.png')
exitimg = pygame.image.load('exit.png')

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==True and self.clicked== False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == False:
            self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

#placing the buttons on the screen
startbutton = Button(100, 200, startimg, 1.5)
exitbutton = Button(450, 200, exitimg, 1.5)

#defining game over message
#the text is stored in a list
# the text appears letter by letter
#pressing enter iterates over the list
def gameovermessage():
    font = pygame.font.Font('freesansbold.ttf',24)
    screen = pygame.display.set_mode([800,600])
    timer = pygame.time.Clock()
    messages = ['GAME OVERRR!!!','tjekek']
    snip = font.render('', True, 'white')
    x = font.render('', True, 'white')
    counter = 0
    speed = 3
    active_message = 0
    message = messages[0]
    done = False
    message1 = 'press enter to continue'
    x = font.render(message1[0:counter // speed], True, 'white')
    screen.blit(x,(10, 400))
    pygame.display.update()
    

    run = True
    while run:
        screen.fill('black')
        timer.tick(120)
        #pygame.draw.rect(screen, 'black', [0, 500, 800, 200])
        if counter < speed*len(message):
            counter +=1
        elif counter >= speed*len(message):
            done = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and done and active_message<len(messages)-1:
                    active_message = active_message + 1
                    done = False
                    message = messages[active_message]
                    counter = 0

        snip = font.render(message[0:counter // speed], True, 'white')
        screen.blit(snip,(10, 250))
        pygame.display.flip()

        if active_message == len(messages)-1:
            snip = font.render(message[0:counter // speed], True, 'white')
            screen.blit(snip,(10, 250))
            pygame.display.flip()
            #time.sleep(10)
            run = False

def gameloop():
    #loading images and placing the spaceship, enemy and bullet
    spaceshipimg = pygame.image.load('spaceship.png')
    spaceshipx = 370
    spaceshipy = 480
    spaceshipx_change=0

    alienimg=(pygame.image.load('alien.png'))
    alienx=(random.randint(0,735))
    alieny=(random.randint(50, 150))
    alienx_change=(0.3)
    alieny_change=(40)

    bulletimg = pygame.image.load('bullet.png')
    bulletx = 0
    bullety = 480
    bullety_change = 1
    bullet_state ="ready"

    #text for score
    score_change =0
    font = pygame.font.Font('freesansbold.ttf',32)
    scorex =10
    scorey = 10

    def score_display(x,y):
        score = font.render("score:"+str(score_change),True,(255,255,255))
        screen.blit(score ,(x, y))

    def spaceship(x,y):
        screen.blit(spaceshipimg ,(x, y))

    def alien(x,y):
        screen.blit(alienimg ,(x, y))

    def fire_bullet(x,y):
        global bullet_state
        bullet_state ="fire"
        screen.blit(bulletimg,(x+16, y+10))

    #function to check if collision has occured
    def isCollision(alienx, alieny, bulletx, bullety):
        distance = (((alienx-bulletx)**2)+((alieny-bullety)**2)**0.5)
        if distance < 27:
            return True
        else:
            return False
    
    running = True
    while running:
        screen.fill((50,100,200))
        screen.blit(background,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alieny = 2000
                spaceshipy = 2000
                bullety = 2000
                scorey=2000
                gameovermessage()
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    spaceshipx_change= -0.3
                if event.key == pygame.K_RIGHT:
                    spaceshipx_change = 0.3
                if event.key == pygame.K_SPACE:
                    if bullet_state =="ready":
                        bullet_sound = mixer.Sound('laser.wav')
                        bullet_sound.play()
                        bulletx = spaceshipx
                        fire_bullet(bulletx,bullety)
                        bullet_state ="fire"
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    spaceshipx_change= 0

        spaceshipx+= spaceshipx_change
        '''if spaceshipx <= 0:
            spaceshipx = 0
        elif spaceshipx >= 736:
            spaceshipx = 736'''

        #if spaceship and enemy are on the same level(ycoordinates)--game over
        if (((alieny-spaceshipy)**2)**0.5)<60:
            alieny = 2000
            spaceshipy = 2000
            bullety = 2000
            scorey=2000
            gameovermessage()
            running = False 

        #if spaceship crosses boundary--game over
        if spaceshipx <= 0 or spaceshipx >= 736:
            alieny = 2000
            spaceshipy = 2000
            bullety = 2000
            scorey=2000
            gameovermessage()
            running = False

        #respawning the enemy if it crosses the boundary
        alienx = alienx+alienx_change
        if alienx <= 0:
            alienx_change = 0.5
            alieny=alieny+alieny_change
        elif alienx >= 736:
            alienx_change =-0.5
            alieny=alieny+alieny_change
            
        # to check if collision has occured and updating score
        collision = isCollision(alienx,alieny,bulletx,bullety)
        if collision :
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bullety = 480
            bullet_state="ready"
            score_change = score_change+1
            print(score_change)
            alienx = random.randint(0,735)
            alieny = random.randint(50, 150)

            
             
        # changing the y coordinate of bullet back to its initial value if it crosses the boundary
        if bullety<=0:
            bullety = 480
            bullet_state="ready"
            
        if bullet_state =="fire":
            fire_bullet(bulletx,bullety)
            bullety = bullety - bullety_change

        
                
        #fire_bullet(spaceshipx,bullety)
        spaceship(spaceshipx, spaceshipy)
        alien(alienx, alieny)
        score_display(scorex,scorey)
        pygame.display.update()
        

#defining instructions
#the text is stored in a list
# the text appears letter by letter
#pressing enter iterates over the list
def instructions():
    font = pygame.font.Font('freesansbold.ttf',24)
    screen = pygame.display.set_mode([800,600])
    timer = pygame.time.Clock()
    messages = ['Welcome to space invaders!!!!!!!!!(press enter to continue)', 'Move the spaceship with arrow keys', 'Press spacebar to shoot bullets', "Risk crossing the boundary at your own peril", 'Shoot the aliens down or die','unimportantstuff']
    snip = font.render('', True, 'white')
    x = font.render('', True, 'white')
    counter = 0
    speed = 3
    active_message = 0
    message = messages[0]
    done = False
    message1 = 'press enter to continue'
    x = font.render(message1[0:counter // speed], True, 'white')
    screen.blit(x,(10, 400))
    pygame.display.update()
    

    run = True
    while run:
        screen.fill('black')
        timer.tick(120)
        #pygame.draw.rect(screen, 'black', [0, 500, 800, 200])
        if counter < speed*len(message):
            counter +=1
        elif counter >= speed*len(message):
            done = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and done and active_message<len(messages)-1:
                    active_message = active_message + 1
                    done = False
                    message = messages[active_message]
                    counter = 0

        snip = font.render(message[0:counter // speed], True, 'white')
        screen.blit(snip,(10, 250))
        pygame.display.flip()

        if active_message == len(messages)-1:
            snip = font.render(message[0:counter // speed], True, 'white')
            screen.blit(snip,(10, 250))
            pygame.display.flip()
            #time.sleep(10)
            run = False

    gameloop()



run = True
while run:
    if startbutton.draw():
        instructions()
        
    if exitbutton.draw():
        run = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()






    






    
