import serial
import math
import threading
import time


class DriveTest:
    def commandThread(self):
        while self.running:
            #time.sleep(0.05)
            #print(self.speed1)
            vastus = self.ser.read(19)
            if len(vastus) > 0:
                print(vastus)
                self.gameOn = self.parseRefCommand(vastus,self.field,self.robotChar)
                print(self.gameOn)
            text = ("sd:" + str(self.speed1) + ":" + str(self.speed2) + ":" + str(self.speed3) + "\r\n")
            self.ser.write('f0\r\n'.encode('utf-8'))
            time.sleep(0.005)
            self.ser.write(text.encode('utf-8'))
            time.sleep(0.005)
            self.ser.write(('d:'+ str(self.throwSpeed)+ '\r\n').encode('utf-8'))


    def __init__(self):
        self.running = True
        self.w = threading.Thread(name='commandThread', target=self.commandThread)
        self.speed1 = 0
        self.speed2 = 0
        self.speed3 = 0
        self.dist = 0.115
        self.f = open("RFinfo.txt")
        self.field = self.f.readline().split("=")[1].split("#")[0].strip()
        self.robotChar = self.f.readline().split("=")[1].split("#")[0].strip()
        self.n = 'rf:a' + self.field + self.robotChar
        self.f.close()
        self.throwSpeed = 1000
        self.wheelone = 0
        self.wheeltwo = 120
        self.wheelthree = 240
        self.gameOn = False
        self.ser = serial.Serial('COM3', baudrate=9600, timeout=0.005)
        self.w.start()

    def stopThrow(self):
        self.throwSpeed= 1000

    def shutdown(self):
        self.speed1 = 0
        self.speed2 = 0
        self.speed3 = 0


    def spinright(self):

        self.speed1 = -9
        self.speed2 = -9
        self.speed3 = -9


    def spinleft(self):
        self.speed1 = 9
        self.speed2 = 9
        self.speed3 = 9


    def circleBallLeft(self):
        self.speed1 = 9
        self.speed2 = 0
        self.speed3 = 0

    def circleBallRight(self):
        self.speed1 = -9
        self.speed2 = 0
        self.speed3 = 0

    def parseRefCommand(self, command, field, robotChar):
        print "cmd " + command
        pieces = command.split(":")
        if pieces[1][1] != field:
            return self.gameOn
        if pieces[1][2] != robotChar and pieces[1][2] != "X":
            return self.gameOn
        if "START" in command:
            self.ser.write(self.n + 'ACK-----\r\n')
            return True
        elif "STOP" in command:
            self.ser.write(self.n + 'ACK-----\r\n')
            self.shutdown()
            return False
        elif "PING" in command:
            self.ser.write(self.n + 'ACK-----\r\n')
            return self.gameOn

    # print(self.ser.isOpen(self))

    # wheelLinearVelocity = robotSpeed * cos(robotDirectionAngle - wheelAngle) + wheelDistanceFromCenter * robotAngularVelocity

    def wheelLogic(self,robotspeed, wheel, suund):
        speed = robotspeed * math.cos(math.radians(suund - wheel))  # +dist*angVel
        return speed

    def startThrow(self, speed):
        self.throwSpeed = speed


    def setspeed(self,suund, speed):
        self.speed1 = int(self.wheelLogic(-speed, self.wheelone, suund))
        self.speed2 = int(self.wheelLogic(-speed, self.wheeltwo,suund))
        self.speed3 = int(self.wheelLogic(-speed, self.wheelthree, suund))


    #    print("mootor1")
    #   print(spd1)
    # print("mootor2")
    #  print(spd2)
    # print("mootor3")
    # print(spd3)
    """
    setspeed(180)
    frame = np.zeros((200,200))
    while(True):
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        #print(key)
        # if the 'q' key is pressed, stop the loop
        if key == ord("w"):
            setspeed(90)
        if key == ord("a"):
            setspeed(180)
        if key == ord("s"):
            setspeed(270)
        if key == ord("d"):
            setspeed(0)

        if key == ord("q"):
            shutdown()
            ##cv2.imwrite("test.png", frame)
            break

    """

    # print(wheelLogic(1,wheelone,dist,1,180))
