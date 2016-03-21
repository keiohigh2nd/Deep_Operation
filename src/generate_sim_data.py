# vim: set fileencoding=utf-8 :
import numpy as np
import cv2
from Arm import Arm
import usb.core, usb.util, time
import move_arms

def robot_arm1(image, xyz):
    cv2.line(image, (0, 0), (xyz[0][1], xyz[0][0]), (0, 255, 0), 10)
    cv2.line(image, (xyz[0][1], xyz[0][0]), (xyz[1][1], xyz[1][0]), (0, 255, 0), 10)
    cv2.line(image,  (xyz[1][1], xyz[1][0]),  (xyz[2][1], xyz[2][0]), (0, 255, 0), 10)
    return image

def robot_arm2(image, xyz):
    cv2.line(image, (len(image[0]), 0), (xyz[0][1], xyz[0][0]), (255, 255, 128), 10)
    cv2.line(image, (xyz[0][1], xyz[0][0]), (xyz[1][1], xyz[1][0]), (255, 255, 128), 10)
    cv2.line(image,  (xyz[1][1], xyz[1][0]),  (xyz[2][1], xyz[2][0]), (255, 255, 128), 10)
    return image

def put_rectangles(rows, cols, image, pos):
    #Bottom
    cv2.rectangle(image,(pos[0][0][0], pos[0][0][1]), (pos[0][1][0], pos[0][1][1]),(255,0,0),cv2.cv.CV_FILLED)
    #TOP
    cv2.rectangle(image,(pos[1][0][0], pos[1][0][1]), (pos[1][1][0], pos[1][1][1]),(255,0,0),cv2.cv.CV_FILLED)
    return image

def fix_frames(arm1, arm2, image):
    image = robot_arm1(image, arm1.position)
    image = robot_arm2(image, arm2.position)
    return image

def init_frame(rows, cols, obj_pos):
    image = np.zeros((rows, cols, 3), np.uint8)
    image = put_rectangles(rows, cols, image, obj_pos)
    return image

def calculate(arm_pos, objs):
    #ここの距離の計算は要注意
    #HOW TO CALCULATE DISTANCE BETWEENE PATIENTS
    #Armが近い方が行くのか、3unitが近い方が行くのか、どっちだ。
    tmp1_x = (objs[0][0][0]-arm_pos[2][0])
    tmp1_y = (objs[0][0][1]-arm_pos[2][1])
    tmp2_x = (objs[1][0][0]-arm_pos[2][0])
    tmp2_y = (objs[1][0][1]-arm_pos[2][1])

    return tmp1_x, tmp1_y, tmp2_x, tmp2_y

def calc_dist(x1,y1,x2,y2):
    if (x1*x1+y1*y1) > (x2*x2 + y2*y2):
       return 2
    else:
       return 1

def random_position_init(arm1, arm2, objs, frame_id):
    #Set random movements(Move Limitation)
    arm1.set_random_position(1)
    arm2.set_random_position(2)

    #FIX S
    canvas_image = init_frame(rows, cols, obj_pos)
    image = fix_frames(arm1, arm2, canvas_image)
    cv2.imwrite('result/s_%s.jpg'%frame_id, image)

    #Calculate distance from objs
    d1_arm1_x, d1_arm1_y, d2_arm1_x, d2_arm1_y = calculate(arm1.position, objs)
    d1_arm2_x, d1_arm2_y, d2_arm2_x, d2_arm2_y = calculate(arm2.position, objs)

    if d1_arm1_x < 10 and d1_arm1_y < 10:
        print 'Catch and GO'
	arm1.action(8, 0, 0, 1)
    if d1_arm2_x < 10 and d1_arm2_y < 10:
    	print 'Catch and GO'
	arm1.action(8, 0, 0, 1)

    if d2_arm1_x < 10 and d2_arm1_y < 10:
        print 'Catch and GO'
	arm2.action(8, 0, 0, 2)
    if d2_arm2_x < 10 and d2_arm2_y < 10:
        print 'Catch and GO'
	arm2.action(8, 0, 0, 2)

    #Decide Actions
    nearest_arm_id = calc_dist(d1_arm1_x, d1_arm1_y, d1_arm2_x, d1_arm2_y) 
    if nearest_arm_id == 1:
	#適切な行動をここで取れ
	print 'A'
        #Move A to remove top and B should Remove Bottom ---> Multithreading
	arm1.action(6, abs(d1_arm1_x)/10, abs(d1_arm1_y)/10, 1)  #consider gradients
        arm2.action(7, abs(d2_arm2_x)/10, abs(d2_arm2_y)/10, 2)  #consider gradients
    else:
	print 'B'
	#Move B to remove top and A should Remove TOP --> multithreading
	arm1.action(5, abs(d2_arm1_x)/10, abs(d2_arm1_y)/10,1)
	arm2.action(5, abs(d1_arm2_x)/10, abs(d1_arm2_y)/10,2)

    #FIX S-dash
    canvas_image = init_frame(rows, cols, obj_pos)
    image = fix_frames(arm1, arm2, canvas_image)
    cv2.imwrite('result/s_dash_%s.jpg'%frame_id, image)

if __name__ == "__main__":
    cols = 1024
    rows = 800

    obj_pos = (([int(cols*0.6),int(rows*0.6)], [int(cols*0.6)+40, rows], [0,0]), ([int(cols*0.4),int(rows*0.4)], [int(cols*0.6)+100, int(rows*0.5)],[0,0]))
    
    arm1 = Arm(([100,100,0], [200,300,0], [400, 600, 0]))
    arm2 = Arm(([80,800,0], [100,700,0], [250, 500, 0]))

    actions = move_arms.sim_get_actions()

    canvas_image = init_frame(rows, cols, obj_pos)
    image = fix_frames(arm1, arm2, canvas_image)

    cv2.imwrite('result/ss-dash.jpg', image)
    canvas_image = init_frame(rows, cols, obj_pos)
    image = fix_frames(arm1, arm2, canvas_image)

    for frame_id in xrange(10): 
      random_position_init(arm1, arm2, obj_pos, frame_id)

