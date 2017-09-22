####################################
# Name: Dina Chen 
# CMU 15-112 Term Project | June 2016
# Requries Python3
# Barebones interface base code provided by course instructors
# all other code is original
####################################

from tkinter import *
import random



# global variables
white="gray90"
black="gray10"
scores=[0]

####################################
# init
####################################

def init(data,mode="splashScreen",difficulty='EASY'):
    data.cubesize = data.width*.2
    data.mode = mode
    data.previousMode=''
    data.difficulty=difficulty

    data.bg_color=black
    data.player=Player(data)
    data.cx=data.width/2
    data.cy=data.height/2

    data.gravity=1.5
    data.timer=0
    data.maxVelocity=15
    data.timeOnCube=1
    data.start=False
    data.seconds=120 # start the with 2:00min
    data.score=0

    data.cubes=[]           # all cubes in the map
    data.cubesInView=[]     # all cubes visiblze on the window
    data.cubesNearPlayer=[] # maximum 4 nearest cubes to player (N/S/E/W) 


    helpCubeList=[[
    0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,white,black,black,white,0,0]]

    tutorial1 = [
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,white,black,0,0,0]]

    tutorial4 = [
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,black,white,black,white,0,0]]

    if data.mode=='splashScreen':
        cubeList=[
        [0,0,0,0,0,0,0],
        [0,black,white,black,white,black,0],
        [0,white,black,white,black,white,0],
        [0,black,white,black,white,black,0],
        [0,white,black,white,black,white,0]
        ] 
        cubeList=[
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [black,white,black,white,black,white,black],
        [white,black,white,black,white,black,white],
        [black,white,black,white,black,white,black],
        [white,black,white,black,white,black,white],
        ] 
    
    
    if data.mode=='playGame':
        cubeList=makeRandom2DWorld(data)

    data.helpCubes=sorted(makeCubeData(data,helpCubeList))
    data.cubes=sorted(makeCubeData(data,cubeList))
    data.tutorial1=sorted(makeCubeData(data,tutorial1))
    data.tutorial4=sorted(makeCubeData(data,tutorial4))
    


    # Buttons throughout the game
    home_help = Button(data.cubesize*2,data.cubesize*2,
        ' H E L P \n  < H > ',white,data,'help')
    home_tutorial = Button(data.cubesize*4,data.cubesize*2,
        'TUTORIAL\n     < T >',white,data,'tutorial')
    home_easy = Button( data.cubesize*2,data.cubesize*4,
        'E A S Y \n < E >',white,data,'playGame')
    home_hard = Button(data.cubesize*4,data.cubesize*4,
        'H A R D\n < D >',white,data,'playGame')


    help_tutorial = Button(data.cubesize*3,data.cubesize*4,
        'TUTORIAL\n    < T >',white,data,'tutorial')
    help_back = Button(data.cubesize*2,data.cubesize*4,
        'BACK\n < B > ',white,data,data.previousMode)


    tutorial_back = Button(data.cubesize*.75,data.cubesize*1.5,
        'BACK\n< B > ',white,data,data.previousMode)

    tutorial_main = Button(data.cubesize*4.25,data.cubesize*1.5,
        'MAIN MENU\n     < M > ',white,data,'splashScreen')

    try_again = Button(data.cubesize*3,data.cubesize*4,
        'TRY \n AGAIN \n < T >', white, data,'playGame')
    data.splashButtons=[home_tutorial,home_easy,home_hard,home_help]
    data.helpButtons=[help_tutorial,help_back]
    data.gameOverButtons=[help_back,try_again]
    data.tutorialButtons=[tutorial_back,tutorial_main]
    data.tutorialmode=1


    # Info in tutorial
    data.zcount = 0

    data.text1 = [  'Welcome to Illusion-Z, a 2D-3D platform game.','',
                    'Control your x-y position with the arrow keys.',
                    'Control the state of the world using the  < Z > key.',
                    'Go ahead and try it now.']
    data.text2 = [  'Good.','You can only pass through transparent cubes.']
    data.text3 = [  '','You can only pass through transparent cubes.',
                    'Try standing on the black cube.']
    data.text4 = [  'Inverting the world while inside a cube',
                    'causes it to disappear from the map.',''
                    'The goal is to remove as many cubes as possible in the given time.','',
                    'Try removing all the cubes from the screen.']
    data.text4a= [  '','',
                    'In the game, you can lose by falling off the screen.',
                    'Be careful about which cubes you remove!',]
    data.text5 = [  'In HARD MODE, cubes will fall away', 
                    'after stood on for a short period of time.',
                    'You do not earn points from cubes that fall.','',
                    'Remove the cubes from the screen by standing on them.']
    data.text6 = [  'Nice job!',"You're ready to play.",''
                    ]

    
