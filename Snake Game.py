from turtle import Turtle, Screen
import random
import time
KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_SPACE = 'Up', 'Down', 'Left', 'Right', 'space'
# Global variable
g_snake = None
g_monster = None
g_food = None
g_screen = None
g_words = None
g_lstTail = []
g_lstFood = []
g_lstNumber = []
mDirection = None      # the direction of monster
sDirection =  None     # the direction of snake
init_sDirection = None # the initial direction of snake
# Global constant
Start = 0              # start time
Time = 0               # the number of time
Now = 0                # the time of now
Contacted = 0          # the number of contacted
sSpeed = 500           # the speed of snake
mSpeed = 475           # the speed of monster
def countTime():
    global Time, Start, Now, mDirection
    Now = time.time()
    Time = round(Now-Start)
    g_screen.ontimer(countTime,1000) 
def countContacted():
    global Contacted
    for i in g_lstTail:
        if g_monster.distance(i) < 20:
            Contacted += 1
def configureScreen(w=500,h=500):
    global Time,Contacted
    s = Screen()
    s.setup(w,h)
    s.title('Snake: '+'Contacted: '+str(Contacted)+', Time: '+str(Time))
    s.tracer(0)
    return s
def configureSnake(shape='square',color='red',x=0,y=0):
    t = Turtle(shape)
    t.penup()
    t.color(color)
    t.goto(x,y)
    return t
def configureMonster():
    while True:
        x=random.randint(-220,220)
        y=random.randint(-220,220)
        if g_snake.distance((x,y)) > 300:
            break
        else:
            continue
    m = configureSnake(shape='square',color='purple',x=x,y=y)
    return m
def configureWords(color='black',x=-220,y=220):
    w = Turtle()
    w.penup()
    w.color(color)
    w.goto(x,y)
    w.hideturtle()
    w.write('Welcome to my version of snake!',align='left',font=('aerial',10,'normal'))
    w.goto(x,y-40)
    w.write('You are going to use the 4 arrow keys to move the snake',align='left',font=('aerial',10,'normal'))
    w.goto(x,y-60)
    w.write('around the screen, trying to consume all the food items',align='left',font=('aerial',10,'normal'))
    w.goto(x,y-80)
    w.write('before the monster catches you',align='left',font=('aerial',10,'normal'))
    w.goto(x,y-120)
    w.write('Click anywhere on the screen to start the game, have fun!!',align='left',font=('aerial',10,'normal'))
    return w
def configureFood(color='black'):
    global g_lstFood, g_lstNumber
    i = 0
    lstx = random.sample(range(-200,200,20),9)
    lsty = random.sample(range(-200,200,20),9)
    lstx.append(0)
    lsty.append(0)
    g_lstNumber = [1,2,3,4,5,6,7,8,9,5]
    while i < 10:
        newFood = Turtle()
        newFood.penup()
        newFood.color(color)
        newFood.hideturtle()
        x = lstx[i]
        y = lsty[i]
        g_lstFood.append(newFood)
        newFood.goto(x,y)
        newFood.write(g_lstNumber[i],align='center',font=('Courier',10,'normal'))
        i += 1
    return newFood
# change the direction of snake
def moveUp():
    global sDirection
    sDirection = 'up'
def moveDown():
    global sDirection
    sDirection = 'down'
def moveLeft():
    global sDirection
    sDirection = 'left'
def moveRight():
    global sDirection
    sDirection = 'right'
def moveMonster(d=20):
    gameOver()
    global mDirection, sSpeed, mSpeed
    mSpeed = random.randint(sSpeed-25,sSpeed+25)
    y = g_snake.ycor()-g_monster.ycor()
    x = g_snake.xcor()-g_monster.xcor()
    if mDirection != 'stop':
        if x >= y > 0 or x > -y > 0:
            mDirection = 'right'
        elif -x >= y > 0 or x <= y < 0:
            mDirection = 'left'
        elif 0 < -x < y or y > x > 0:
            mDirection = 'up'
        elif y < x < 0 or -y >= x > 0:
            mDirection = 'down'  
        if mDirection == 'up':
            g_monster.setheading(90)
            g_monster.forward(d)
        elif mDirection == 'down':
            g_monster.setheading(270)
            g_monster.forward(d)
        elif mDirection == 'left':
            g_monster.setheading(180)
            g_monster.forward(d)
        elif mDirection == 'right':
            g_monster.setheading(0)
            g_monster.forward(d)
    g_screen.update()
    g_screen.ontimer(moveMonster,mSpeed)
