###IMPORTS AND HANDLING
import math
import random
import pprint

###DO NOT MODIFY THE BELOW LINES ####
from controller import Robot, Receiver, Emitter

###DO NOT MODIFY THE ABOVE LINES ####


current_positions = {}

if __name__ == "__main__":
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())
    receiver = robot.getReceiver("receiver")
    receiver.enable(timestep)
    emitters = [robot.getEmitter("emitter " + str(i)) for i in range(1, 5)] 
    while robot.step(timestep) != -1:        
        while(receiver.getQueueLength() > 0):
            data = receiver.getData().decode("ascii").strip("[]").split(", ")
            data[1:] = [float(i) for i in data[1:]]
            data[0] = data[0].strip("'")
            current_positions[data[0]] = data[1:]
            receiver.nextPacket()            
        print(current_positions)


    
            