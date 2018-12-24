import random
import numpy
import math
import Robot
import matplotlib.pylab as plt
import xlwt
from xlwt import Workbook

#----------------------------------------------- variables -----------------------------------------------------------------------

global current_x, current_y
global x_cell, y_cell
global last_x, last_y
global robot_pos
global miu
global Va_real, Vd_real
global Va_state, Vd_state
global i
action = [0,1,2,3,4,5]
global dt
global missReward
global goalReward
global normalReward
global endFlag
global Vx, Vy

#------------------------------------------------ defim ------------------------------------------------------------------

def convert_angle(angle):
    if(angle <45 and angle >=0):
        return 0
    if (angle < 90 and angle >= 45):
        return 1
    if (angle < 135 and angle >= 90):
        return 2
    if (angle < 180 and angle >= 135):
        return 3
    if (angle < 225 and angle >= 180):
        return 4
    if (angle < 270 and angle >= 225):
        return 5
    if (angle < 315 and angle >= 270):
        return 6
    if (angle < 360 and angle >= 315):
        return 7

def convert_y(y):
    if(y <10 and y >=0):
        return 0
    if (y < 20 and y >= 10):
        return 1
    if (y < 30 and y >= 20):
        return 2
    if (y < 40 and y >= 30):
        return 3
    if (y < 50 and y >= 40):
        return 4
    if (y < 60 and y >= 50):
        return 5
    if (y < 70 and y >= 60):
        return 6
    if (y < 80 and y >= 70):
        return 7
    if (y < 90 and y >= 80):
        return 7

def convert_x(x):
    if(x <24.5 and x >=0):
        return 0
    if (x < 49 and x >= 24.5):
        return 1
    if (x < 73.5 and x >= 49):
        return 2
    if (x < 98 and x >= 73.5):
        return 3
    if (x < 122.5 and x >= 98):
        return 4
    if (x <= 147 and x >= 122.5):
        return 5

def convert_amplitude(amplitude):
    if(amplitude <20 and amplitude >=0):
        return 0
    if (amplitude < 40 and amplitude >= 20):
        return 1
    if (amplitude < 60 and amplitude >= 40):
        return 2
    if (amplitude >= 60):
        return 3

def update_variables(a):    ## after each movement, update variables amplitude, velocity, dx, dy
    global Vx, Vy,current_x,current_y,Vd_real,Va_real,Va_state,Vd_state,x_cell,y_cell,dt
    if a!=2:
        dt=1
    else:
        dt=0.04
    Vx = Va_real*math.cos(math.radians(Vd_real))
    Vy = -(Va_real*math.sin(math.radians(Vd_real)))     #Velocity Y is minus
    current_x = dt*Vx + current_x                  #update real X
    current_y = dt*Vy + current_y                 #update real Y
    noise=numpy.random.normal(0,0.5)
    Vd_real = Vd_real+noise
    if (current_y> 90):   ## mikre katze
        global current_y
        current_y= 180-current_y
        global Vd_real
        Vd_real = 360 - Vd_real
    if (current_y < 0):  ## mikre katze
        global current_y
        current_y = 0 - current_y
        global Vd_real
        Vd_real = 360 - Vd_real
    Va_real = Va_real*(1-miu)
    Va_state = convert_amplitude(Va_real)
    Vd_state = convert_angle(Vd_real)
    x_cell = convert_x(current_x)
    y_cell = convert_y(current_y)

def init_learning():
    global messi
    messi = Robot.Robot()

def init_epizode():
    global endFlag,Va_real,Vd_real,Va_state,Vd_state,current_x,current_y,x_cell,y_cell,robot_pos,dt,Vx,miu
    endFlag = 1
    Va_real = random.randint(1, 70)
    Vd_real = random.randint(90, 270)
    Va_state = convert_amplitude(Va_real)
    Vd_state = convert_angle(Vd_real)
    current_x = random.uniform(49, 147)
    current_y = random.uniform(0, 90)
    x_cell = convert_x(current_x)
    y_cell = convert_y(current_y)
    robot_pos = 1
    miu=0.01
    dt = 0.04
    Vx=Va_real * math.cos(math.radians(Vd_real))

#------------------------------------------------ main loop ------------------------------------------------------------------

init_learning()
lastRatio=0
lastScore = 0
scores = []
random.seed(365)
for i in range (100000):
    init_epizode()
    while endFlag :
        global messi,current_x,Vx,endFlag
        field_state = (x_cell,y_cell,Va_state,Vd_state)
        messi.update(field_state,current_x,Vx)
        update_variables(messi.lastAction)
        if current_x<0 or Va_real<=0.5 or messi.hit!=0 or Vd_real<90 or Vd_real>270:    # check end of episode
            endFlag = 0
    if (i%1000)==0:
         scores.append(messi.score-lastScore)              # insert hit amount for last 1000 iteration
         lastScore=messi.score

#------------------------------------------------ insert matrix action to excell----------------------------------------------

# Workbook is created
wb = Workbook()
# add_sheet is used to create sheet.
sheet1 = wb.add_sheet('Sheet 1')
for i in range (6):
    for j in range(9):
        for k in range(4):
            for l in range(8):
                for m in range(3):
                    for n in range (6):
                        line = i*864 + j*96 + k*24 + l*3 + m
                        output = messi.ai.q.get(((i, j, k, l, m), n),None)
                        if output is None:
                            messi.ai.q[(i, j, k, l, m), n]=0
                            sheet1.write(line, n, 0)
                        else:
                            ins = messi.ai.q [((i,j,k,l,m),n)]
                            sheet1.write(line, n, ins)

wb.save('hello-100000.xls')

#------------------------------------------------ print plot ------------------------------------------------------------------

print(scores)
array=range(len(scores))
plt.plot(array,scores,color='magenta')
plt.xlabel('i*1000')
plt.ylabel('num of hit for 1000')
plt.show()