class Button(object):
    def __init__(self,x,y,text,color,data,mode):
        self.x=x
        self.y=y
        self.width=data.cubesize
        self.height=data.cubesize #makes cube sized buttons
        self.bounds=getBounds(self)
        self.text=text
        if text == 'H A R D\n < D >': self.difficulty='HARD'
        else: self.difficulty='EASY'
        self.color=color
        self.mode=mode


    def draw(self,canvas):
        canvas.create_text(self.x,self.y,text=self.text,
            fill=self.color,font='Impact 30')

    


# may want to consider new classes for body parts
# as head/body/legs/shadow may have different animation patterns
class Player(object):
    def __init__(self,data):
        self.width=20
        self.height=60
        self.x=data.cubesize*3.15
        self.y=data.cubesize*3.15
        (self.velocity_x,self.velocity_y)=(0,0)
        
        self.maxspeed=15
        self.bounds=getBounds(self)
        


    def draw(self,canvas,data):      
        (x1,y1,x2,y2)=self.bounds
        headsize=(self.width) 
        neck=((x1+x2)/2,y1+headsize) #tip of body triangle

        if data.bg_color==white:
            color=black
            shadowcolor = "grey10"
        if data.bg_color==black: 
            color=white
            shadowcolor="grey30"
        if data.mode=='splashScreen':
            shadowcolor=None


        if data.player.isOnSolidCube(data):
                canvas.create_oval(x1,y2-5,x2,y2+5,
                          fill=shadowcolor,width=0)

        # body is a triangle
        canvas.create_polygon(neck,x1,y2,x2,y2,
                                fill=color,width=0)

        # head 
        # small adjustments to the head position based on movement
        # give a sense of responsiveness
        if (data.mode == 'playGame'):
            velocity_x = data.cubes[0].velocity_x
            velocity_y = data.cubes[0].velocity_y
        elif (data.mode == 'splashScreen' or 'help'):
            velocity_x = -data.player.velocity_x*2
            velocity_y = -data.player.velocity_y*2.5

        if velocity_x>5: x1+=5
        elif velocity_x<-5: x1-=5
        elif velocity_x>3: x1+=3
        elif velocity_x<-3: x1-=3
        elif velocity_x>2: x1+=1
        elif velocity_x<-2: x1-=1
        else: x1=self.bounds[0]

        if velocity_y<-4:y1-=5
        elif velocity_y<-3:y1-=3
        elif velocity_y<-2:y1-=1
        else: y1=self.bounds[1]

        canvas.create_oval(x1,y1+5,x1+headsize,y1+headsize+5,
                                          fill=color,width=0)




    def isOnSolidCube(self,data): 
        feet = self.y+self.height/2
        for cube in data.cubesNearPlayer:
            (corners1,corners2,x,y,width,height,
             upper,lower,left,right,midpoints)=cube.initVariableNames()
            if data.mode=='playGame'or 'help':
                if (cube.isSolid and left<self.x<right  and 
                    feet<upper and feet>upper-25): 
                    return True
            if data.mode=='splashScreen' or 'tutorial':
                if (cube.isSolid and left<self.x<right and
                    feet<upper and feet>upper-1): return True
        return False


    def hitCubeLeft(self,data):
        player_right= self.x+self.width/2
        player_left = self.x-self.width/2

        for cube in data.cubesNearPlayer:
            (corners1,corners2,x,y,width,height,
             upper,lower,left,right,midpoints)=cube.initVariableNames()

            if (cube.isSolid and 
                upper-self.height/2<self.y<lower+self.height/2 and
                player_right<left and 
                player_left>left-self.width-10):
                    return True # 10 px padding
        return False

    def hitCubeRight(self,data):
        player_right= self.x+self.width/2
        player_left = self.x-self.width/2

        for cube in data.cubesNearPlayer:
            (corners1,corners2,x,y,width,height,
             upper,lower,left,right,midpoints)=cube.initVariableNames()

            if (cube.isSolid and 
                upper-self.height/2<self.y<lower+self.height/2 and
                player_left>right and 
                player_right<right+self.width+10): # 10 px padding
                    return True                         
        return False

    def isInCube(self,data):
        for cube in data.cubesNearPlayer:
            (corners1,corners2,x,y,width,height,
             upper,lower,left,right,midpoints)=cube.initVariableNames()
            if (lower>self.y>upper and left<self.x<right): return True
        return False


    def isFalling(self,data):
        if data.mode=='playGame': return data.cubes[0].velocity_y<0
        return data.player.velocity_y>0
    def isJumping(self,data):
        return data.cubes[0].velocity_y>0
    def isMovingLeft(self,data):
        if data.mode=='playGame': return data.cubes[0].velocity_x>0
        return data.player.velocity_x<0
    def isMovingRight(self,data):
        if data.mode=='playGame': return data.cubes[0].velocity_x<0
        return data.player.velocity_x>0
    def move(self,dx=0,dy=0):
        if (dx,dy)==(0,0):
            (dx,dy)=(self.velocity_x,self.velocity_y)
        self.x+=self.velocity_x
        self.y+=self.velocity_y
        self.bounds=getBounds(self)


