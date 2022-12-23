import pygame
import os
import time


""" 
    Pong inspired game based on John Donne's "The Flea"

    The point is to not get hit by the slapping hand

    This game is analogous to the scene in the poem in which the lady proceeds to kill the flea

    Use arrow keys to move the flea

    Enjoy!

"""
pygame.init() #to initialize fonts and stuff

WIDTH, HEIGHT = 900, 500 #window width and height

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #creates screen
pygame.display.set_caption("Flea Game!") #title of screen
FPS = 60 #fps
VEL = 10 #Velocity of flea
 
FLEA_WIDTH, FLEA_HEIGHT = 80,70
HAND_WIDTH, HAND_HEIGHT = 90,80
START_WIDTH, START_HEIGHT = 120,70
TITLE_WIDTH, TITLE_HEIGHT = 300, 150

#loading in all of the images (everything is in a folder)
#there is a folder inside of the folder called "images"

FLEA_IMAGE = pygame.image.load(os.path.join("images","flea.png")).convert()
HAND_IMAGE = pygame.image.load(os.path.join("images","hand.png"))
START_IMAGE = pygame.image.load(os.path.join("images","startButton.jpg")).convert()
TITLETEXT_IMAGE = pygame.image.load(os.path.join("images","titleText.jpg")).convert()
TRYAGAIN_IMAGE = pygame.image.load(os.path.join("images","tryAgain.jpg")).convert()
MAINMENU_IMAGE = pygame.image.load(os.path.join("images","mainMenu.jpg")).convert()
MAN_IMAGE = pygame.image.load(os.path.join("images","beggingMan.png"))
WOMAN_IMAGE = pygame.image.load(os.path.join("images","annoyedWoman.png"))
FLEA_IMAGE = pygame.transform.scale(FLEA_IMAGE,(FLEA_WIDTH,FLEA_HEIGHT))
HAND_IMAGE = pygame.transform.scale(HAND_IMAGE,(HAND_WIDTH,FLEA_HEIGHT))
START_IMAGE = pygame.transform.scale(START_IMAGE,(START_WIDTH,START_HEIGHT))
TITLETEXT_IMAGE = pygame.transform.scale(TITLETEXT_IMAGE,(TITLE_WIDTH, TITLE_HEIGHT))
MAN_IMAGE = pygame.transform.scale(MAN_IMAGE, (200, 270))
WOMAN_IMAGE = pygame.transform.scale(WOMAN_IMAGE, (290, 300))
MAINMENU_IMAGE = pygame.transform.scale(MAINMENU_IMAGE, (200,50))
TRYAGAIN_IMAGE = pygame.transform.scale(TRYAGAIN_IMAGE, (200,50))

fleaFacing = 'left'
handFacing = 'right'



#this draws the window every frame, determining what goes on the screen
def draw_window(flea, hand, start, playing, menu, options, Score, main, tryr):

    textColor = (92,5,5)
    WIN.fill((0,0,0)) #clears the screen out first so it is just black

    font = pygame.font.SysFont('impact', 25)
    line1 = font.render('Cruel and sudden, hast thou since Purpled thy nail, in blood of innocence?', True, textColor)
    line2 = font.render(f'Your score was {Score}', True, textColor)
    font = pygame.font.SysFont('impact', 30)
    line3 = font.render(f'Score: {Score}', True, textColor)
    if playing:
        WIN.blit(FLEA_IMAGE,(flea.x, flea.y)) #blit simply places an image somewhere on the screen
        WIN.blit(HAND_IMAGE,(hand.x, hand.y))
        WIN.blit(line3, (780,20))
    if menu:
        WIN.blit(TITLETEXT_IMAGE,(WIDTH/2 - TITLE_WIDTH/2, 100-TITLE_HEIGHT/2))
        WIN.blit(START_IMAGE,(start.x, start.y))
        WIN.blit(MAN_IMAGE,(10, HEIGHT/2-130))
        WIN.blit(WOMAN_IMAGE,(600, HEIGHT/2-160))
    if options:
        WIN.blit(MAINMENU_IMAGE, (main.x, main.y))
        WIN.blit(TRYAGAIN_IMAGE, (tryr.x, tryr.y))
        WIN.blit(line1, (60, 40))
        WIN.blit(line2, (350, 80))
    pygame.display.update() #updates screen


def flea_handle_movement(KeysPressed, Flea): #checks if left or right key is pressed
    global FLEA_IMAGE
    global fleaFacing
    if KeysPressed[pygame.K_LEFT] and (Flea.x >= VEL):
        Flea.x -= VEL
        if fleaFacing == 'right':
            fleaFacing = 'left'
            FLEA_IMAGE = pygame.transform.flip(FLEA_IMAGE, True, False) #flips which way flea is facing
    if KeysPressed[pygame.K_RIGHT] and (Flea.x <= 810):
        Flea.x += VEL
        if fleaFacing == 'left':
            fleaFacing = 'right'
            FLEA_IMAGE = pygame.transform.flip(FLEA_IMAGE, True, False)


def f(x): #function for increasing speed of slapping hand
    return 2*((1+5**(x+1)/(1+5**x))) 

