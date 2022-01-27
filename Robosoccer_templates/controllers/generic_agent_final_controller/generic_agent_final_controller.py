from controller import Robot, Motor, GPS, InertialUnit, Emitter, Receiver
robot = Robot()
timestep = int(robot.getBasicTimeStep())
gps = robot.getGPS("gps")
gps.enable(timestep)
inertialUnit = robot.getInertialUnit("inertial unit")
inertialUnit.enable(timestep)
emitter = robot.getEmitter("emitter")
OLD_DATA = None
transmission_iteration_variable = 0
TRANSMIT_INTERVAL = 1
NAME = robot.getName()
receiver = robot.getReceiver("receiver")
receiver.enable(timestep)

import math

PUSHER_REWIND_FORCE = -5
PUSHER_FORWARD_FORCE = 20
pusher_motor = robot.getMotor("pusher_motor")
pusher_motor.setPosition(float('inf'))

ROLLER_MOTOR_VEL = -150
roller_motor = robot.getMotor("roller_motor")
roller_motor.setPosition(float('inf'))
roller_motor.setVelocity(ROLLER_MOTOR_VEL)

MAX_WHEEL_VELOCITY = 60
motors = [robot.getMotor("motor_" + str(i)) for i in range(1,5)]
[motor.setPosition(float('inf')) for motor in motors]
[motor.setVelocity(0) for motor in motors]

WHEEL_TO_CENTER = 0.06660945878
WHEEL_RADIUS = 0.015

while robot.step(timestep) != -1:
    if(transmission_iteration_variable%TRANSMIT_INTERVAL == 0):
        transmit = False
        data_raw = [round(i, 3) for i in gps.getValues() + inertialUnit.getRollPitchYaw()]
        data_raw = [data_raw[0], data_raw[2] , data_raw[5]]
        data_raw = [NAME] + data_raw
        if(OLD_DATA is None):
            transmit = True
            OLD_DATA = data_raw
        # print(",",data)
        else:
            for i in range(len(data_raw)):
                if(OLD_DATA[i] != data_raw[i]):
                    transmit = True
                    OLD_DATA = data_raw
        if(transmit):
            emitter.send(bytes(str(data_raw), 'ascii'))
    transmission_iteration_variable += 1
    if(receiver.getQueueLength() > 0):
        data = receiver.getData().decode('ascii')
        receiver.nextPacket()
        data =data.strip("[]").split(", ")
        data = [float(i) for i in data]
        desired_linear_V = tuple(data[0:2])
        desired_angular_V = data[2]
        desired_pusher_state = data[3]

        v_mod = math.sqrt(desired_linear_V[0]**2 + desired_linear_V[1]**2)
        alpha = math.atan2(-desired_linear_V[1], desired_linear_V[0])
        m1_vel = -v_mod*math.cos(math.pi/4 - alpha)/WHEEL_RADIUS
        m2_vel = m1_vel
        m3_vel = v_mod*math.cos(math.pi/4 + alpha)/WHEEL_RADIUS
        m4_vel = m3_vel

        m1_vel -= desired_angular_V*WHEEL_TO_CENTER/WHEEL_RADIUS
        m2_vel += desired_angular_V*WHEEL_TO_CENTER/WHEEL_RADIUS
        m3_vel -= desired_angular_V*WHEEL_TO_CENTER/WHEEL_RADIUS
        m4_vel += desired_angular_V*WHEEL_TO_CENTER/WHEEL_RADIUS
        vels = [m1_vel, m2_vel, m3_vel, m4_vel]
        i = 0
        while(any(abs(i) > MAX_WHEEL_VELOCITY for i in vels)):
            i += 1
            vels = [j/1.2 for j in vels]
        for i in range(4):
            motors[i].setVelocity(vels[i])
        if(desired_pusher_state == 0):
            pusher_motor.setForce(PUSHER_REWIND_FORCE)
        else:
            pusher_motor.setForce(PUSHER_FORWARD_FORCE)
    