class Cube(object):
    def __init__(self,x,y,data,color=black):
        (cx,cy)=(data.cx,data.cy)
        self.color=color
        (self.x,self.y)=(x,y)

        self.width=self.height=data.cubesize
        self.square1=Square(x,y,data.cubesize) #larger square
        self.square2=Square(x+(cx-x)*.25,y+(cy-y)*.25,data.cubesize*.75) #smaller square
        self.defineSolid(data)
        self.distFromCenter(data)
        self.drop=False

        (self.velocity_x,self.velocity_y)=(0,0)

    # I redefined less than in order to sort according to delta_cx
    # cubes further from the center are sorted (thus drawn) first
    # cubes  closer   to the center are sorted (thus drawn) last
    # preventing overlapping of 'hidden' faces
    def __lt__(self,other):
        if  abs(self.delta_cx)> abs(other.delta_cx): return True
        if (abs(self.delta_cx)==abs(other.delta_cx) and
            abs(self.delta_cy)> abs(other.delta_cy)): return True
        else: return False

    # can be called inside other functions to quickly generate
    # shorter variable names in one line using the method
    def initVariableNames(self):
        square1=self.square1.corners 
        square2=self.square2.corners
        NW = square2[0]
        NE = square2[1]
        SE = square1[1]
        SW = square1[0]

        # top face midpoints
        midpoints = (getMidpoint(NW,SW),getMidpoint(NE,SE))

        x = self.x
        y = self.y
        width=self.width
        height=self.height
        upper = y-height/2
        lower = y+height/2
        left  = x-width/2
        right = x+width/2

        return (square1,square2,x,y,width,height,upper,lower,left,right,midpoints)

    # returns distance of center front face of the cube to the
    # center of the screen
    def distFromCenter(self,data):
        self.delta_cy=self.y-data.cy
        self.delta_cx=self.x-data.cx


    # cube is solid when its color is opposite of bg color
    def defineSolid(self,data):
        self.isSolid=(self.color!=data.bg_color and self.color!=None)


    def isInView(self,data): 
        (corners1,corners2,x,y,width,height,
         upper,lower,left,right,midpoints)=self.initVariableNames()
        margin= 100
        upper -=1000 #causes player to fall a bit longer before game over
        lower +=margin
        left  -=margin
        right +=margin
        
        if (lower < 0 or upper > data.height or
            right  < 0 or left > data.width): return False
        else: return True


    # determines which quadrant with respect to the viewing screen
    # necessary for determining the order of faces drawn in perspective
    # returns a string representing UpRight, UpLeft, DownRight, DownLeft
    # also relevant: if they fall in a MiddleHorizontal or MiddleVertical 

    def getQuadrant(self,data): 
        (corners1,corners2,x,y,width,height,
         upper,lower,left,right,midpoints)=self.initVariableNames()

        location = ""
        if data.mode=='playGame':
            if lower<=data.cy: location+='U' 
            if upper>=data.cy: location+='D' 
            if right< data.cx: location+='L'
            if left > data.cx: location+='R'

            if len(location)!=2: 
                location='MV'# default
                if lower>data.cy and upper<data.cy: location='MH'
        else:
            if lower<=data.cy: location+='U' 
            if upper>=data.cy: location+='D' 
            if right<= data.cx: location+='L'
            if left >= data.cx: location+='R'


            if len(location)!=2: 
                location='MV'# default
                if lower>data.cy and upper<data.cy: location='MH'
        
        return location


    def castShadow(self,canvas,data):
        (corners1,corners2,x,y,width,height,
         upper,lower,left,right,midpoints)=self.initVariableNames()

        lightColors=["grey90","grey80","grey50","grey30"]
        darkColors=["grey20","grey15","grey10","grey10"]

        if self.color==white: colors=lightColors
        if self.color==black: colors= darkColors

        canvas.create_polygon(midpoints,corners2[1],corners2[0],fill=colors[-1])


    def draw(self,canvas,data):
        (corners1,corners2,x,y,width,height,
         upper,lower,left,right,midpoints)=self.initVariableNames()

        #gradient of shadese from lightest to darkest
        lightColors=["grey90","grey80","grey50","grey30"]
        darkColors=["grey20","grey15","grey10","grey10"]

        if self.color==white: colors=lightColors

        if self.color==black: colors= darkColors



        def fillFront():
            canvas.create_polygon(corners1,fill=colors[1])

        def fillBottom():
            canvas.create_polygon(corners2[2],corners2[3], 
                                  corners1[3],corners1[2],
                                           fill=colors[3])
        def fillTop():
            canvas.create_polygon(corners2[0],corners2[1],
                                  corners1[1],corners1[0],
                                           fill=colors[0])
        def fillLeft():
            canvas.create_polygon(corners2[0],corners2[3], 
                                  corners1[3],corners1[0],
                                            fill=colors[2])
        def fillRight():
            canvas.create_polygon(corners2[1],corners2[2],
                                  corners1[2],corners1[1],
                                           fill=colors[2])


        if self.isSolid:
            quadrant=self.getQuadrant(data)

            if quadrant[0]=='U': fillBottom()
            if quadrant[1]=='L': fillRight()
            if quadrant[1]=='R': fillLeft()
            if quadrant[0]=='D': fillTop()

            if quadrant=="MV": 
                fillTop()
                fillBottom()
            if quadrant=='MH':
                fillLeft()
                fillRight()

            fillFront()

        if not self.isSolid and self.color != None: 
            if data.bg_color==black: color = white
            elif data.bg_color==white: color = black
            
            self.square1.draw(canvas,color)
            self.square2.draw(canvas,color)
            for i in range(4): #Draws 4 corner connecting lines
                canvas.create_line(corners1[i],corners2[i],dash=(1,5),
                                             fill=color)


        # debugging purposes only - draw center vanishing point
        #canvas.create_oval(data.cx-2,data.cy-2,data.cx+2,data.cy+2,fill="red")
        # draw line on midpoints
        #canvas.create_line(midpoints,fill='red')

    def move(self,dx=0,dy=0):
        if (dx,dy)==(0,0):
            (dx,dy) = (self.velocity_x,self.velocity_y) 
        if self.drop: self.x+=10
        self.x+=dx 
        self.y+=dy
        self.square1.move(dx,dy)
        self.square2.move(dx*.75,dy*.75) 
        # this needs to be consistent with the resizing of square2
        # to keep vanishing point static


    def containsPlayer(self,data):
        player= data.player
        (corners1,corners2,x,y,width,height,
        upper,lower,left,right,midpoints)=self.initVariableNames()
        if (lower>player.y>upper and left<player.x<right): return True
        return False


    def isNearPlayer(self,data):
        player= data.player
        maxDist = data.cubesize
        if (abs(self.x-player.x)<maxDist and abs(self.y-player.y)<maxDist):
            return True
        return False


