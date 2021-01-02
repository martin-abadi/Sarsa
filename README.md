# SarsaReinforcement Learning project
RL of a robot to play hockey table, implementing SARSA and image segmentation to train the movement of the robot.

1) On the first step, we track the ball movement on videos, in order to understand and mimic the movements for a simulation that will help us teach the robot.

2) Secondly, we create the simulation of the ball moving towards the robot, and moduled the situation and actions the robot can do.

3) We checked hyperparameters for the SARSA policy. We finally chose α=0.1; 𝛾=0.9; 𝜀=0.1. Rewards: 100 for kicking, 0 for not moving, -10 for missing.

An improvement of 42.5% kicking the ball, after 100K iterations.

1 - The segmentation was done by changing each frame of a video to an RGB matrix, looking for a strong color of red or green (two ball colors).    
    Turning the RGB picture to HSV picture, we define a threshold above 0.85 for the color of the ball, and detect the biggest mass of white pixels, to finally describe the place of the ball.
    A sanity check of the position output was done.
    
2 - The field was divided to 6*6 squares, thus the place of the ball was translated more clearly to the robot.    
    The states of the robot: Place Up, Place Middle, Place Up    
    Actions: Don't move, move up, move down, kick up, kick middle, kick down.
    
3 - We used an epsilon-greedy policy to choose the best action.
