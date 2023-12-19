'''
Super Mario Bro's Game
Built for COMP16321 Intro to Programming Coursework 2
By Benjamin Dyson

Recommended Screen Resolution: 1440 x 900

IMAGE CREDITS:
Mario image: All states,
Designed by Rose Studio,
https://www.shutterstock.com/image-vector/kyiv-ukraine-april-12-2023-set-2288183539
Accessed: 22/11/2023

Mushroom image: Cartoon mushroom
Designed by Rose Studio,
https://www.shutterstock.com/image-vector/set-enemies-characters-super-mario-bros-2291573629
Accessed: 22/11/2023

Trophy image: Cartoon Trophy
Designed by juicy_fish 
https://www.freepik.com/free-vector/gradient-trophy-2_35202416.htm#query=trophy%20cartoon&position=8&from_view=keyword&track=ais&uuid=ce9ad9ae-72d6-4f8d-9bfc-21bc20a2cae0
Accessed: 22/11/2023

Cloud image: Cartoon Cloud,
Designed by rawpixel.com/Freepix
https://www.freepik.com/free-vector/set-cloud-with-pop-art-style_24525423.htm#query=cartoon%20cloud&position=9&from_view=keyword&track=ais&uuid=63d70567-defa-4bea-9742-dddc8a811876
Accessed: 21/11/2023

Boss key image: Excel Image,
Designed by rawpixel.com/Freepix
https://www.freepik.com/free-vector/illustration-data-analysis-graph_2605698.htm#query=microsoft%20excel&position=21&from_view=keyword&track=ais&uuid=180c763e-41cb-4cd8-8b97-9f44cf6a661a
Accessed: 20/11/2023
'''

#Import libraries
from tkinter import Tk, Canvas, Label, Entry, Button, ALL, END, Toplevel
import random
from PIL import Image, ImageTk
from time import sleep

#Set Constants
#Set screen width and height here
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900

#Set game width and height
GAME_WIDTH = 0.8*SCREEN_WIDTH
GAME_HEIGHT = SCREEN_HEIGHT

#Set player size
PLAYERXSIZE = 30
PLAYERYSIZE = 60
#Set player start position
PLAYERSTARTPOS = (100, 700)

#Set coin size
COINXSIZE = 20
COINYSIZE = 20

#Set mushrooms size
MUSHROOMXSIZE = 30
MUSHROOMYSIZE = 30

#Set trophy size
TROPHXSIZE = 40
TROPHYSIZE = 45

#Cloud size
CLOUDXSIZE = 200
CLOUDYSIZE = 103

#Define how fast the falling is
GRAVITY = 0.25

#Set initial falling and jumping velocity
INTIAL_FALL_VELOCITY = 1
INTIAL_JUMP_VELOCITY = 9

#Set mushroom move speed
MUSHROOM_MOVE_SPEED = 1

#Set background
BACKGROUND_COLOUR = '#87CEEB'


#Set functions

def UserOption(): #Function to flip the user input variable
    global controls
    #Change the controls the user is using between arrows and WASD
    if controls == 'WASD':
        controls = 'Arrows'
        controlButton.config(text=controls)

    elif controls == 'Arrows':
        controls = 'WASD'
        controlButton.config(text=controls)

def setMovement(event): #Function to set boolean movement variables when the key is pressed
    key = event.keysym
    global controls
    global right, left, jumping, up, YVelocity, down, falling
    if controls == 'WASD':
        if key == 'd':
            right = True
        elif key == 'a':
            left = True
        elif key == 'w':
            if cheatCode == 'Fly': #If fly is on use up and dont use jump
                up = True
            else:
                if jumping == False and not(falling): #Reset Y velocity to intial jump velocity
                    YVelocity = INTIAL_JUMP_VELOCITY
                jumping = True 
        elif key == 's':
            down = True

    elif controls == 'Arrows':
        if key == 'Right':
            right = True
        elif key == 'Left':
            left = True
        elif key =='Up':
            if cheatCode == 'Fly': #If fly is on use up and dont use jump
                up = True
            else:
                if jumping == False: #Reset Y velocity to intial jump velocity
                    YVelocity = INTIAL_JUMP_VELOCITY
                jumping = True   
        elif key == 'Down':
            down = True  

def removeMovement(event):#Function to remove boolean movement variables when the key is released
    key = event.keysym
    global right, left, jumping, up, YVelocity, down, runImage
    if controls == 'WASD':
        if key == 'd':
            right = False
            runImage = 1
        elif key == 'a':
            left = False
            runImage = 1
        elif key == 'w':
            if cheatCode == 'Fly': #If fly is on use up and dont use jump
                up = False
        elif key == 's':
            down = False

    elif controls == 'Arrows':
        if key =='Right':
            right = False
            runImage = 1
        elif key =='Left':
            left = False
            runImage = 1
        elif key =='Up':
            if cheatCode == 'Fly': #If fly is on use up and dont use jump
                up = False 
        elif key == 'Down':
            down = False 

def pauseGame(event): #Function to flip the pause
    global pause
    global countdownOn
    if pause == False:
        pause = True
    elif pause == True:
        #Countdown before user starts
        if not(countdownOn):
            countdownOn = True
            for i in range(3, 0, -1):
                countdown = canvas.create_text(500, 400, text=str(i), fill='black', font=('Arial', 100))
                window.update()
                sleep(1)
                canvas.delete(countdown)
            countdownOn = False
        pause = False

def setBossKey(event): #Function to flip the boss key
    global bosskey
    bosskey = True

def deleteBossWindow(event): #Function to delete the boss window
    global pause
    pause = False
    bossWindow.destroy()

def checkCollisionsWithTopPlatforms(playerHitBox, platforms): #check if the player is on top of a platform
    for platform in platforms:
        playerCoords = canvas.coords(playerHitBox) #Get player coordinates
        platformCoords = canvas.coords(platform) #Get platform coorfinates
        if playerCoords[2]>=platformCoords[0] and playerCoords[0]<=platformCoords[2] and playerCoords[3]>=platformCoords[1] and playerCoords[1]<=platformCoords[1]:
            Ycorrection = canvas.coords(playerHitBox)[3]-canvas.coords(platform)[1]
            #Correct the hitbox and image to stay above the platform
            canvas.move(playerHitBox, 0, -(Ycorrection)) 
            canvas.move(playerImage, 0, -(Ycorrection))
            return True
    return False