class Square(object):
    def __init__(self,x,y,size):
        self.x=x
        self.y=y
        self.width=size
        self.height=size
        self.bounds=getBounds(self)
        self.border=white
        self.corners=self.getCorners()

    # draws dotted outline of the square
    def draw(self,canvas,color):
        corners=self.corners
        for i in range(4):
            canvas.create_line(corners[-1+i],corners[i],dash=(1,5),fill=color)
        
    def move(self,dx,dy):

        self.x+=dx
        self.y+=dy
        self.corners=self.getCorners()

    def getCorners(square):
        x=square.x
        y=square.y
        w=square.width
        h=square.height
        NW=(x-w/2,y-h/2)
        NE=(x+w/2,y-h/2)
        SE=(x+w/2,y+h/2)
        SW=(x-w/2,y+h/2)
        return(NW,NE,SE,SW)


class Shadow(object):
    def __init__(self,data):
        player = data.player
        (self.x1,self.y1,
         self.x2,self.y2)=data.player.bounds
        if data.bg_color==white: self.color="grey10"
        else:                    self.color="grey30"
        self.size=1
        #self.velocity=

        def draw(self,canvas,data):
            points=(x1,y1,x2,y2)=data.player.bounds
            for point in points:
                point*=size

            if player.isOnSolidCube(data):
                canvas.create_oval(x1,y2-5,x2,y2+5,fill=shadowcolor,width=0)
        def move(): pass


# returns NW and SE corner, or L/U/R/D sides
def getBounds(element):
    width = element.width
    height = element.height
    (x1,x2)=(element.x-width/2,element.x+width/2)
    (y1,y2)=(element.y-height/2,element.y+height/2)
    return(x1,y1,x2,y2)


def getMidpoint(p1,p2):
    (x1,y1)=(p1[0],p1[1])
    (x2,y2)=(p2[0],p2[1])
    return ((x1+x2)/2,(y1+y2)/2)

def sortCubes(data):
    for cube in data.cubes:
        cube.distFromCenter(data)
    data.cubes=sorted(data.cubes)


def updateCubesInView(data,cubes):
    data.cubesInView=[]
    data.cubesNearPlayer=[]
    for cube in cubes:
        if cube.isInView(data): 
            data.cubesInView+=[cube]
        if cube.isNearPlayer(data):
            data.cubesNearPlayer+=[cube]



# returns a randomly generated list representing a 2D plane of cubes
def makeRandom2DWorld(data):
    L=[]
    rows = 8
    cols = 15

    for row in range(rows):
        L+=[[]]
        for col in range(cols): 
            num=random.choice(range(3))
            if data.difficulty=='EASY':
                num=random.choice(range(4))
            if num!=0: 
                num=random.choice((0,1))
                if num==0: L[row]+=[black] 
                else: L[row]+=[white]      
            else: L[row]+=[0]  # empty cube

    return (L)

def makeCubeData(data,L):
    cubes=[]
    size=data.cubesize
    (rows,cols)=(len(L),len(L[0]))
    for row in range(rows-1,-1,-1): 
        y = size*row
        for col in range(cols): 
            x = size*col
            color =L[row][col]

            if color!=0: #non-empty
                cubes+=[Cube(x,y,data,color)]
    return cubes
                
