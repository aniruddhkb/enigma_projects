from controller import Robot, GPS

robot = Robot()
timestep = int(robot.getBasicTimeStep())

gps = robot.getGPS("gps")
gps.enable(timestep)

emitter = robot.getEmitter("emitter")
OLD_DATA = None
TRANSMIT_INTERVAL = 10
i = 0
while robot.step(timestep) != -1:
    if(i % TRANSMIT_INTERVAL == 0):
        transmit = False
        data_raw = ["ball"] + [round(i, 3) for i in gps.getValues()]
        if(OLD_DATA is None):
            transmit = True
            OLD_DATA = data_raw
        else:
            for i in range(len(data_raw)):
                if(OLD_DATA[i] != data_raw[i]):
                    transmit = True
                    OLD_DATA = data_raw
        if(transmit):
            emitter.send(bytes(str(data_raw), 'ascii'))
    i += 1