def checkCollisionsWithBottomPlatforms(playerHitBox, platforms): #Check if the player hits the bottom of a platform
    for platform in platforms:
        playerCoords = canvas.coords(playerHitBox)#Get player coordinates
        platformCoords = canvas.coords(platform) #Get platform coorfinates
        if playerCoords[2]>=platformCoords[0] and playerCoords[0]<=platformCoords[2] and playerCoords[1]<=platformCoords[3] and playerCoords[1]>=platformCoords[1]:
            return True
    return False

def checkCollisionsWithLeftSidePlatforms(playerHitBox, platforms): #Check if the player hits the left of a platform
    for platform in platforms:
        playerCoords=canvas.coords(playerHitBox) #Get player coordinates
        platformCoords = canvas.coords(platform) #Get platform coorfinates
        if playerCoords[2]>=platformCoords[0] and playerCoords[0]<=platformCoords[0] and playerCoords[1]+1<platformCoords[3] and playerCoords[3]-1>platformCoords[1]:
            return True, canvas.coords(playerHitBox)[2]-canvas.coords(platform)[0]
    return False, 0

def checkCollisionsWithRightSidePlatforms(playerHitBox, platforms): #Check if the player hits the right of a platform
    for platform in platforms:
        playerCoords=canvas.coords(playerHitBox) #Get player coordinates
        platformCoords = canvas.coords(platform) #Get platform coorfinates
        if playerCoords[2]>=platformCoords[2] and playerCoords[0]<=platformCoords[2] and playerCoords[1]+1<platformCoords[3] and playerCoords[3]-1>platformCoords[1]:
            return True, canvas.coords(platform)[2]-canvas.coords(playerHitBox)[0]
    return False, 0

def checkCollisionsWithTopMushroom(playerHitBox, object): #Check if the player collides with the top of the mushroom
    playerCoords = canvas.coords(playerHitBox) #Get player coordinates
    mushroomCoords = canvas.coords(object)  #Get mushroom coordinates
    if playerCoords[2]>=mushroomCoords[0] and playerCoords[0]<=mushroomCoords[2] and playerCoords[3]+5>=mushroomCoords[1] and playerCoords[1]<=mushroomCoords[1]:
        return True
    return False

def checkCollisionsWithSideMushroom(playerHitBox, mushroom): #Check if the player has collided with the side of the mushroom
    playerCoords = canvas.coords(playerHitBox) #Get player coordinates
    mushroomCoords = canvas.coords(mushroom) #Get mushroom coordinates
    sideHit = False
    #Check right side
    if playerCoords[1]<=mushroomCoords[3] and playerCoords[3]>=mushroomCoords[1] and playerCoords[2]+MUSHROOM_MOVE_SPEED+7>=mushroomCoords[0] and playerCoords[0]<=mushroomCoords[2]:
        sideHit = True
    #Check left side
    if playerCoords[1]<=mushroomCoords[3] and playerCoords[3]>=mushroomCoords[1] and playerCoords[2]>=mushroomCoords[2] and playerCoords[0]-MUSHROOM_MOVE_SPEED-7<=mushroomCoords[2]:
        sideHit = True
    return sideHit

def mushroomOnSideOfPlatform(mushroom, platforms): #Check if the mushroom is on the side of a platform
    for platform in platforms:
        mushroomCoords = canvas.coords(mushroom) #Get mushroom coordinates
        platformCoords = canvas.coords(platform) #Get platform coorfinates
        if mushroomCoords[0]>platformCoords[0] and mushroomCoords[2]<platformCoords[2]:  #Check if mushroom is in a platforms range
            if(mushroomCoords[0]-MUSHROOM_MOVE_SPEED<=platformCoords[0] or mushroomCoords[2]+MUSHROOM_MOVE_SPEED>=platformCoords[2]): #Check if next move is out of platform rnage
                return True
    return False

def checkCollisionWithCoin(playerHitBox, coin): #Check player has collided with the coin
    playerCoords = canvas.coords(playerHitBox) #Get player coordinates
    coinCoords = canvas.coords(coin) #Get coin coordinates
    if playerCoords[2]>=coinCoords[0] and playerCoords[0]<=coinCoords[2] and playerCoords[0]<=coinCoords[3] and playerCoords[3]>=coinCoords[1]:
        return True
    return False

def checkCollisionWithTrophy(playerHitBox, trophy):#Check player has collided with the trophy
    playerCoords = canvas.coords(playerHitBox) #Get player coordinates
    trophyCoords = canvas.coords(trophy) #Get trophy coordinatesd
    if playerCoords[2]>=trophyCoords[0] and playerCoords[0]<=trophyCoords[2] and playerCoords[0]<=trophyCoords[3] and playerCoords[3]>=trophyCoords[1]:
        return True
    return False