def resetLevel(data,difficulty):
    player = data.player
    init(data,'playGame',difficulty)
    updateCubesInView(data,data.cubes)
    if not player.isOnSolidCube(data) or player.isInCube(data):
            resetLevel(data,difficulty)


def invertWorld(data):
    if data.bg_color==white: data.bg_color=black
    elif data.bg_color==black: data.bg_color=white
    if data.mode=='playGame':
        for cube in data.cubesNearPlayer: 
            if cube.containsPlayer(data): 
                cube.color=None
                break
    for cube in data.cubes:
        cube.defineSolid(data)
    for cube in data.helpCubes:
        cube.defineSolid(data)


def drawAllCubes(canvas,data):
    for cube in data.cubesInView: 
        cube.draw(canvas,data)

        #drawing shadows for cubes
        for other in data.cubesInView: 
            if (cube.isSolid and other.isSolid and   # both cubes are solid
                cube.x == other.x and                # same column
                data.cubesize*4>cube.y-other.y>0 and # is above, not too high
                cube.y-data.cubesize/2 >= data.cy):  # top face is visible 
                cube.castShadow(canvas,data)

def moveAllCubes(data):
    if (not data.player.isOnSolidCube(data) and 
        not data.cubes[0].velocity_y<-data.maxVelocity):
        for cube in data.cubes:
                cube.velocity_y-=data.gravity 

    for cube in data.cubes:
        cube.velocity_x*=.9
        cube.move()

def countTimeOnCube(data):
    player=data.player
    #data.timeOnCube=0
    data.timeOnCube+=1
    width=data.cubesize
    for cube in data.cubesNearPlayer:

        if not data.player.isOnSolidCube(data):
            data.timeOnCube=0
            break
        if (data.difficulty=='HARD' and cube.isSolid and
            cube.x-width/2<player.x<cube.x+width/2 and
            player.y<cube.y and data.timeOnCube>15 ): 
            cube.drop= True
            break

    
def drawButtons(canvas,buttons,data):
    for button in buttons: button.draw(data,canvas)

# for determining buttons that have been clicked
def isInBounds(position,bounds):
    (x,y)=(position[0],position[1])
    (x1,y1,x2,y2)=bounds
    return (x1<x<x2 and y1<y<y2)


def countScore(data):
    data.score=0
    for cube in data.cubes:
        if cube.color==None: data.score+=1


def drawStats(canvas,data):
        if data.bg_color==white: color= black
        else: color = white
        minutes = data.seconds//60
        seconds = str(data.seconds%60)
        if len(seconds)!=2:
            seconds = ("0"+seconds)
        canvas.create_text(10,10,anchor=NW,
            text="%s MODE"%(data.difficulty),
            font="Arial 25",fill=color)
        canvas.create_text(10, 40, anchor=NW,
            text="Timer: %s:%s"%(minutes,seconds), 
            font="Arial 18", fill=color )
        canvas.create_text(10,60,anchor=NW,
            text="Score: %d"%(data.score),
            font="Arial 18",fill=color)


        


####################################
# mode dispatcher
####################################

def mousePressed(event, data):
    if (data.mode == "splashScreen"): splashScreenMousePressed(event, data)
    elif (data.mode == "playGame"):   playGameMousePressed(event, data)
    elif (data.mode == "help"):       helpMousePressed(event, data)
    elif (data.mode == "gameOver"):   gameOverMousePressed(event,data)
    elif (data.mode == "tutorial"):   tutorialMousePressed(event,data)
def keyPressed(event, data,canvas):
    if (data.mode == "splashScreen"): splashScreenKeyPressed(event, data)
    elif (data.mode == "playGame"):   playGameKeyPressed(event, data)
    elif (data.mode == "help"):       helpKeyPressed(event, data)
    elif (data.mode == "gameOver"):   gameOverKeyPressed(event,data)
    elif (data.mode == "tutorial"):   tutorialKeyPressed(event,data)
def timerFired(data):
    if (data.mode == "splashScreen"): splashScreenTimerFired(data)
    elif (data.mode == "playGame"):   playGameTimerFired(data)
    elif (data.mode == "help"):       helpTimerFired(data)
    elif (data.mode == "gameOver"):   gameOverTimerFired(data)
    elif (data.mode == "tutorial"):   tutorialTimerFired(data)
def redrawAll(canvas, data,scores):
    if (data.mode == "splashScreen"): splashScreenRedrawAll(canvas, data)
    elif (data.mode == "playGame"):   playGameRedrawAll(canvas, data,scores)
    elif (data.mode == "help"):       helpRedrawAll(canvas, data)
    elif (data.mode == "gameOver"):   gameOverRedrawAll(canvas,data,scores)
    elif (data.mode == "tutorial"):   tutorialRedrawAll(canvas,data)

####################################
# splashScreen mode
####################################