def moveSnake(d=20):
    gameOver()               # check the status of the game
    if sDirection == 'up':
        g_snake.setheading(90)
        g_snake.forward(d)
    elif sDirection == 'down':
        g_snake.setheading(270)
        g_snake.forward(d)
    elif sDirection == 'left':
        g_snake.setheading(180)
        g_snake.forward(d)
    elif sDirection == 'right':
        g_snake.setheading(0)
        g_snake.forward(d)
    if mDirection != 'stop':
        countTime()
        countContacted()
        g_screen.title('Snake: '+'Contacted: '+str(Contacted)+', Time: '+str(Time))           # refresh the title
    win()
    g_screen.update()
def gameOver(color='red'):
    global sDirection, mDirection
    g = Turtle()
    g.penup()
    g.color(color)
    g.hideturtle()
    y = abs(g_snake.ycor()-g_monster.ycor())
    x = abs(g_snake.xcor()-g_monster.xcor())
    if x < 20 and y < 20:
        sDirection = 'stop'
        mDirection = 'stop'
        g.goto(g_snake.xcor(),g_snake.ycor())
        g.write('Game Over !! ', align='right', font=('aerial',16,'bold'))
    return g
def stopSnake():
    global sDirection, init_sDirection
    if sDirection != 'stop':
        init_sDirection = sDirection
        sDirection = 'stop'
    else:
        sDirection = init_sDirection
def win(color='red'):
    global sDirection, mDirection
    w = Turtle()
    w.penup()
    w.color(color)
    w.hideturtle()
    if len(g_lstTail) == 50:
        sDirection = 'stop'
        mDirection = 'stop'
        w.goto(g_snake.xcor(),g_snake.ycor())
        w.write('You Win !!! ',align='right',font=('aerial',16,'bold'))
    return w
# keyboard bindings
def configureKey(s):
    s.listen()
    s.onkey(moveUp,KEY_UP)
    s.onkey(moveDown,KEY_DOWN)
    s.onkey(moveRight,KEY_RIGHT)
    s.onkey(moveLeft,KEY_LEFT)
    s.onkey(stopSnake,KEY_SPACE)
# move the tail
def stampItems():
    global g_lstFood, g_lstTail, sDirection, sSpeed
    for i in range(1,11):
        if g_snake.distance(g_lstFood[i-1]) < 20:
            g_lstFood[i-1].goto(500,500)
            g_lstFood[i-1].clear()
            sSpeed += 25
            for j in range(g_lstNumber[i-1]):
                newTail = Turtle()
                newTail.shape('square')
                newTail.color('blue','black')
                newTail.speed(0)
                newTail.penup()
                newTail.setx(g_snake.xcor())
                newTail.sety(g_snake.ycor())
                g_lstTail.append(newTail)
    for k in range(len(g_lstTail)-1,0,-1):
        x = g_lstTail[k-1].xcor()
        y = g_lstTail[k-1].ycor()
        if sDirection != 'stop':
            g_lstTail[k].goto(x,y)
    if sDirection != 'stop':
        if len(g_lstTail) > 1:
            g_lstTail[0].goto(g_snake.xcor(),g_snake.ycor())
    moveSnake()
    checkBound()
    g_screen.ontimer(stampItems,sSpeed)
    return g_lstTail
def checkBound():
    global sDirection
    if g_snake.xcor() >= 240:
        sDirection = 'stop'
        g_snake.goto(239,g_snake.ycor())
    elif g_snake.xcor() <= -240:
        sDirection = 'stop'
        g_snake.goto(-239,g_snake.ycor())
    elif g_snake.ycor() >= 240:
        sDirection = 'stop'
        g_snake.goto(g_snake.xcor(),239)
    elif g_snake.ycor() <= -240:
        sDirection = 'stop'
        g_snake.goto(g_snake.xcor(),-239)
def onClick(x,y):
    global Start
    g_words.clear()
    g_food = configureFood()
    Start = time.time()
    stampItems()
    moveMonster()
if __name__ == '__main__':
    g_screen = configureScreen()
    g_snake = configureSnake()
    g_monster = configureMonster()
    g_screen.update()
    g_words = configureWords()
    g_screen.onclick(onClick)
    configureKey(g_screen)
    g_screen.listen()
    g_screen.mainloop()
