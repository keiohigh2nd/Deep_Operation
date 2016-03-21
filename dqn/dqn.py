import pickle
import numpy as np
import scipy.misc as spm
import copy

from chainer import cuda, FunctionSet, Variable, optimizers
import chainer.functions as F
import prepare_dataset

class DQN_class:
    gamma = 0.99  
    initial_exploration = 100 
    replay_size = 32  
    target_model_update_freq = 10**4  
    data_size = 20

    def __init__(self, enable_controller=[0, 3, 4]):
        self.num_of_actions = len(enable_controller)
        self.enable_controller = enable_controller 

        print "Initializing DQN..."

        print "Model Building"
        self.model = FunctionSet(
            l1=F.Convolution2D(3, 32, ksize=8, stride=4, nobias=False, wscale=np.sqrt(2)),
            l2=F.Convolution2D(32, 64, ksize=4, stride=2, nobias=False, wscale=np.sqrt(2)),
            l3=F.Convolution2D(64, 64, ksize=3, stride=1, nobias=False, wscale=np.sqrt(2)),
            l4=F.Linear(3136, 512, wscale=np.sqrt(2)),
            q_value=F.Linear(512, self.num_of_actions,
                             initialW=np.zeros((self.num_of_actions, 512),
                                               dtype=np.float32))
        )

        self.model_target = copy.deepcopy(self.model)

        print "Initizlizing Optimizer"
        self.optimizer = optimizers.RMSpropGraves(lr=0.00025, alpha=0.95, momentum=0.95, eps=0.0001)
        self.optimizer.setup(self.model.collect_parameters())

        # History Data :  D=[s, a, r, s_dash, end_episode_flag]
        self.D = [np.zeros((self.data_size, 800, 1024, 3), dtype=np.uint8),
                  np.zeros(self.data_size, dtype=np.uint8),
                  np.zeros((self.data_size, 1), dtype=np.int8),
                  np.zeros((self.data_size, 3, 84, 84), dtype=np.uint8),
                  np.zeros((self.data_size, 1), dtype=np.bool)]

    def forward(self, state, action, Reward, state_dash, episode_end):
        num_of_batch = state.shape[0]
        s = Variable(state)
        s_dash = Variable(state_dash)

        Q = self.Q_func(s)  # Get Q-value

        # Generate Target Signals
        tmp = self.Q_func_target(s_dash)  # Q(s',*)
        tmp = list(map(np.max, tmp.data.get()))  # max_a Q(s',a)
        max_Q_dash = np.asanyarray(tmp, dtype=np.float32)
        target = np.asanyarray(Q.data.get(), dtype=np.float32)

        for i in xrange(num_of_batch):
            if not episode_end[i][0]:
                tmp_ = np.sign(Reward[i]) + self.gamma * max_Q_dash[i]
            else:
                tmp_ = np.sign(Reward[i])

            action_index = self.action_to_index(action[i])
            target[i, action_index] = tmp_

        # TD-error clipping
        td = Variable(cuda.to_gpu(target)) - Q  # TD error
        td_tmp = td.data + 1000.0 * (abs(td.data) <= 1)  # Avoid zero division
        td_clip = td * (abs(td.data) <= 1) + td/abs(td_tmp) * (abs(td.data) > 1)

        zero_val = Variable(cuda.to_gpu(np.zeros((self.replay_size, self.num_of_actions), dtype=np.float32)))
        loss = F.mean_squared_error(td_clip, zero_val)
        return loss, Q

    def stockExperience(self, time,
                        state, action, reward, state_dash,
                        episode_end_flag):
        data_index = time % self.data_size

        if episode_end_flag is True:
            self.D[0][data_index] = state
            self.D[1][data_index] = action
            self.D[2][data_index] = reward
        else:
            self.D[0][data_index] = state
            self.D[1][data_index] = action
            self.D[2][data_index] = reward
            self.D[3][data_index] = state_dash
        self.D[4][data_index] = episode_end_flag

    def experienceReplay(self, time):

        if self.initial_exploration < time:
            # Pick up replay_size number of samples from the Data
            if time < self.data_size:  # during the first sweep of the History Data
                replay_index = np.random.randint(0, time, (self.replay_size, 1))
            else:
                replay_index = np.random.randint(0, self.data_size, (self.replay_size, 1))

            s_replay = np.ndarray(shape=(self.replay_size, 4, 84, 84), dtype=np.float32)
            a_replay = np.ndarray(shape=(self.replay_size, 1), dtype=np.uint8)
            r_replay = np.ndarray(shape=(self.replay_size, 1), dtype=np.float32)
            s_dash_replay = np.ndarray(shape=(self.replay_size, 4, 84, 84), dtype=np.float32)
            episode_end_replay = np.ndarray(shape=(self.replay_size, 1), dtype=np.bool)
            for i in xrange(self.replay_size):
                s_replay[i] = np.asarray(self.D[0][replay_index[i]], dtype=np.float32)
                a_replay[i] = self.D[1][replay_index[i]]
                r_replay[i] = self.D[2][replay_index[i]]
                s_dash_replay[i] = np.array(self.D[3][replay_index[i]], dtype=np.float32)
                episode_end_replay[i] = self.D[4][replay_index[i]]

            s_replay = cuda.to_gpu(s_replay)
            s_dash_replay = cuda.to_gpu(s_dash_replay)

            # Gradient-based update
            self.optimizer.zero_grads()
            loss, _ = self.forward(s_replay, a_replay, r_replay, s_dash_replay, episode_end_replay)
            loss.backward()
            self.optimizer.update()

    def Q_func(self, state):
        h1 = F.relu(self.model.l1(state))  # scale inputs in [0.0 1.0]
        h2 = F.relu(self.model.l2(h1))
        h3 = F.relu(self.model.l3(h2))
        h4 = F.relu(self.model.l4(h3))
        Q = self.model.q_value(h4)
        return Q

    def Q_func_target(self, state):
        h1 = F.relu(self.model_target.l1(state))  # scale inputs in [0.0 1.0]
        h2 = F.relu(self.model_target.l2(h1))
        h3 = F.relu(self.model_target.l3(h2))
        h4 = F.relu(self.model.l4(h3))
        Q = self.model_target.q_value(h4)
        return Q

    def e_greedy(self, state, epsilon):
        s = Variable(state)
        Q = self.Q_func(s)
        Q = Q.data

        if np.random.rand() < epsilon:
            index_action = np.random.randint(0, self.num_of_actions)
            print "RANDOM"
        else:
            index_action = np.argmax(Q.get())
            print "GREEDY"
        return self.index_to_action(index_action), Q

    def target_model_update(self):
        self.model_target = copy.deepcopy(self.model)

    def index_to_action(self, index_of_action):
        return self.enable_controller[index_of_action]

    def action_to_index(self, action):
        return self.enable_controller.index(action)

if __name__ == "__main__":
    DQN = DQN_class()
    state, state_dash, action, rewards = prepare_dataset.init()
    print state[0].shape
    DQN.forward(state[0], action[0][0], rewards[0], state_dash, 'False')