def splashScreenMousePressed(event, data):
    position=(event.x,event.y)
    data.previousMode='splashScreen'

    for button in data.splashButtons:
        if isInBounds(position,getBounds(button)):
            data.difficulty=button.difficulty
            resetLevel(data,button.difficulty)
            if button.mode=='tutorial': 
                data.tutorialmode=1
                data.zcount=0
            data.mode=button.mode



def splashScreenKeyPressed(event, data):

    dist = 10
    player=data.player
   
    if (event.keysym=='z'):
        invertWorld(data)
        for cube in data.cubes:
            cube.defineSolid(data)

    if (event.keysym=='Right'):
        player.velocity_x+=dist
    if (event.keysym=='Left'):
        player.velocity_x-=dist
    if (((event.keysym=='space') or event.keysym=="Up")
        and data.player.velocity_y==0) : #cannot endlessly jump
        data.player.y-=10
        player.velocity_y-=dist*1.5

    if (event.keysym=='t'):
        init(data)
        data.mode='tutorial'
    if (event.keysym=='h'):
        resetLevel(data,'EASY')
        data.mode='help'
    if (event.keysym=='e'):
        resetLevel(data,'EASY')
        data.mode='playGame'
    if (event.keysym=='d'):
        resetLevel(data,'HARD')
        data.mode='playGame'

def splashScreenTimerFired(data):
    player = data.player
    player.velocity_x*=.9
    if player.velocity_y<data.maxVelocity/2:
        player.velocity_y+=data.gravity/2

    # stop x motion when approaching cube from the side
    if ((player.isMovingRight(data) and player.hitCubeLeft(data)) or
        (player.isMovingLeft(data)  and player.hitCubeRight(data))):
       player.velocity_x=0

    if (player.isFalling(data) and player.isOnSolidCube(data)):
        player.velocity_y=0

    player.move()

    pass

def splashScreenRedrawAll(canvas, data):
    if   data.bg_color==black: color = white
    elif data.bg_color==white: color = black


    canvas.create_rectangle(0,0,data.width,data.height,fill=data.bg_color)
    canvas.create_text(data.width/2, data.height*.15,fill=color,
                       text="ILLUSION-Z", font="Impact 169 bold")

    updateCubesInView(data,data.cubes)
    drawAllCubes(canvas,data)

    for button in data.splashButtons:
        button.draw(canvas)
    data.player.draw(canvas,data)
    


####################################
# help mode
####################################

def helpMousePressed(event, data):
    position=(event.x,event.y)
    for button in data.helpButtons:
        if isInBounds(position,getBounds(button)):
            if button.mode =='tutorial':
                data.tutorialmode=1
                data.mode='tutorial' 
            elif data.previousMode=='': 
                init(data)
                data.mode= 'splashScreen'
            else:
                data.player=Player(data) #re-init player position 
                data.mode = data.previousMode

def helpKeyPressed(event, data):

    dist = 10
    player=data.player

    if (event.keysym == 'b'): 
        data.player=Player(data)
        if data.previousMode=='': 
            init(data)
            data.mode= 'splashScreen'
        else: data.mode = data.previousMode  
    if (event.keysym=='z'):
        invertWorld(data)
        for cube in data.helpCubes:
            cube.defineSolid(data)
    if (event.keysym=='t'):
        data.mode='tutorial'


    if (event.keysym=='Right'):
        player.velocity_x+=dist
    if (event.keysym=='Left'):
        player.velocity_x-=dist
    if (((event.keysym=='space') or event.keysym=="Up")
        and data.player.velocity_y==0) : #cannot endlessly jump
        data.player.y-=10
        player.velocity_y-=dist*1.6



def helpTimerFired(data):
    player = data.player
    player.velocity_x*=.9
    if player.velocity_y<data.maxVelocity/2:
        player.velocity_y+=data.gravity/2

    # stop x motion when approaching cube from the side
    if ((player.isMovingRight(data) and player.hitCubeLeft(data)) or
        (player.isMovingLeft(data)  and player.hitCubeRight(data))):
       player.velocity_x=0

    if (player.y>data.height*.85 or 
        player.isFalling(data) and player.isOnSolidCube(data)):
        player.velocity_y=0

    player.move()

def helpRedrawAll(canvas, data):
    
    textList = ['Use arrow keys to move.','Press < SPACE > or < UP > to jump.',
    'Press < Z > to invert the world.','Press < H > to access this screen.' ]

    if   data.bg_color==black: color = white
    elif data.bg_color==white: color = black
    canvas.create_rectangle(0,0,data.width,data.height,fill=data.bg_color)
    canvas.create_text(data.width/2, data.height*.1,fill=color,
                       text="HOW TO PLAY", font="Impact 140 bold")

    for i in range(len(textList)):
        text = textList[i]
        canvas.create_text(data.width/2,data.height*.25+data.cubesize*i/2,
            fill=color, text=text,font= "Impact 30 ")

    updateCubesInView(data,data.helpCubes)
    drawAllCubes(canvas,data)

    for button in data.helpButtons:
        button.draw(canvas)

    data.player.draw(canvas,data)
    
    

