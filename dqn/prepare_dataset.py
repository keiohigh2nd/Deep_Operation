# coding: utf-8
import os, cv2 
import numpy as np


def init():
    files = os.listdir('desc')

    state = []
    state_dash = []
    action = []
    rewards = []
    i = 0
    for file in files:
        tmp_s = cv2.imread('result/s_'+file.split('.')[0] +'.jpg')
        tmp_s = np.transpose(tmp_s)
        tmp_s = tmp_s.reshape((1,) + tmp_s.shape)
        tmp_s[0] = i
        state.append(tmp_s)

        tmp_s_dash = cv2.imread('result/s_dash_'+file.split('.')[0] +'.jpg')
        tmp_s_dash = np.transpose(tmp_s_dash)
        tmp_s_dash = tmp_s.reshape((1,) + tmp_s_dash.shape)
        tmp_s_dash[0] = i
        state_dash.append(tmp_s_dash)
    
        f = open('desc/%s'%file, 'r')
        tmp = f.read().split(',')
        action.append([tmp[0], tmp[1]])
        rewards.append(tmp[2])
        f.close() 

    state = np.array(state).astype(np.float32)/ 255
    state_dash = np.array(state_dash).astype(np.float32)/ 255

    
    #state = state.reshape((1,) + state.shape)
    return state, state_dash, action, rewards

if __name__ == "__main__":
    init()