def printLevel(): #Print the levels to the canvas
    global currentLevel
    global platforms
    global mushrooms
    global coins
    global mushroomDirections
    global trophy
    global clouds
    global trophyImage
    global mushroomImages
    # global playerImage
    #Instantiate the arrys to avoid errors if one isn't used
    clouds = []
    platforms = []
    mushrooms = []
    mushroomImages = []
    coins = []
    mushroomDirections = []
    trophy = ''
    if currentLevel == 1:
        #Create the clouds
        clouds.append(canvas.create_image(50, 200, image=cloudImg))
        clouds.append(canvas.create_image(300, 300, image=cloudImg))
        clouds.append(canvas.create_image(600, 170, image=cloudImg))
        clouds.append(canvas.create_image(950, 270, image=cloudImg))
        clouds.append(canvas.create_image(1100, 160, image=cloudImg))
        clouds.append(canvas.create_image(1400, 310, image=cloudImg))

        #Create the platforms
        platforms.append(canvas.create_rectangle(50, GAME_HEIGHT-100, 1100, GAME_HEIGHT-50, fill='green'))

        #Create the coins
        coins.append(canvas.create_rectangle(340, GAME_HEIGHT-135, 340+COINXSIZE, GAME_HEIGHT-135+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(380, GAME_HEIGHT-135, 380+COINXSIZE, GAME_HEIGHT-135+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(420, GAME_HEIGHT-135, 420+COINXSIZE, GAME_HEIGHT-135+COINYSIZE, fill='gold'))

        coins.append(canvas.create_rectangle(600, GAME_HEIGHT-135, 600+COINXSIZE, GAME_HEIGHT-135+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(640, GAME_HEIGHT-135, 640+COINXSIZE, GAME_HEIGHT-135+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(680, GAME_HEIGHT-135, 680+COINXSIZE, GAME_HEIGHT-135+COINYSIZE, fill='gold'))

        #Create the trophy
        trophy = canvas.create_rectangle(950, GAME_HEIGHT-160, 950+TROPHXSIZE, GAME_HEIGHT-160+TROPHYSIZE, outline='')
        trophyImage = canvas.create_image(950+TROPHXSIZE/2, 740+TROPHYSIZE/2, image=trophyImg)

    elif currentLevel == 2:
        #Create the clouds
        clouds.append(canvas.create_image(50, 200, image=cloudImg))
        clouds.append(canvas.create_image(300, 300, image=cloudImg))
        clouds.append(canvas.create_image(600, 170, image=cloudImg))
        clouds.append(canvas.create_image(950, 270, image=cloudImg))
        clouds.append(canvas.create_image(1100, 160, image=cloudImg))
        clouds.append(canvas.create_image(1400, 310, image=cloudImg))

        #Add platforms
        platforms.append(canvas.create_rectangle(50, GAME_HEIGHT-100, 500, GAME_HEIGHT-50, fill='green'))
        platforms.append(canvas.create_rectangle(500, GAME_HEIGHT-250, 1000, GAME_HEIGHT-200, fill='green'))
        platforms.append(canvas.create_rectangle(1000, GAME_HEIGHT-100, 1300, GAME_HEIGHT-50, fill='green'))

        #Create the coins
        coins.append(canvas.create_rectangle(290, GAME_HEIGHT-135, 290+COINXSIZE, GAME_HEIGHT-135+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(330, GAME_HEIGHT-135, 330+COINXSIZE, GAME_HEIGHT-135+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(370, GAME_HEIGHT-135, 370+COINXSIZE, GAME_HEIGHT-135+COINYSIZE, fill='gold'))

        coins.append(canvas.create_rectangle(660, GAME_HEIGHT-285, 660+COINXSIZE, GAME_HEIGHT-285+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(700, GAME_HEIGHT-285, 700+COINXSIZE, GAME_HEIGHT-285+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(740, GAME_HEIGHT-285, 740+COINXSIZE, GAME_HEIGHT-285+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(780, GAME_HEIGHT-285, 780+COINXSIZE, GAME_HEIGHT-285+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(820, GAME_HEIGHT-285, 820+COINXSIZE, GAME_HEIGHT-285+COINYSIZE, fill='gold'))

        #Create the trophy
        trophy = canvas.create_rectangle(1200, GAME_HEIGHT-160, 1200+TROPHXSIZE, GAME_HEIGHT-160+TROPHYSIZE, outline='')
        trophyImage = canvas.create_image(1200+TROPHXSIZE/2, 740+TROPHYSIZE/2, image=trophyImg)

    elif currentLevel == 3:
        #Create the clouds
        clouds.append(canvas.create_image(50, 200, image=cloudImg))
        clouds.append(canvas.create_image(300, 300, image=cloudImg))
        clouds.append(canvas.create_image(600, 170, image=cloudImg))
        clouds.append(canvas.create_image(950, 270, image=cloudImg))
        clouds.append(canvas.create_image(1100, 160, image=cloudImg))
        clouds.append(canvas.create_image(1400, 310, image=cloudImg))

        #Add platforms
        platforms.append(canvas.create_rectangle(50, GAME_HEIGHT-100, 550, GAME_HEIGHT-50, fill='green'))
        platforms.append(canvas.create_rectangle(600, GAME_HEIGHT-100, 1100, GAME_HEIGHT-50, fill='green'))
        platforms.append(canvas.create_rectangle(1150, GAME_HEIGHT-100, 1650, GAME_HEIGHT-50, fill='green'))

        #Create the coins
        coins.append(canvas.create_rectangle(370, GAME_HEIGHT-135, 370+COINXSIZE, GAME_HEIGHT-135+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(410, GAME_HEIGHT-135, 410+COINXSIZE, GAME_HEIGHT-135+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(450, GAME_HEIGHT-135, 450+COINXSIZE, GAME_HEIGHT-135+COINYSIZE, fill='gold'))

        coins.append(canvas.create_rectangle(800, GAME_HEIGHT-135, 800+COINXSIZE, GAME_HEIGHT-135+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(840, GAME_HEIGHT-135, 840+COINXSIZE, GAME_HEIGHT-135+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(880, GAME_HEIGHT-135, 880+COINXSIZE, GAME_HEIGHT-135+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(920, GAME_HEIGHT-135, 920+COINXSIZE, GAME_HEIGHT-135+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(960, GAME_HEIGHT-135, 960+COINXSIZE, GAME_HEIGHT-135+COINYSIZE, fill='gold'))
        
        #Create mushrooms
        mushrooms.append(canvas.create_rectangle(1020, GAME_HEIGHT-130, 1020+MUSHROOMXSIZE, GAME_HEIGHT-130+MUSHROOMYSIZE, outline=''))
        mushroomImages.append(canvas.create_image(1020+MUSHROOMXSIZE/2, 770+MUSHROOMYSIZE/2, image=mushroomImg))

        #Initiate Mushroom moving direction 1 is right, -1 is left
        mushroomDirections = [-1 for i in range(len(mushrooms))]

        #Create the trophy
        trophy = canvas.create_rectangle(1550, GAME_HEIGHT-160, 1550+TROPHXSIZE, GAME_HEIGHT-160+TROPHYSIZE, outline='')
        trophyImage = canvas.create_image(1550+TROPHXSIZE/2, 740+TROPHYSIZE/2, image=trophyImg)

    elif currentLevel == 4: #Final level
        #Create the clouds
        clouds.append(canvas.create_image(50, 200, image=cloudImg))
        clouds.append(canvas.create_image(300, 300, image=cloudImg))
        clouds.append(canvas.create_image(600, 170, image=cloudImg))
        clouds.append(canvas.create_image(950, 270, image=cloudImg))
        clouds.append(canvas.create_image(1100, 160, image=cloudImg))
        clouds.append(canvas.create_image(1400, 310, image=cloudImg))
        
        #Create platforms
        platforms.append(canvas.create_rectangle(50, GAME_HEIGHT-350, 450, GAME_HEIGHT-300, fill='green'))
        platforms.append(canvas.create_rectangle(500, GAME_HEIGHT-200, 900, GAME_HEIGHT-150, fill='green'))
        platforms.append(canvas.create_rectangle(500, GAME_HEIGHT-500, 900, GAME_HEIGHT-450, fill='green'))
        platforms.append(canvas.create_rectangle(950, GAME_HEIGHT-100, 1250, GAME_HEIGHT-50, fill='green'))
        platforms.append(canvas.create_rectangle(1300, GAME_HEIGHT-200, 1600, GAME_HEIGHT-150, fill='green'))
        platforms.append(canvas.create_rectangle(1650, GAME_HEIGHT-300, 1950, GAME_HEIGHT-250, fill='green'))
        platforms.append(canvas.create_rectangle(2000, GAME_HEIGHT-400, 2300, GAME_HEIGHT-350, fill='green'))
        platforms.append(canvas.create_rectangle(2350, GAME_HEIGHT-500, 2650, GAME_HEIGHT-450, fill='green'))
        platforms.append(canvas.create_rectangle(2700, GAME_HEIGHT-600, 3100, GAME_HEIGHT-550, fill='green'))

        #Create coins
        coins.append(canvas.create_rectangle(650, GAME_HEIGHT-235, 650+COINXSIZE, GAME_HEIGHT-235+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(690, GAME_HEIGHT-235, 690+COINXSIZE, GAME_HEIGHT-235+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(730, GAME_HEIGHT-235, 730+COINXSIZE, GAME_HEIGHT-235+COINYSIZE, fill='gold'))

        coins.append(canvas.create_rectangle(1400, GAME_HEIGHT-235, 1400+COINXSIZE, GAME_HEIGHT-235+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(1440, GAME_HEIGHT-235, 1440+COINXSIZE, GAME_HEIGHT-235+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(1480, GAME_HEIGHT-235, 1480+COINXSIZE, GAME_HEIGHT-235+COINYSIZE, fill='gold'))

        coins.append(canvas.create_rectangle(2450, GAME_HEIGHT-535, 2450+COINXSIZE, GAME_HEIGHT-535+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(2490, GAME_HEIGHT-535, 2490+COINXSIZE, GAME_HEIGHT-535+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(2530, GAME_HEIGHT-535, 2530+COINXSIZE, GAME_HEIGHT-535+COINYSIZE, fill='gold'))

        coins.append(canvas.create_rectangle(2850, GAME_HEIGHT-635, 2850+COINXSIZE, GAME_HEIGHT-635+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(2890, GAME_HEIGHT-635, 2890+COINXSIZE, GAME_HEIGHT-635+COINYSIZE, fill='gold'))
        coins.append(canvas.create_rectangle(2930, GAME_HEIGHT-635, 2930+COINXSIZE, GAME_HEIGHT-635+COINYSIZE, fill='gold'))

        #Create Mushrooms
        mushrooms.append(canvas.create_rectangle(820, GAME_HEIGHT-530, 820+MUSHROOMXSIZE, GAME_HEIGHT-530+MUSHROOMYSIZE, outline=''))
        mushrooms.append(canvas.create_rectangle(1520, GAME_HEIGHT-230, 1520+MUSHROOMXSIZE, GAME_HEIGHT-230+MUSHROOMYSIZE, outline=''))
        mushrooms.append(canvas.create_rectangle(1870, GAME_HEIGHT-330, 1870+MUSHROOMXSIZE, GAME_HEIGHT-330+MUSHROOMYSIZE, outline=''))
        mushrooms.append(canvas.create_rectangle(2220, GAME_HEIGHT-430, 2220+MUSHROOMXSIZE, GAME_HEIGHT-430+MUSHROOMYSIZE, outline=''))
        mushrooms.append(canvas.create_rectangle(2570, GAME_HEIGHT-530, 2570+MUSHROOMXSIZE, GAME_HEIGHT-530+MUSHROOMYSIZE, outline=''))

        #Create mushroom images
        mushroomImages.append(canvas.create_image(820+MUSHROOMXSIZE/2, 370+MUSHROOMYSIZE/2, image=mushroomImg))
        mushroomImages.append(canvas.create_image(1520+MUSHROOMXSIZE/2, 670+MUSHROOMYSIZE/2, image=mushroomImg))
        mushroomImages.append(canvas.create_image(1870+MUSHROOMXSIZE/2, 570+MUSHROOMYSIZE/2, image=mushroomImg))
        mushroomImages.append(canvas.create_image(2220+MUSHROOMXSIZE/2, 470+MUSHROOMYSIZE/2, image=mushroomImg))
        mushroomImages.append(canvas.create_image(2570+MUSHROOMXSIZE/2, 370+MUSHROOMYSIZE/2, image=mushroomImg))

        #Initiate Mushroom moving direction 1 is right, -1 is left
        mushroomDirections = [-1 for i in range(len(mushrooms))]
        
        #Create the trophy
        trophy = canvas.create_rectangle(3050, GAME_HEIGHT-660, 3050+TROPHXSIZE, GAME_HEIGHT-660+TROPHYSIZE, outline='')
        trophyImage = canvas.create_image(3050+TROPHXSIZE/2, 240+TROPHYSIZE/2, image=trophyImg)

def getCheatCode(): #Function to get and return the cheat code upon entry button being pressed
    global cheatCode
    #Set cheat code to the code
    cheatCode = cheatCodeEntry.get()
    #Clear the entry box
    cheatCodeEntry.delete(0, END)
    #Allow focus back on the game when entered
    canvas.focus_set()

def destroyWidgets(leaderboardLabels): #Function to destroy all widgets on the main window
    canvas.delete(ALL)
    canvas.destroy()
    scoreLabel.destroy()
    cheatCodeLabel.destroy()
    cheatCodeEntry.destroy()
    cheatCodeBtn.destroy()
    controlButton.destroy()
    saveBtn.destroy()
    loadBtn.destroy()
    leaderboardTitleLabel.destroy()
    for i in range(len(leaderboardLabels)):
        leaderboardLabels[i].destroy()

def getUsername(): #Function to get the username from the username entry
    #Retrieves the username from the username entry when the enter button is pressed
    global username, leaderboard
    username = usernameEntry.get()

def saveLevel(): #Function to save the exact game state into a text file
    '''savefile format:
        score
        \n
        level
        \n
        platform coordinates (split by commas)
        \n
        coins
        \n
        enemies
        \n
        trophy
        \n
        playercoords
    '''
    stringToWrite = ''
    #Add the score
    stringToWrite += str(score)+'\n'

    #Add the current level
    stringToWrite += str(currentLevel)+'\n'

    #Add all the paltform coords
    for platform in platforms:
        stringToWrite += str(canvas.coords(platform)) + '|'
    stringToWrite += '\n'

    #Add all the coin coords
    for coin in coins:
        stringToWrite += str(canvas.coords(coin)) + '|'
    stringToWrite += '\n'

    #Add all the mushroom coords
    for mushroom in mushrooms:
        stringToWrite += str(canvas.coords(mushroom)) + '|'
    stringToWrite += '\n'
    
    #Add trophy coords and player coords
    stringToWrite += str(canvas.coords(trophy)) + '\n' + str(canvas.coords(playerHitBox))

    with open('saveFile.txt', 'w') as file:
        file.write(stringToWrite)

def loadLevel(): #Function to load a game from a text file
    global currentLevel
    global clouds
    global platforms
    global coins
    global mushrooms
    global mushroomDirections
    global trophy
    global playerHitBox
    global levelLabel
    global score
    global mushroomImages
    global trophyImage
    global playerImage
    mushrooms = []
    mushroomDirections = []
    mushroomImages = []

    with open('saveFile.txt', 'r') as file:
        score = int(file.readline().strip())
        currentLevel = int(file.readline().strip())
        platformCoords = file.readline().strip('|\n').split('|')
        coinCoords = file.readline().strip('|\n').split('|')
        mushroomCoords = file.readline().strip('|\n').split('|')
        trophyCoords = file.readline().strip()
        playerCoords = file.readline().strip()

    #Update the score to the previous score
    scoreLabel.config(text='Score: '+str(score))

    #Manipulate the line to be an array of integers without spaces
    platformPositions = []
    for platformCoord in platformCoords:
        platformCoord = platformCoord.strip('][').split(',')
        for i in range(len(platformCoord)):
            if i==0:
                platformCoord[i]=int(float(platformCoord[i]))
                continue
            platformCoord[i]=int(float(platformCoord[i][1:]))
        platformPositions.append(platformCoord)

    #Manipulate the line to be an array of integers without spaces
    coinPositions = []
    if not(coinCoords==['']):
        for coinCoord in coinCoords:
            coinCoord = coinCoord.strip('][').split(',')
            for i in range(len(coinCoord)):
                if i==0:
                    coinCoord[i]=int(float(coinCoord[i]))
                    continue
                coinCoord[i]=int(float(coinCoord[i][1:]))
            coinPositions.append(coinCoord)

    #Manipulate the line to be an array of integers without spaces
    mushroomPositions = []
    if not(mushroomCoords == ['']):
        for mushroomCoord in mushroomCoords:
            mushroomCoord = mushroomCoord.strip('][').split(',')
            for i in range(len(mushroomCoord)):
                if i==0:
                    mushroomCoord[i]=int(float(mushroomCoord[i]))
                    continue
                mushroomCoord[i]=int(float(mushroomCoord[i][1:])) #Remove the space
            mushroomPositions.append(mushroomCoord)
        
    trophyCoords = trophyCoords.strip('][').split(',')
    for i in range(len(trophyCoords)):
        if i==0:
            trophyCoords[i]=int(float(trophyCoords[i]))
            continue
        trophyCoords[i]=int(float(trophyCoords[i][1:]))

    playerCoords = playerCoords.strip('][').split(',')
    for i in range(len(playerCoords)):
        if i==0:
            playerCoords[i]=int(float(playerCoords[i]))
            continue
        playerCoords[i]=int(float(playerCoords[i][1:]))

    canvas.delete(ALL)

    platforms = []
    mushrooms = []
    coins = []
    clouds = []

    trophy = ''
    playerHitBox = ''

    #Create the clouds
    clouds.append(canvas.create_image(50, 200, image=cloudImg))
    clouds.append(canvas.create_image(300, 300, image=cloudImg))
    clouds.append(canvas.create_image(600, 170, image=cloudImg))
    clouds.append(canvas.create_image(950, 270, image=cloudImg))
    clouds.append(canvas.create_image(1100, 160, image=cloudImg))
    clouds.append(canvas.create_image(1400, 310, image=cloudImg))

    #Load the platforms
    for platformCoord in platformPositions:
        platforms.append(canvas.create_rectangle(platformCoord[0], platformCoord[1], platformCoord[2], platformCoord[3], fill='green'))

    #Load the coins
    for coinCoord in coinPositions:
        coins.append(canvas.create_rectangle(coinCoord[0], coinCoord[1], coinCoord[2], coinCoord[3], fill='gold'))

    #load the mushrooms
    for mushroomCoord in mushroomPositions:
        mushrooms.append(canvas.create_rectangle(mushroomCoord[0], mushroomCoord[1], mushroomCoord[2], mushroomCoord[3], outline=''))
        #Create mushroom images
        mushroomImages.append(canvas.create_image(mushroomCoord[0]+MUSHROOMXSIZE/2, mushroomCoord[1]+MUSHROOMYSIZE/2, image=mushroomImg))

    #Reset the mushroom direction array
    mushroomDirections = [-1 for i in range(len(mushrooms))]

    #Load the trophy
    trophy = canvas.create_rectangle(trophyCoords[0], trophyCoords[1], trophyCoords[2], trophyCoords[3], outline='')
    trophyImage = canvas.create_image(trophyCoords[0]+TROPHXSIZE/2, trophyCoords[1]+TROPHYSIZE/2, image=trophyImg)

    #Load the player
    playerHitBox = canvas.create_rectangle(playerCoords[0], playerCoords[1], playerCoords[2], playerCoords[3], outline='') #no fill and outline=''
    playerImage = canvas.create_image(playerCoords[0]+PLAYERXSIZE/2, playerCoords[1]+PLAYERYSIZE/2, image=standingImg)

    #Reprint score label
    levelLabel = canvas.create_text(80, 20, text='Level: '+str(currentLevel), font=('Arial', 30), fill = 'black')


#Set up window
window = Tk()
window.title('Super Mario Bros')
window.config(bg='white')

# window.attributes('-fullscreen', True)
window.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")

#Set up canvas
canvas = Canvas(window, bg=BACKGROUND_COLOUR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack(side='left')

#Set up score and create the label
score = 0
scoreLabel = Label(window, text='Score: '+str(score), font=('Arial', 40), bg='white', fg='black')
scoreLabel.pack(pady=(50, 0))

#Create the label to show where the cheat code is
cheatCodeLabel = Label(window, text='Cheat code: ', font=('Arial', 25), bg='white', fg='black')
cheatCodeLabel.pack(pady=(30, 0))

#Create an entry box to enter cheat code
cheatCodeEntry = Entry(window, width=int(0.1*SCREEN_WIDTH), fg='black', bg='white', insertbackground='black')
cheatCodeEntry.pack(padx=5)

#Create an entry button
cheatCodeBtn = Button(window, text='Enter', command=getCheatCode, bg='white', fg='black')
cheatCodeBtn.pack(pady=(5, 20))

#Create a button to switch between controls
controls = 'WASD'
controlButton = Button(window,  width=8, height=2, text=controls, command=UserOption, bg='white', fg='black', font=('Arial', 30))
controlButton.pack(pady=(20, 0))

#Create leaderboard
leaderboardTitleLabel = Label(window, text='Leaderboard: ', font=('Arial', 30), bg='white', fg='black')
leaderboardTitleLabel.pack(anchor='w', pady=(30, 5))

#Open leaderboards file
with open('leaderboard.txt', 'r') as leaderboardFile:
    leaderboardLabels = [] #Save an array of the printed labels to delete later
    leaderboard = [] #Save the leaderbaord so it can be amended later
    for i in range(1, 6):
        entry = leaderboardFile.readline().split(' ')
        if entry == ['']: #If there is no entry yet for this position print wihtout a name
            leaderboardLabel = Label(window, text=str(i)+'. ', font=('Arial', 20), bg='white', fg='black')
        else: 
            entry[1] = entry[1].rstrip() #remove the new line
            leaderboard.append(entry)
            leaderboardLabel = Label(window, text=str(i)+'. '+' '.join(entry[:-1])+' '+entry[-1], font=('Arial', 20), bg='white', fg='black')
        leaderboardLabel.pack(anchor='w') #Anchor to the left
        leaderboardLabels.append(leaderboardLabel)

#Create a save button
saveBtn = Button(window, text='Save', width=8, height=2, command=saveLevel, font=('Arial', 30), bg='white', fg='black')
saveBtn.pack(pady=(60, 0))

#Create a load button
loadBtn = Button(window, text='Load', width=8, height=2, command=loadLevel, font=('Arial', 30), bg='white', fg='black')
loadBtn.pack(pady=(30, 0))

#Bind the key press and key release
canvas.bind('<KeyPress>', lambda event: setMovement(event))
canvas.bind('<KeyRelease>', lambda event: removeMovement(event))

#Set pause to space key
canvas.bind('<space>', pauseGame)

#Bind the boss key
canvas.bind('<b>', setBossKey)

canvas.focus_set()

#Open all the images
#Mario images
standingImg = ImageTk.PhotoImage(Image.open('MarioStanding.png'))
rightRunningImg1 = ImageTk.PhotoImage(Image.open('MarioRun1.png'))
rightRunningImg2 = ImageTk.PhotoImage(Image.open('MarioRun2.png'))
rightRunningImg3 = ImageTk.PhotoImage(Image.open('MarioRun3.png'))
leftRunningImg1 = ImageTk.PhotoImage(Image.open('MarioRun1.png').transpose(Image.FLIP_LEFT_RIGHT))
leftRunningImg2 = ImageTk.PhotoImage(Image.open('MarioRun2.png').transpose(Image.FLIP_LEFT_RIGHT))
leftRunningImg3 = ImageTk.PhotoImage(Image.open('MarioRun3.png').transpose(Image.FLIP_LEFT_RIGHT))
rightJumpingImg = ImageTk.PhotoImage(Image.open('MarioJump.png'))
leftJumpingImg = ImageTk.PhotoImage(Image.open('MarioJump.png').transpose(Image.FLIP_LEFT_RIGHT))

#Intialise run image variable to flip through the running states
runImage = 1

#Trophy image
trophyImg = ImageTk.PhotoImage(Image.open('Trophy.png'))

#Mushroom image
mushroomImg = ImageTk.PhotoImage(Image.open('Mushroom.png'))

#Cloud image
cloudImg = ImageTk.PhotoImage(Image.open('cloudImage.png'))

#Boss image
bossImg = ImageTk.PhotoImage(Image.open('bossImage.jpeg').resize((SCREEN_WIDTH, SCREEN_HEIGHT)))

#Instantiate the platforms array
platforms = []

#Instantiate the mushrooms array
mushrooms = []

#Instantiate the coins array
coins = []

#Instantiate the clouds
clouds = []

#Instantiate the player hit box and image (the hitbox is invisible in gameplay)
playerHitBox = canvas.create_rectangle(PLAYERSTARTPOS[0], PLAYERSTARTPOS[1], PLAYERSTARTPOS[0] + PLAYERXSIZE, PLAYERSTARTPOS[1]+ PLAYERYSIZE, outline='') #no fill and outline=''
playerImage = canvas.create_image(PLAYERSTARTPOS[0]+PLAYERXSIZE/2, PLAYERSTARTPOS[1]+PLAYERYSIZE/2, image=standingImg)


#Initiate YVelocity
YVelocity = INTIAL_FALL_VELOCITY

#Initiate Movements
jumping = False
falling = False
right = False
left = False
up = False
down = False

#Initiate the level
currentLevel = 1
#Create level label
levelLabel = canvas.create_text(80, 20, text='Level: '+str(currentLevel), font=('Arial', 30), fill = 'black')

#Print level
printLevel()

#Insantiate cheat code
cheatCode = ''

#Instantiate bosskey
bosskey = False
bosskeyOn = False

#Initally don't have a pause and countdown
pause = False
countdownOn = False

run = True
completed = False

while run:
    if not(pause): #If pause have no movement on the window
        if cheatCode == 'Score': #Check if cheat code is score
            score += 1000
            scoreLabel.config(text='Score: '+str(score)) #Update the score label
            cheatCode = '' #Reset cheat code to only allow for a single increase in score
            
        #Check if player has collided with mushrooms and move the mushrooms
        for mushroomIndex, mushroom in enumerate(mushrooms):
            #Check the mushroom on the side of the platform and change direction
            if mushroomOnSideOfPlatform(mushroom, platforms): #Reverse directon if on the side of the platform
                mushroomDirections[mushroomIndex] = -mushroomDirections[mushroomIndex]
            elif checkCollisionsWithTopMushroom(playerHitBox, mushroom): #Check if the player has jumped on the mushroom
                canvas.delete(mushroom) #Delete the mushroom
                canvas.delete(mushroomImages[mushroomIndex])
                mushrooms.pop(mushroomIndex) #Remove from the array
                mushroomImages.pop(mushroomIndex)
                mushroomDirections.pop(mushroomIndex)
                score += 50
                scoreLabel.config(text='Score: '+str(score))
                continue
            elif checkCollisionsWithSideMushroom(playerHitBox, mushroom): #Check if the player has touched the side of the mushroom
                #End the game
                destroyWidgets(leaderboardLabels)
                mushrooms = []
                coins = []
                clouds = []
                run = False
                break
            #Move mushroom to simulate mushroom moving
            canvas.move(mushroom, mushroomDirections[mushroomIndex]*MUSHROOM_MOVE_SPEED, 0)
            canvas.move(mushroomImages[mushroomIndex], mushroomDirections[mushroomIndex]*MUSHROOM_MOVE_SPEED, 0)
        
        #Break out of while loop if run is false as the previous break only exits the for loop
        if run==False:
            break

        #Check if player has collided with coins
        for coinIndex, coin in enumerate(coins):
            #Check player has collided with coins
            if checkCollisionWithCoin(playerHitBox, coin):
                canvas.delete(coin) #Remove coin from canvas
                coins.pop(coinIndex) #Remove coin from array
                score += 100
                scoreLabel.config(text='Score: '+str(score)) #Update the score label

        #Check if player has collided with the winners trophy
        if checkCollisionWithTrophy(playerHitBox, trophy):
            #Move to next level
            if currentLevel == 1:
                currentLevel = 2
            elif currentLevel == 2:
                currentLevel = 3
            elif currentLevel == 3:
                currentLevel = 4
            elif currentLevel == 4:
                #final level so end the game
                destroyWidgets(leaderboardLabels)
                score += 500
                run = False
                completed = True
                break
            #Delete everything from canvas
            canvas.delete(ALL)
            platforms = []
            mushrooms = []
            coins = []
            clouds = []

            #Print new level
            printLevel()

            #Reset player coords for hitbox and image
            playerHitBox = canvas.create_rectangle(PLAYERSTARTPOS[0], PLAYERSTARTPOS[1], PLAYERSTARTPOS[0] + PLAYERXSIZE, PLAYERSTARTPOS[1]+ PLAYERYSIZE, outline='')
            playerImage = canvas.create_image(PLAYERSTARTPOS[0]+PLAYERXSIZE/2, PLAYERSTARTPOS[1]+PLAYERYSIZE/2, image=standingImg)

            if currentLevel==4:
                #Move the player as they will start in a different position
                canvas.move(playerHitBox, 0, -300) #Move up to new platform
                canvas.move(playerImage, 0, -300)

            #Reprint level label
            levelLabel = canvas.create_text(80, 20, text='Level: '+str(currentLevel), font=('Arial', 30), fill = 'black')
        
        if cheatCode == 'Fly': #Allow user to user all arrows or WASD to move
            if up:
                if not(checkCollisionsWithBottomPlatforms(playerHitBox, platforms)): #Don't allow the user to go through platforms
                    canvas.move(playerHitBox, 0, -7)
                    canvas.move(playerImage, 0, -7)
                    
            elif down:
                if not(checkCollisionsWithTopPlatforms(playerHitBox, platforms)): #Don't allow the user to go through platforms
                    canvas.move(playerHitBox, 0, 7)
                    canvas.move(playerImage, 0, 7)
                    
        else:
            #Check if the player is on a platform 
            falling = not(checkCollisionsWithTopPlatforms(playerHitBox, platforms))
            if jumping:
                if checkCollisionsWithBottomPlatforms(playerHitBox, platforms): #Check if the player has hit the bottom of the platform
                    jumping = False
                #Run the jumping mechanism
                canvas.move(playerHitBox, 0, -YVelocity)
                canvas.move(playerImage, 0, -YVelocity)
                YVelocity = YVelocity - GRAVITY #Increase height slower as they jump heigher
                if YVelocity < 0:
                    jumping = False
                    YVelocity = INTIAL_FALL_VELOCITY
                    falling = True

            elif falling: #Have the player fall down
                canvas.move(playerHitBox, 0, YVelocity)
                canvas.move(playerImage, 0, YVelocity)
                YVelocity = YVelocity + GRAVITY #Fall down faster the longer the player is falling
            else:
                YVelocity = INTIAL_FALL_VELOCITY #Reset inital fall velocity and don't move the players y coordinate

        if right:
            leftCollide, distToMove = checkCollisionsWithLeftSidePlatforms(playerHitBox, platforms)
            if leftCollide: #Check if the player is colliding with the left side of a platform
                right = False
                #Adjust all the objects so player isn't inside a platform
                for platform in platforms: #Move all plaforms
                    canvas.move(platform, distToMove, 0)
                for mushroom in mushrooms: #Move all the mushrooms
                    canvas.move(mushroom, distToMove, 0)
                for coin in coins: #Move all the coins
                    canvas.move(coin, distToMove, 0)
                for mushImg in mushroomImages: #Move all the mushroom images
                    canvas.move(mushImg, distToMove, 0)
                canvas.move(trophy, distToMove, 0) #move the trophy
                canvas.move(trophyImage, distToMove, 0)
            else:
                for platform in platforms: #Move all plaforms
                    canvas.move(platform, -7, 0)
                for mushroom in mushrooms: #Move all the mushrooms
                    canvas.move(mushroom, -7, 0)
                for coin in coins: #Move all the coins
                    canvas.move(coin, -7, 0)
                for mushImg in mushroomImages: #Move all the mushroom images
                    canvas.move(mushImg, -7, 0)
                canvas.move(trophy, -7, 0) #move the trophy
                canvas.move(trophyImage, -7, 0)

        elif left:
            rightCollide, distToMove = checkCollisionsWithRightSidePlatforms(playerHitBox, platforms)
            if rightCollide: #Check if the player is colliding with the right side of a platform
                left = False
                #Adjust all the objects so player isn't inside a platform
                for platform in platforms: #Move all plaforms
                    canvas.move(platform, -distToMove, 0)
                for mushroom in mushrooms: #Move all the mushrooms
                    canvas.move(mushroom, -distToMove, 0)
                for coin in coins: #Move all the coins
                    canvas.move(coin, -distToMove, 0)
                for mushImg in mushroomImages: #Move all the mushroom images
                    canvas.move(mushImg, -distToMove, 0)
                canvas.move(trophy, -distToMove, 0) #move the trophy
                canvas.move(trophyImage, -distToMove, 0)
            else:
                for platform in platforms: #Move all plaforms
                    canvas.move(platform, 7, 0)
                for mushroom in mushrooms: #Move all the mushrooms
                    canvas.move(mushroom, 7, 0)
                for coin in coins: #Move all the coins
                    canvas.move(coin, 7, 0)
                for mushImg in mushroomImages: #Move all the mushroom images
                    canvas.move(mushImg, 7, 0)
                canvas.move(trophy, 7, 0) #Move the trophy
                canvas.move(trophyImage, 7, 0)
        
        #Check if player touches the bottom of the screen
        if canvas.coords(playerHitBox)[3] >= GAME_HEIGHT:
            destroyWidgets(leaderboardLabels)
            mushrooms = []
            coins = []
            clouds = []
            run = False
            break

        #Set images for certain cases of the players movement
        if (falling or jumping) and right:
            canvas.itemconfigure(playerImage, image=rightJumpingImg)
        if (falling or jumping) and left:
            canvas.itemconfigure(playerImage, image=leftJumpingImg)
        elif not(falling) and not(jumping) and right:
            if runImage == 1:
                canvas.itemconfigure(playerImage, image=rightRunningImg1)
            elif runImage == 3:
                canvas.itemconfigure(playerImage, image=rightRunningImg2)
            elif runImage == 6:
                canvas.itemconfigure(playerImage, image=rightRunningImg3)
            elif runImage == 9:
                runImage = 1
            runImage += 1
        elif not(falling) and not(jumping) and left:
            if runImage == 1:
                canvas.itemconfigure(playerImage, image=leftRunningImg1)
            elif runImage == 3:
                canvas.itemconfigure(playerImage, image=leftRunningImg2)
            elif runImage == 6:
                canvas.itemconfigure(playerImage, image=leftRunningImg3)
            elif runImage == 9:
                runImage = 1
            runImage += 1
        elif not(falling) and not(jumping) and not(right) and not(left):
            canvas.itemconfigure(playerImage, image=standingImg)
            runImage = 1
            
        #Move clouds
        for cloud in clouds:
            if canvas.coords(cloud)[0]+CLOUDXSIZE<=0:
                canvas.move(cloud, 1640, 0)
            canvas.move(cloud, -random.randint(0, 2), 0)

    if bosskey:
        #Create a window on top of the screen
        bossWindow = Toplevel()
        bossWindow.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        bossWindow.title('Not suspicious excel sheet')
        #Create a canvas to print the image and bind the delete key
        bossCanvas = Canvas(bossWindow, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        bossCanvas.pack()
        bossImage = bossCanvas.create_image(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, image=bossImg)
        #Press any key to resume game
        bossCanvas.bind('<KeyPress>', deleteBossWindow)
        bossCanvas.focus_set()
        #Set boss key to false to stop creating multiple windows
        bosskey = False
        #Pause game until the window is deleted
        pause = True
    
    #Have a pause to create a framerate
    sleep(1/60)
    window.update()

#Ouput a game over label
if completed: #Print a completed message
    gameOverLabel = Label(window, text='Game Completed!', font=('Arial', 100), bg='white', fg='black')
else: #print a game over message
    gameOverLabel = Label(window, text='Game Over', font=('Arial', 100), bg='white', fg='red')
gameOverLabel.pack(pady=(300, 0))

#Output a label for the user to enter a username
usernameLabel = Label(window, text='Enter your username: ', font=('Arial', 35), bg='white', fg='black')
usernameLabel.pack(pady=(60, 30))

#Output an entry for the user to enter username
usernameEntry = Entry(window, width=100, fg='black', bg='white', insertbackground='black', borderwidth=1)
usernameEntry.pack(padx=30)
usernameEntry.focus()

#Button submit username
usernameBtn = Button(window, width=6, height=1, text='Enter', command=getUsername, bg='white', fg='black', font=('Arial', 25))
usernameBtn.pack(pady=(5, 20))

username = ''

#Wait until the user has entered a username
while True:
    if username.__contains__(' '):
        usernameEntry.delete(0, END)
        username = ''
        continue
    if username != '':
        break
    window.update()

# Sort leaderboard and put user in the correct location in the leaderboard when user has entered their username
for i in range(0, len(leaderboard)):
    if int(leaderboard[i][1])<score:
        leaderboard.insert(i, [username, str(score)])
        break

#Cut leaderboard to top 5
leaderboard = leaderboard[:5]

#Create string to add to file
stringToWrite = ''
for i in range(0, len(leaderboard)):
    if i == 4: #For the last entry don't add a new line
        stringToWrite = stringToWrite + leaderboard[i][0] + ' ' + leaderboard[i][1]
    else: 
        stringToWrite = stringToWrite + leaderboard[i][0]+ ' ' + leaderboard[i][1]+'\n'

#Save leaderboard to file
with open('leaderboard.txt', 'w') as leaderboardFile:
    leaderboardFile.write(stringToWrite)

window.mainloop()