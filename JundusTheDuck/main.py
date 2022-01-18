# M Project
import pygame
import random
import time

pygame.font.init() #initialize font library
pygame.mixer.init() #initialize audio library

#Set screen
WIDTH, HEIGHT = 1200, 550
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) # New Window displaying with width and height
pygame.display.set_caption("JundusTheDuck") # Title name for Window

# Fonts
MENU_FONT = pygame.font.SysFont('comicsans', 40) #create comic sans font with a size of 40px

#RGB COLORS
BLACK = (0, 0, 0)

# Images
DUCKR_IMAGE = pygame.image.load('Assets/rubberDuck.png')
DASH_IMAGE = pygame.image.load('Assets/duckDash.png')
BATTLE_IMAGE = pygame.image.load('Assets/duckBattle.png')

#Sprites
duckStand = pygame.image.load('Assets/JundusStand.png')
duckRun = [pygame.image.load('Assets/JundusRun1.png'), pygame.image.load('Assets/JundusRun2.png')]
duckSneak = [pygame.image.load('Assets/JundusSneak1.png'), pygame.image.load('Assets/JundusSneak2.png')]
duckJump = pygame.image.load('Assets/JundusJump.png')

#Game settings
FPS = 60 # Frames per second
FLOOR = pygame.Rect(0-1, HEIGHT-50, WIDTH+2, HEIGHT)




# draw rotated ellipse "created by stack overflow"
def draw_ellipse_angle(surface, color, rect, angle, width=0):
    target_rect = pygame.Rect(rect)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(shape_surf, color, (0, 0, *target_rect.size), width)
    rotated_surf = pygame.transform.rotate(shape_surf, angle)
    surface.blit(rotated_surf, rotated_surf.get_rect(center = target_rect.center))





