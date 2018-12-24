import sarsa

#----------------------------------------------- variables -----------------------------------------------------------------------
action = [0,1,2,3,4,5]

#----------------------------------------------- class Robot -----------------------------------------------------------------------
class Robot():
    def __init__(self):
        self.ai = sarsa.Sarsa(actions=range(0,6), epsilon=0.1, alpha=0.1, gamma=0.9)
        self.lastAction = None
        self.lastPosition = 1
        self.pos = 1
        self.score = 0
        self.misses = 0
        self.normalReward = 0
        self.missReward = -10
        self.goalReward = 100
        self.hit = 0

    def calcul_expct(self,x, vx):
        if(self.lastAction!=2 ):
            next_x = vx+x
        else:
            next_x = 0.04*vx + x
        if next_x<=0.25:
            return 1
        else:
            return 0

    def goAction(self,action_d):
        if  action_d ==0:               # move up
            if self.pos < 2:
                self.lastPosition = self.pos
                self.pos = self.pos + 1
        elif action_d == 1:             # move down
            if self.pos > 0:
                self.lastPosition = self.pos
                self.pos = self.pos - 1

    def hit_or_miss(self, x_ball, y_ball,x,vx):
        ans = 0
        if self.lastAction == 5:
            if x_ball == 0 and y_ball == 0:
                if self.pos == 0:
                    ans = 1                                    ############## lachshov al miss
            elif self.pos == 1:
                if x_ball == 0 and y_ball == 3:
                    ans = 1
            elif self.pos == 2:
                if x_ball == 0 and y_ball == 6:
                    ans = 1
        elif self.lastAction == 4:
            if self.pos == 0:
                if x_ball==0 and y_ball==1:
                    ans = 1                                    ############## lachshov al miss
            elif self.pos == 1:
                if x_ball == 0 and y_ball == 4:
                    ans = 1
            elif self.pos == 2:
                if x_ball == 0 and y_ball == 7:
                    ans = 1
        elif self.lastAction == 3:
            if self.pos == 0:
                if x_ball==0 and y_ball==2:
                    ans = 1                                    ############## lachshov al miss
            elif self.pos == 1:
                if x_ball == 0 and y_ball == 5:
                    ans = 1
            elif self.pos == 2:
                if x_ball == 0 and y_ball == 8:
                    ans = 1
        if ans!=1:
            if self.calcul_expct(x, vx) :                   # ball pass the line
                    ans = -1
            else:
                    ans = 0
        return ans


    def calcReward(self, x_ball, y_ball,x,vx):
        self.hit = self.hit_or_miss(x_ball, y_ball,x,vx)
        if self.hit == -1:
            self.misses += 1
            return self.missReward
        elif self.hit == 1:
            self.score += 1
            return self.goalReward
        else:
            return self.normalReward

    def update(self,world_state,realX,vx):
        reward = self.calcReward(list(world_state)[0],list(world_state)[1],realX,vx)
        robot_state = (self.calcState(),)
        state =world_state+robot_state              #merge states for one state
        action = self.ai.chooseAction(state)
        if self.lastAction is not None:
            self.ai.learn(self.lastState, self.lastAction, reward, state, action)
        self.lastState = state
        self.lastAction = action
        self.goAction(action)

    def calcState(self):
        return self.pos