def main():
    global HAND_IMAGE
    global handFacing
    isMenu = True
    isPlaying = False
    isOptions = False
    handEvent = pygame.USEREVENT 

    #each image has a rectangle associated with it because we can change the position of the rectangles
    #but we cannot change position of image
    #we then draw the corresponding images onto wherever the rectangles are
    #the rectangles are also the "hitboxes" so it checks if two rectangles are hitting so it'll know if we lose


    fleaRect = pygame.Rect(WIDTH/2-FLEA_WIDTH/2,460-FLEA_HEIGHT/2,FLEA_WIDTH, FLEA_HEIGHT)
    handRect = pygame.Rect(WIDTH/2-HAND_WIDTH/2, 40, HAND_WIDTH, HAND_HEIGHT)
    startRect = pygame.Rect(WIDTH/2 - START_WIDTH/2, 250, START_WIDTH, START_HEIGHT)
    mainRect = pygame.Rect(150,250,200,50)
    tryRect = pygame.Rect(550,250,200,50)

    clock = pygame.time.Clock()
    run = True
    stepSize = 100
    score = 0
    counter = 0
    moving = False
    handMovingDown = False
    handMovingUp = False
    pygame.time.set_timer(handEvent, 10) #hand waits 10 milliseconds before moving again (negligable, not important)
    while run:
        clock.tick(FPS) #doesn't let it run more than 60 fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if we click x on the window
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN: #if we click on the screen
                x, y = event.pos #position of mouse click
                if startRect.collidepoint(x,y) and isMenu: #if we click on start button in menu
                    isMenu = False
                    isPlaying = True
                    fleaRect.x, fleaRect.y = WIDTH/2-FLEA_WIDTH/2, 460-FLEA_HEIGHT/2 #spawns flea
                    handRect.x, handRect.y = WIDTH/2-HAND_WIDTH/2, 40 #spawns hand
                    score = 0

                if mainRect.collidepoint(x,y) and isOptions: #if we hit main menu after we die
                    isMenu = True
                    isOptions = False
                    isPlaying = False
                if tryRect.collidepoint(x,y) and isOptions: #if we hit try again after we die
                    score = 0
                    isMenu = False
                    isOptions = False
                    isPlaying = True
            if event.type == handEvent and isPlaying: 
                moving = True #initiates hand movement


        if (not handMovingDown and (not handMovingUp)) and moving: #if we have not started moving but need to
            startTime = time.time()*1000
            handMovingDown = True
            targetPoint = [fleaRect.x + 50, fleaRect.y + 50] #finds where the flea currently is
            if targetPoint[0] > WIDTH/2:
                if handFacing == 'left':
                    HAND_IMAGE = pygame.transform.flip(HAND_IMAGE, True, False) #flips hand according to direction
                    handFacing = 'right'
            else:
                if handFacing == 'right':
                    HAND_IMAGE = pygame.transform.flip(HAND_IMAGE, True, False)
                    handFacing = 'left'

            handStart = [WIDTH/2-HAND_WIDTH/2, 40] #where the hand starts every time
            stepX = (targetPoint[0] - handStart[0])/stepSize #the speed is determiend by how many steps it takes to get to the flea
            stepY = (targetPoint[1] - handStart[1])/stepSize #the less steps means the faster it goes
            steps = 0
        elif handMovingDown and ((time.time()*1000 - startTime) > 15): #the time thing makes sure its not moving more than one step every 15 milliseconds
            handRect.x += stepX # one step in x and y
            handRect.y += stepY
            steps += 1
            startTime = time.time()*1000
            if steps == stepSize: #once it reaches the flea
                handMovingUp = True
                handMovingDown = False
                steps = 0
                startTime = time.time()*1000
                stepX = (handRect.x - handStart[0])/stepSize
                stepY = (handRect.y - handStart[1])/stepSize
        elif handMovingUp and ((time.time()*1000 - startTime) > 15): #starts going back up
            handRect.x -= stepX
            handRect.y -= stepY
            steps += 1
            startTime = time.time()*1000
            if steps == stepSize: #once it is back in the position
                handMovingUp = False
                handMovingDown = False
                moving = False
                score += 1 #add to score
                counter += 1
                stepSize -= int(f(counter-10)) #make it go faster according to function
                if stepSize < 30: #max speed (30 step size)
                    stepSize = 30

        else:
            pass
                    



        if not isPlaying: #if it isn't playing, everything goes back to default position and values
            isPlaying = False
            fleaRect.x, fleaRect.y = WIDTH/2-FLEA_WIDTH/2,460-FLEA_HEIGHT/2
            handRect.x, handRect.y = WIDTH/2-HAND_WIDTH/2, 40
            moving = False
            handMovingDown = False
            handMovingUp = False
            counter = 0
            stepSize = 100

        if pygame.Rect.colliderect(fleaRect, handRect): #if flea and hand rectangles collide, game over
            isPlaying = False
            isOptions = True

        keys_pressed = pygame.key.get_pressed() #all keys currently pressed
        flea_handle_movement(keys_pressed, fleaRect) #checks if left or right key pressed for moving flea
        


        draw_window(fleaRect, handRect, startRect, isPlaying, isMenu, isOptions, score, mainRect, tryRect)
        #draws window
        #also, every iteration of the while loop is one frame

    pygame.quit() #if the x is clicked on the window

main()   