#Character Settings
class player(object):
    def __init__(self, x, y, width, height, startToFace):
        self.x, self.y, self.width, self.height = x, y, width, height


        self.hitbox = (self.x, self.y, self.width, self.height)
        #used while sneaking hitbox (x coordinate remains the same)
        self.sneakHitbox = (self.x, self.y+(self.height/3), self.width-(self.width/15), self.height-(self.height/3))

        self.greenbox = False

        self.vel = 15
        self.jumping = False
        self.ground = True
        self.gravity = 15

        self.isFacing = startToFace

        self.isrunning = True
        self.sneak = False
        self.runCount = 0
    
    def draw(self):
        if self.runCount + 1 >= 60:
            self.runCount = 0

        #standing animation
        if not self.jumping and not self.isrunning and not self.sneak:
            if self.isFacing == "RIGHT":
                WINDOW.blit(pygame.transform.scale(duckStand, (self.width, self.height)), (self.x,self.y))

            elif self.isFacing == "LEFT": #make duck face left
                WINDOW.blit(pygame.transform.flip(pygame.transform.scale(duckStand, (self.width, self.height)), True, False), (self.x,self.y))
        
        #crouch animation
        if not self.jumping and not self.isrunning and self.sneak:
            if self.isFacing == "RIGHT":
                WINDOW.blit(pygame.transform.scale(duckJump, (self.width, self.height)), (self.x,self.y))

            elif self.isFacing == "LEFT": #make duck face left
                WINDOW.blit(pygame.transform.flip(pygame.transform.scale(duckJump, (self.width, self.height)), True, False), (self.x,self.y))


        #running animation
        if self.isrunning and not self.jumping and not self.sneak:
            if self.isFacing == "RIGHT":
                WINDOW.blit(pygame.transform.scale(duckRun[self.runCount//30], (self.width, self.height)), (self.x,self.y))
                self.runCount += 9 #increase speed of frames

            elif self.isFacing == "LEFT": #make duck face left
                WINDOW.blit(pygame.transform.flip(pygame.transform.scale(duckRun[self.runCount//30], (self.width, self.height)), True, False), (self.x,self.y))
                self.runCount += 9 #increase speed of frames


        #sneaking animation
        if self.sneak and self.isrunning and not self.jumping:
            if self.isFacing == "RIGHT":
                WINDOW.blit(pygame.transform.scale(duckSneak[self.runCount//30], (self.width, self.height)), (self.x,self.y))
                self.runCount += 9 #increase speed of frames

            elif self.isFacing == "LEFT": #make duck face left
                WINDOW.blit(pygame.transform.flip(pygame.transform.scale(duckSneak[self.runCount//30], (self.width, self.height)), True, False), (self.x,self.y))
                self.runCount += 9 #increase speed of frames


        #jumping animation
        if self.jumping:
            if self.isFacing == "RIGHT":
                WINDOW.blit(pygame.transform.scale(duckJump, (self.width, self.height)), (self.x,self.y))

            elif self.isFacing == "LEFT": #make duck face left
                WINDOW.blit(pygame.transform.flip(pygame.transform.scale(duckJump, (self.width, self.height)), True, False), (self.x,self.y))
    


    def movements(self, keys_pressed):
        #left and right movement
        if keys_pressed[pygame.K_a] and self.x - self.vel > -10:
            self.x -= self.vel
            self.isrunning = True

            self.isFacing = "LEFT"

        elif keys_pressed[pygame.K_d] and self.x + self.vel < WIDTH - 65:
            self.x += self.vel
            self.isrunning = True

            self.isFacing = "RIGHT"

        else:
            self.isrunning = False

        #sneak and midair crouch movement
        if keys_pressed[pygame.K_s]:
            self.sneak = True
        else:
            self.sneak = False

        #jump movement
        if not self.jumping:
            if keys_pressed[pygame.K_SPACE]: 
                self.jumping = True

                self.isrunning = False
        else:
            if self.ground:
                self.y -= (HEIGHT-self.y) + self.gravity

                self.ground = False
            else:
                # player is in the air
                self.y -= self.gravity
                self.gravity -= 1.5

                # check if player is back on the ground
                if self.y > HEIGHT - 125:
                    self.y = HEIGHT - 125

                    self.ground = True
                    self.gravity = 15

                    self.jumping = False

        # re-update hitboxes
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        #used while sneaking hitbox (x coordinate remains the same)
        self.sneakHitbox = pygame.Rect(self.x, self.y+(self.height/3), self.width-(self.width/15), self.height-(self.height/3))

        #show player hitbox
        # self.greenbox = True
        # if self.greenbox:
        #     if self.jumping or self.sneak:
        #         pygame.draw.rect(WINDOW, (0, 255, 0), self.sneakHitbox, 2)
        #     else:
        #         pygame.draw.rect(WINDOW, (0, 255, 0), self.hitbox, 2)
#characters
jundus = player(500, 425, 75, 75, "RIGHT")





#weather settings
class weather(object):
    def __init__(self, leastX, maxX, leastY, maxY, amount, colorP):
        #particle effects
        self.weather = []
        self.leastX, self.maxX = leastX, maxX
        self.leastY, self.maxY = leastY, maxY

        self.amount = amount

        self.colorP = colorP
        for i in range(self.amount):
            self.addParticle()
    
    def addParticle(self):
        self.weather.append({
            "x": random.randrange(0, WIDTH),
            "y": random.randrange(0, HEIGHT),
            "r": random.randrange(2, 5),
            "color": self.colorP,
            "xSpeed": random.randint(self.leastX, self.maxX),
            "ySpeed": random.uniform(self.leastY, self.maxY),
            "rSpeed": random.uniform(0,2)})
    
    def weatherDraw(self):
        for i in range(self.amount):
            pygame.draw.circle(WINDOW, self.weather[i]["color"], (self.weather[i]["x"], self.weather[i]["y"]), self.weather[i]["r"])

            #Change particle x coordinate
            self.weather[i]["x"] -= self.weather[i]["xSpeed"]
            #Change particle y coordinate
            self.weather[i]["y"] += self.weather[i]["ySpeed"]

            #if particle moves offscreen, put it back on the opposide SIDE of the screen
            if self.weather[i]["x"] > WIDTH:
                self.weather[i]["x"] = 0
            elif self.weather[i]["x"] < 0:
                self.weather[i]["x"] = WIDTH

            #if particle moves offscreen, put it back on the TOP of the screen
            if self.weather[i]["y"] - self.weather[i]["r"] > HEIGHT:
                self.weather[i]["y"] = -self.weather[i]["r"]







#theme creater
class theme(object):
    def __init__(self, times, spacing, speed, background, floor, decorColor1, decorColor2, decorColor3):
        self.times, self.spacing, self.speed = times, spacing, speed

        self.decor = []

        self.background = background
        self.floor = floor

        self.color1 = decorColor1
        self.color2 = decorColor2
        self.color3 = decorColor3

        for i in range(self.times):
            self.addDecoration(i)
    
    def addDecoration(self, i):
        self.decor.append({
            "x": 150+(i*self.spacing),
            "y": -100,
            "width": 20,
            "height": 230})
    
    def placeDecorationSPEED(self, i, EXTRAspeed):
        #decoration directions
        #change decor x coordinate
        self.decor[i]["x"] -= self.speed+EXTRAspeed

        # if decor moves offscreen, put it back on the opposide side of the screen
        if self.decor[i]["x"] < -325:
            self.decor[i]["x"] = 2000
















#main menu
class mainMenuTheme(object):
    def __init__(self):
        #themes (theme, times, spacing, speed, background, floor, decorColor1, decorColor2, decorColor3)
        self.current = theme(8, 335, 3, (0, 0, 0), (0, 26, 0), (0, 51, 0), (26, 13, 0), (100, 255, 0))
        self.lush = theme(8, 335, 3, (0, 0, 0), (0, 26, 0), (0, 51, 0), (26, 13, 0), (100, 255, 0))
        self.night = theme(8, 335, 3, (0, 0, 38), (57, 38, 19), (0, 0, 128), (3, 10, 64), (255, 255, 0))

        #weather (leastX, maxX, leastY, maxY, amount, colorP)
        self.currentP = weather(5, 8, -3, 3, 150, (255, 255, 0))
        self.lushP = weather(5, 8, -3, 3, 150, (255, 255, 0))
        self.nightP = weather(5, 8, -3, 3, 150, (100, 255, 0))
        
    
    def placeDecorationBEHIND(self):
        #draw decoration objects
        for i in range(len(self.current.decor)):
            #tree log
            pygame.draw.rect(WINDOW, self.current.color2, pygame.Rect(self.current.decor[i]["x"]+30, 0, 80, HEIGHT)) 

            self.current.placeDecorationSPEED(i, 0)

    def placeDecorationFRONT(self):
        pygame.draw.rect(WINDOW, self.current.floor, FLOOR)#Draw a floor on the window
        #draw weather
        self.currentP.weatherDraw()

        #draw decoration objects
        for i in range(len(self.current.decor)):
            
            #tree leaves
            draw_ellipse_angle(WINDOW, self.current.color1, (self.current.decor[i]["x"], self.current.decor[i]["y"]-50, self.current.decor[i]["width"]+120, self.current.decor[i]["height"]+120), 20)
            draw_ellipse_angle(WINDOW, self.current.color1, (self.current.decor[i]["x"], self.current.decor[i]["y"]-50, self.current.decor[i]["width"]+120, self.current.decor[i]["height"]+120), 60)
            draw_ellipse_angle(WINDOW, self.current.color1, (self.current.decor[i]["x"], self.current.decor[i]["y"]-50, self.current.decor[i]["width"]+120, self.current.decor[i]["height"]+120), -20)
            draw_ellipse_angle(WINDOW, self.current.color1, (self.current.decor[i]["x"], self.current.decor[i]["y"]-50, self.current.decor[i]["width"]+120, self.current.decor[i]["height"]+120), -60)

            #tree core
            pygame.draw.circle(WINDOW, self.current.color3, (self.current.decor[i]["x"]+70, self.current.decor[i]["y"]+180), 30)

            #tree fruit
            pygame.draw.circle(WINDOW, self.current.color3, (self.current.decor[i]["x"]-80, self.current.decor[i]["y"]+210), 15)
            pygame.draw.circle(WINDOW, self.current.color3, (self.current.decor[i]["x"]+10, self.current.decor[i]["y"]+290), 15)
            pygame.draw.circle(WINDOW, self.current.color3, (self.current.decor[i]["x"]+130, self.current.decor[i]["y"]+290), 15)
            pygame.draw.circle(WINDOW, self.current.color3, (self.current.decor[i]["x"]+220, self.current.decor[i]["y"]+210), 15)

            #tall grass
            for q in range(5):
                pygame.draw.ellipse(WINDOW, self.current.color1, (self.current.decor[i]["x"]+(q*70)-60, self.current.decor[i]["y"]+580, self.current.decor[i]["width"], self.current.decor[i]["height"]-150))
                draw_ellipse_angle(WINDOW, self.current.color1, (self.current.decor[i]["x"]+(q*70)-60, self.current.decor[i]["y"]+580, self.current.decor[i]["width"], self.current.decor[i]["height"]-150), 45)
                draw_ellipse_angle(WINDOW, self.current.color1, (self.current.decor[i]["x"]+(q*70)-60, self.current.decor[i]["y"]+580, self.current.decor[i]["width"], self.current.decor[i]["height"]-150), -45)

                pygame.draw.circle(WINDOW, self.current.color3, (self.current.decor[i]["x"]+(q*70)-50, self.current.decor[i]["y"]+580), 4)
                pygame.draw.circle(WINDOW, self.current.color3, (self.current.decor[i]["x"]+(q*70)-80, self.current.decor[i]["y"]+590), 4)
                pygame.draw.circle(WINDOW, self.current.color3, (self.current.decor[i]["x"]+(q*70)-20, self.current.decor[i]["y"]+590), 4)
                
            self.current.placeDecorationSPEED(i, 0)
mainMenu = mainMenuTheme()










#obstacle Run Game
class duckDashGame(object):
    def __init__(self, x, y, width, height):
        #themes      (times, spacing, speed, background, floor, decorColor1, decorColor2, decorColor3) 
        self.currentF = theme(14, 179.5, 8, (0, 0, 0), (100, 255, 0), (255, 255, 0), (255, 163, 67), (0, 255, 0))
        self.currentB = theme(14, 179.5, 5, (0, 0, 0), (100, 255, 0), (255, 255, 0), (255, 163, 67), (0, 255, 0))
        self.lush = theme(14, 179.5, 8, (0, 0, 0), (100, 255, 0), (255, 255, 0), (255, 163, 67), (0, 255, 0))
        self.night = theme(14, 179.5, 5, (0, 0, 0), (255, 255, 0), (0, 255, 0), (70, 102, 255), (0, 255, 255))

        #obstacle
        self.x, self.y, self.width, self.height = x, y, width, height
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

        #game settings
        self.intensity = 1

        self.scoreTick = time.time()
        self.score = 0
        self.highscore = self.score
    
    def placeDecorationBEHIND(self):
        #draw decoration objects
        for i in range(len(self.currentB.decor)):
            pygame.draw.rect(WINDOW, self.currentB.color3, pygame.Rect(self.currentB.decor[i]["x"]-110, 50, 178.5, 200), 2)
            pygame.draw.rect(WINDOW, self.currentB.color3, pygame.Rect(self.currentB.decor[i]["x"]-110, HEIGHT-300, 178.5, 200), 2)

            pygame.draw.circle(WINDOW, self.currentB.color1, (self.currentB.decor[i]["x"]+70, self.currentB.decor[i]["y"]+350), 30, 5)

            pygame.draw.rect(WINDOW, self.currentB.color2, pygame.Rect(self.currentB.decor[i]["x"]-200, 0, 179.5, 50), 2)
            pygame.draw.rect(WINDOW, self.currentB.color2, pygame.Rect(self.currentB.decor[i]["x"]-200, HEIGHT-100, 179.5, 50), 2)

            self.currentB.placeDecorationSPEED(i, 0)
    
    def placeDecorationFRONT(self):
        for i in range(len(self.currentF.decor)):
            #draw faster floor
            pygame.draw.rect(WINDOW, self.currentF.color3, pygame.Rect(self.currentF.decor[i]["x"], 500, 179.5, 200), 2)

            self.currentF.placeDecorationSPEED(i, self.intensity)
        self.obstacle()
    
    def obstacle(self):
        #obstacle
        pygame.draw.rect(WINDOW, self.currentF.color1, self.hitbox)
        pygame.draw.rect(WINDOW, BLACK, pygame.Rect(self.x+5, self.y+5, self.width-10, self.height-10))

        if self.hitbox.colliderect(jundus.hitbox):#if player hits obstacle, reset score, scoretick, intensity and obstacle x position
            self.x = 2000
            self.intensity = 0
            self.highscore = self.score
            self.score, self.scoreTick = 0,  time.time()
        else:
            if self.score < 500*(self.intensity//5): #every 500 points in your score, will increase the "intensity" by 5px faster
                self.x -= self.currentF.speed+ (1*self.intensity)
            else:
                self.intensity += 5

            #if obstacle moves offscreen, put it back to the right side
            if self.x < -200:
                self.x = 2000

        self.score = round((time.time()-self.scoreTick)*100)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
duckDash = duckDashGame(1000, 400, 80, 100)





def levelOperator(mousePosition, keys_pressed, type, theme, player, text):
    WINDOW.fill(theme.background)#fill window background

    type.placeDecorationBEHIND()

    #player movements and bindings
    player.movements(keys_pressed)
    player.isFacing = "RIGHT"
    player.isrunning = True
    player.draw()

    type.placeDecorationFRONT()

    gameTypes(mousePosition, text, theme)


def gameTypes(mousePosition, text, type):
        #game text
        WINDOW.blit(MENU_FONT.render((text), 1, type.color3), (10, 10))

        #load startblocks
        startblocks(mousePosition, DUCKR_IMAGE, type.color3, pygame.Rect(800, 0, 40, 40), (50, 50), (795, -5), "Main Menu")
        startblocks(mousePosition, DASH_IMAGE, type.color3, pygame.Rect(845, 0, 40, 40), (40,40), (845, 0), "Duck Dash")
        startblocks(mousePosition, BATTLE_IMAGE, type.color3, pygame.Rect(890, 0, 40, 40), (40,40), (890, 0), "Duck Battle")

def startblocks(mousePosition, image, color, hitbox, size, xy, game):
        #Create Startblock
        pygame.draw.rect(WINDOW, color, hitbox)
        WINDOW.blit(pygame.transform.scale(image, size), xy)

        if hitbox.collidepoint(mousePosition): #if start block is clicked begin game
            currentScreen.type = game

def themeswitch(currentLevel, newlevel, currentW, newP):
    #change level theme colours
    currentLevel.background = convertRGB(currentLevel.background, newlevel.background, 0.5)

    current1, current2, current3 = currentLevel.color1, currentLevel.color2, currentLevel.color3
    color1, color2, color3 = newlevel.color1, newlevel.color2, newlevel.color3

    currentLevel.color1, currentLevel.color2, currentLevel.color3 = convertRGB(current1, color1, 0.5), convertRGB(current2, color2, 0.5), convertRGB(current3, color3, 0.5)

    #change weather (if there is one)
    if currentW is not False and newP is not False:
        for i in range(currentW.amount):
            currentW.weather[i]["color"] = convertRGB(currentW.weather[i]["color"], newP.weather[i]["color"], 1)
            currentW.weather[i]["xSpeed"] = slowlymatch(currentW.weather[i]["xSpeed"], newP.weather[i]["xSpeed"], 0.01)
            currentW.weather[i]["ySpeed"] = slowlymatch(currentW.weather[i]["ySpeed"], newP.weather[i]["ySpeed"], 0.01)
            currentW.weather[i]["rSpeed"] = slowlymatch(currentW.weather[i]["rSpeed"], newP.weather[i]["rSpeed"], 0.01)


def convertRGB(changingcolor, requestedcolor, rate): #slowly change the rgb one at a time
    r1, g1, b1 = changingcolor
    r2, g2, b2 = requestedcolor

    r = slowlymatch(r1, r2, rate)
    g = slowlymatch(g1, g2, rate)
    b = slowlymatch(b1, b2, rate)

    return (r, g, b)

def slowlymatch(request, final, rate):
    if request > final:
        return request - rate
    elif request < final:
        return request + rate
    else: #if matched completely return regularly
        return request




class levelAnalyzer(object):
    def __init__(self, screendisplayed):
        self.type = screendisplayed
        self.theme = "LUSH"
    
    def levelHandler(self, keys_pressed, mousePosition):
        #key interations for theme
        if keys_pressed[pygame.K_1]:
            self.theme = "NIGHT"
        elif keys_pressed[pygame.K_2]:
            self.theme = "LUSH"

    
        if currentScreen.type == "Main Menu":
            levelOperator(mousePosition, keys_pressed, mainMenu, mainMenu.current, jundus, "WASD: MOVE     SPACE: JUMP     1,2: SWITCH THEME")

            #theme switching
            if self.theme == "LUSH":
                themeswitch(mainMenu.current, mainMenu.lush, mainMenu.currentP,  mainMenu.lushP)
            elif self.theme == "NIGHT":
                themeswitch(mainMenu.current, mainMenu.night,  mainMenu.currentP,  mainMenu.nightP)


        elif currentScreen.type == "Duck Dash":
            levelOperator(mousePosition, keys_pressed, duckDash, duckDash.currentF, jundus, f"SCORE: {duckDash.score}     HIGHSCORE: {duckDash.highscore}     1,2: SWITCH THEME")

            #theme switching
            if self.theme == "LUSH":
                themeswitch(duckDash.currentF, duckDash.lush, False, False)
                themeswitch(duckDash.currentB, duckDash.lush, False, False)
            elif self.theme == "NIGHT":
                themeswitch(duckDash.currentF, duckDash.night,  False,  False)
                themeswitch(duckDash.currentB, duckDash.night, False, False)
currentScreen = levelAnalyzer("Main Menu")





def main(): # main function
    clock = pygame.time.Clock()

    # Run Game
    run = True
    while run:
        clock.tick(FPS)# Refresh rate by frames per second

        mousePosition = (1, 1)

        # Create a function/loop to quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()#quits the game

            if event.type == pygame.MOUSEBUTTONDOWN: #main mouse handler
                mousePosition = pygame.mouse.get_pos()
                print(mousePosition)
        #
        
        #get keyspressed
        keys_pressed = pygame.key.get_pressed()

        #use level handler and redraw the window
        currentScreen.levelHandler(keys_pressed, mousePosition)
        pygame.display.update()#update the display changes

    main()#restart game


if __name__ == "__main__":
    main()