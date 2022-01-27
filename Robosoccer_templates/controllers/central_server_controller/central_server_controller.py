from controller import Robot, Receiver, Emitter
import math
robot = Robot()
timestep = int(robot.getBasicTimeStep())

receiver = robot.getReceiver("receiver")
receiver.enable(timestep)
left_emitter = robot.getEmitter("left_emitter")
right_emitter = robot.getEmitter("right_emitter")

while robot.step(timestep) != -1:
    while(receiver.getQueueLength() > 0):
        data = receiver.getData().decode("ascii").strip("[]").split(", ")
        data[1:] = [float(i) for i in data[1:]]
        data[0] = data[0].strip("'")
        receiver.nextPacket()
        right_emitter.send(bytes(str(data), 'ascii'))
        if(data[0] == 'ball'):
            new_data = [data[0], -data[1], data[2], -data[3]]
        else:
            new_data = [data[0], -data[1], -data[2], data[3] + math.pi]
            if(new_data[3] > math.pi):
                new_data[3] = new_data[3] - 2*math.pi
            new_data[3] = round(new_data[3], 3)
        left_emitter.send(bytes(str(new_data), 'ascii'))

#TO IMPLEMENT: Detection of the goal and resetting the simulation

        