####################################
# playGame mode
####################################

def playGameMousePressed(event, data):
    pass

def playGameKeyPressed(event, data):
    data.start=True
    dist = 10

    if (event.keysym == 'h'):
        #if data.bg_color==white: invertWorld(data) 
        data.previousMode='playGame'
        data.player=Player(data)
        data.mode = "help"
    if (event.keysym =='z'): invertWorld(data)
   
        

    if (event.keysym =='Right'):
        for cube in data.cubes: cube.velocity_x-=dist

    if (event.keysym=='Left'):
        for cube in data.cubes: cube.velocity_x+=dist

    if (event.keysym=="Down"):
        if not abs(data.cubes[0].velocity_y)>data.maxVelocity:
            for cube in data.cubes: cube.velocity_y-=dist
        
    if (((event.keysym=='space') or event.keysym=="Up")
        and data.cubes[0].velocity_y==0) : #cannot endlessly jump
        for cube in data.cubes: cube.velocity_y+=dist*2 



def playGameTimerFired(data):
    if data.start:
        data.timer+=1
        if data.timer%50==0: data.seconds-=1

        # stop x motion when approaching cube from the side
        if ((data.player.isMovingRight(data) and 
             data.player.hitCubeLeft(data)) or
            (data.player.isMovingLeft(data)  and 
             data.player.hitCubeRight(data))):
            for cube in data.cubes: cube.velocity_x=0

        # stops player from falling 
        if (data.player.isFalling(data) and 
            data.player.isOnSolidCube(data)):
            for cube in data.cubes: cube.velocity_y=0

        for cube in data.cubes:
            if cube.drop and cube.velocity_y<data.maxVelocity: cube.move(0,25)
            
        countScore(data)
        countTimeOnCube(data)
        moveAllCubes(data)


def playGameRedrawAll(canvas, data,scores):
    canvas.create_rectangle(0,0,data.width,data.height,fill=data.bg_color)
    
    sortCubes(data)
    updateCubesInView(data,data.cubes)
    if len(data.cubesInView) <1 or data.seconds==0: 
        scores+=[data.score]
        data.mode='gameOver'

    
    drawAllCubes(canvas,data)
    data.player.draw(canvas,data)
    drawStats(canvas,data)




####################################
# game over mode
####################################

def gameOverMousePressed(event, data):
    position=(event.x,event.y)
    difficulty=data.difficulty
    for button in data.gameOverButtons:
        if isInBounds(position,getBounds(button)):
            if button.mode=='playGame': 
                resetLevel(data,difficulty)
                data.mode='playGame'
            else:#a) #re-init player position 
                init(data)
                data.mode = 'splashScreen'

def gameOverKeyPressed(event, data):

    dist = 10
    player=data.player

    if (event.keysym == 'b'): 
        data.player=Player(data)
        init(data)
        data.mode= 'splashScreen'
    
    if (event.keysym == 't'):
        resetLevel(data,data.difficulty)
        data.mode='playGame'


   
    if (event.keysym=='z'):
        invertWorld(data)
        for cube in data.helpCubes:
            cube.defineSolid(data)


    if (event.keysym=='Right'):
        player.velocity_x+=dist
    if (event.keysym=='Left'):
        player.velocity_x-=dist
    if (((event.keysym=='space') or event.keysym=="Up")
        and data.player.velocity_y==0) : #cannot endlessly jump
        data.player.y-=10
        player.velocity_y-=dist*1.6




def gameOverTimerFired(data):
    player = data.player
    player.velocity_x*=.9
    if player.velocity_y<data.maxVelocity/2:
        player.velocity_y+=data.gravity/2

    # stop x motion when approaching cube from the side
    if ((player.isMovingRight(data) and player.hitCubeLeft(data)) or
        (player.isMovingLeft(data)  and player.hitCubeRight(data))):
       player.velocity_x=0

    if (player.y>data.height*.85 or 
        player.isFalling(data) and player.isOnSolidCube(data)):
        player.velocity_y=0

    player.move()

def gameOverRedrawAll(canvas, data,scores):

    hiscore=max(scores)
    if data.score>hiscore: hiscore=data.score

    minutes = data.seconds//60
    seconds = str(data.seconds%60)

    if len(seconds)!=2:
            seconds = ("0"+seconds)

    textList = ['Time Remaining: %s:%s'%(minutes,seconds),
                'Cubes obtained: %s'%(data.score),
                'Hi-Score: %s'%(hiscore)]

    if   data.bg_color==black: color = white
    elif data.bg_color==white: color = black
    canvas.create_rectangle(0,0,data.width,data.height,fill=data.bg_color)
    canvas.create_text(data.width/2, data.height*.1,fill=color,
                       text="GAME OVER", font="Impact 140 bold")


    for i in range(len(textList)):
        text = textList[i]
        canvas.create_text(data.width/2,data.height*.25+data.cubesize*i/2,
            fill=color, text=text,font= "Impact 30 ")

    updateCubesInView(data,data.helpCubes)
    drawAllCubes(canvas,data)

    for button in data.gameOverButtons:
        button.draw(canvas)


    data.player.draw(canvas,data)


