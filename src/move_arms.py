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

def get_actions():
    actions = []
    actions.append([0,1,0]) #Rotate base anti-clockwise
    actions.append([0,2,0]) #Rotate base clockwise
    actions.append([64,0,0]) #Shoulder up
    actions.append([128,0,0]) #Shoulder down
    actions.append([16,0,0]) #Elbow up
    actions.append([32,0,0]) #Elbow down
    actions.append([4,0,0]) #Wrist up
    actions.append([8,0,0]) # Wrist down
    actions.append([2,0,0]) #Grip open
    actions.append([1,0,0]) #Grip close
    actions.append([0,0,1]) #Light on
    actions.append([0,0,0]) #Light off
    return actions

def sim_get_actions():
    actions = []
    actions.append([1,0,0]) #Rotate base anti-clockwise
    actions.append([-1,0,0]) #Rotate base clockwise
    actions.append([0,1,1]) #Shoulder up
    actions.append([0,-1,-1]) #Shoulder down
    actions.append([0,1,1]) #Elbow up
    actions.append([0,-1,-1]) #Elbow down
    actions.append([0,1,1]) #Wrist up
    actions.append([0,-1,-1]) # Wrist down
    actions.append([0,0,0]) #Grip open
    actions.append([0,0,0]) #Grip close
    actions.append([0,0,1]) #Light on
    actions.append([0,0,0]) #Light off
    return actions

