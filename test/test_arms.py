#import the USB and Time librarys into Python
import usb.core, usb.util, time

#Define a procedure to execute each movement
def MoveArm(Duration, ArmCmd, RoboArm):
    #Start the movement
    RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,3)
    #Stop the movement after waiting a specified duration
    time.sleep(Duration)
    ArmCmd=[0,0,0]
    RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,3)