####################################
# tutorial mode
####################################

def tutorialMousePressed(event, data):

    position=(event.x,event.y)
    for button in data.tutorialButtons:
        if isInBounds(position,getBounds(button)):
            if button.mode=='splashScreen':
                init(data)
                data.mode='splashScreen'

            if data.previousMode=='': 
                init(data)
                data.mode= 'splashScreen'
            else:
                data.player=Player(data) #re-init player position 
                data.mode = data.previousMode
def tutorialKeyPressed(event, data):

    dist = 10
    player=data.player


    if (event.keysym == 'b'): 
        data.player=Player(data)
        if data.previousMode=='': 
            init(data)
            data.mode= 'splashScreen'
        else: data.mode = data.previousMode
   
    if (event.keysym=='m'):
        init(data)
        data.mode='splashScreen'

    if (event.keysym=='z'):
        data.zcount+=1

        if data.tutorialmode==4:
            for cube in data.tutorial4: 
                if cube.containsPlayer(data): 
                    cube.color=None
                    break


        invertWorld(data)
        for cube in data.cubesInView:
            cube.defineSolid(data)
        if data.zcount==2: 
            data.tutorialmode=2
        if data.zcount==3:
            data.tutorialmode=3



    if (event.keysym=='Right'):
        player.velocity_x+=dist
    if (event.keysym=='Left'):
        player.velocity_x-=dist
    if (((event.keysym=='space') or event.keysym=="Up")
        and data.player.velocity_y==0) : #cannot endlessly jump
        data.player.y-=10
        player.velocity_y-=dist*1.6




def tutorialTimerFired(data):
    player = data.player
    player.velocity_x*=.9
    if player.velocity_y<data.maxVelocity/2:
        player.velocity_y+=data.gravity/2

    # stop x motion when approaching cube from the side
    #if data.tutorialmode<4:
    if ((player.isMovingRight(data) and player.hitCubeLeft(data)) or
        (player.isMovingLeft(data)  and player.hitCubeRight(data))):
       player.velocity_x=0

    if (player.y>data.height*.85 or 
        player.isFalling(data) and player.isOnSolidCube(data)):
        player.velocity_y=0

    if data.tutorialmode==5:
        if player.isOnSolidCube(data): data.timeOnCube+=1
        for cube in data.tutorial1:
            if cube.drop: 
                cube.velocity_y+=data.gravity
                cube.move()

    player.move()






def tutorialRedrawAll(canvas, data):
    if   data.bg_color==black: color = white
    elif data.bg_color==white: color = black
    canvas.create_rectangle(0,0,data.width,data.height,fill=data.bg_color)
    canvas.create_text(data.width/2, data.height*.1,fill=color,
                       text="TUTORIAL", font="Impact 140 bold")


    
    # sequence of tutorial screens 
    # only proceed after player completes a specific action
    if data.tutorialmode==1:
        cubes = data.tutorial1
        textList = data.text1

    elif data.tutorialmode==2:
        cubes=data.tutorial1
        textList=data.text2

    elif data.tutorialmode==3:
        cubes=data.tutorial1
        textList=data.text3
        if (data.bg_color==white and 
            data.player.isOnSolidCube(data)):
            data.tutorialmode=4

    elif data.tutorialmode==4:
        cubes=data.tutorial4
        textList=data.text4
        empty = 0
        for cube in data.tutorial4: 
            cube.move()
            if cube.color==None: empty+=1
        if empty>=2: textList=data.text4a
        if empty==4: data.tutorialmode=5


    elif data.tutorialmode==5:
        player=data.player

        width=data.cubesize
        cubes=data.tutorial1
        textList=data.text5
        cubesOffScreen=0
        for cube in cubes:
            if (cube.isSolid  and
            cube.x-width/2<player.x<cube.x+width/2 and
            player.y<cube.y and data.timeOnCube>20 ): 
                cube.drop= True
                data.timeOnCube=0
            if cube.y>data.height*2: cubesOffScreen+=1
        if cubesOffScreen==2: data.tutorialmode=6

    elif data.tutorialmode==6: 
        cubes=data.tutorial1
        textList=data.text6




    for i in range(len(textList)):
        text = textList[i]
        canvas.create_text(data.width/2,data.height*.3+data.cubesize*i/5,
            fill=color, text=text)

    updateCubesInView(data,cubes)
    for cube in data.cubesInView:
        cube.defineSolid(data)
    drawAllCubes(canvas,data)



    for button in data.tutorialButtons:
        button.draw(canvas)

    data.player.draw(canvas,data)
    
    
    
    


####################################
# use the run function as-is
####################################

def run(width=700, height=700):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data,scores)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data, canvas)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed

run()   