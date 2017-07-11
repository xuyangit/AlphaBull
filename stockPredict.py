import tensorflow as tf
import numpy as np
import random
from collections import deque
import datetime
import json
import csv
from snownlp import SnowNLP
newsType = 5
files = [ "cpinews.txt", "estatenews.txt", "gdpnews.txt", "industrynews.txt",
         "ppinews.txt", "rmbnews.txt"]
trainData = {}
def collectFiles():
    for file in files:
        with open(file, encoding="utf-8") as f:
            for line in f:
                news = json.loads(line)
                if(news["time"] in trainData):
                    record = trainData[news["time"]]
                    s = SnowNLP(news["content"])
                    if(news["type"] in record):
                        record[news["type"]] += s.sentiments
                    else:
                        record[news["type"]] = s.sentiments
                else:
                    s = SnowNLP(news["content"])
                    trainData[news["time"]] = {news["type"]:s.sentiments}
collectFiles()
print(trainData)
with open("000001.csv") as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        print(line)

# Hyper Parameters for DQN
GAMMA = 0.9  # discount factor for target Q
INITIAL_EPSILON = 0.5  # starting value of epsilon
FINAL_EPSILON = 0.01  # final value of epsilon
REPLAY_SIZE = 10000  # experience replay buffer size
BATCH_SIZE = 32  # size of minibatch


class DQN():
    # DQN Agent
    def __init__(self, env):
        # init experience replay
        self.replay_buffer = deque()
        # init some parameters
        self.time_step = 0
        self.epsilon = INITIAL_EPSILON
        # self.state_dim = env.observation_space.shape[0]
        # self.action_dim = env.action_space.n
        self.state_dim = newsType
        self.action_dim = 3
        self.create_Q_network()
        self.create_training_method()
        # Init session
        self.session = tf.InteractiveSession()
        self.session.run(tf.initialize_all_variables())

    def create_Q_network(self):
        # network weights
        W1 = self.weight_variable([self.state_dim, 20])
        b1 = self.bias_variable([20])
        W2 = self.weight_variable([20, self.action_dim])
        b2 = self.bias_variable([self.action_dim])
        # input layer
        self.state_input = tf.placeholder("float", [None, self.state_dim])
        # hidden layers
        h_layer = tf.nn.relu(tf.matmul(self.state_input, W1) + b1)
        # Q Value layer
        self.Q_value = tf.matmul(h_layer, W2) + b2

    def create_training_method(self):
        self.action_input = tf.placeholder("float", [None, self.action_dim])
        # one hot presentation
        self.y_input = tf.placeholder("float", [None])
        Q_action = tf.reduce_sum(tf.mul(self.Q_value, self.action_input), reduction_indices=1)
        self.cost = tf.reduce_mean(tf.square(self.y_input - Q_action))
        # self.optimizer = tf.train.AdamOptimizer(0.0001).minimize(self.cost)
        self.optimizer = tf.train.RMSPropOptimizer(0.01, 0.1).minimize(self.cost)

    def perceive(self, state, action, reward, next_state, done):
        one_hot_action = np.zeros(self.action_dim)
        one_hot_action[action] = 1
        self.replay_buffer.append((state, one_hot_action, reward, next_state, done))

        if len(self.replay_buffer) > REPLAY_SIZE:
            self.replay_buffer.popleft()

        if len(self.replay_buffer) > BATCH_SIZE:
            self.train_Q_network()

    def train_Q_network(self):
        self.time_step += 1

        # Step 1: obtain random minibatch from replay memory
        minibatch = random.sample(self.replay_buffer, BATCH_SIZE)
        state_batch = [data[0] for data in minibatch]
        action_batch = [data[1] for data in minibatch]
        reward_batch = [data[2] for data in minibatch]
        next_state_batch = [data[3] for data in minibatch]

        # Step 2: calculate y
        y_batch = []
        Q_value_batch = self.Q_value.eval(feed_dict={self.state_input: next_state_batch})

        for i in range(0, BATCH_SIZE):
            done = minibatch[i][4]
            if done:
                y_batch.append(reward_batch[i])
            else:
                y_batch.append(reward_batch[i] + GAMMA * np.max(Q_value_batch[i]))

        self.optimizer.run(feed_dict={
            self.y_input: y_batch,
            self.action_input: action_batch,
            self.state_input: state_batch
        })

    def egreedy_action(self, state):
        Q_value = self.Q_value.eval(feed_dict={
            self.state_input: [state]})[0]
        if random.random() <= self.epsilon:
            return random.randint(0, self.action_dim - 1)
        else:
            return np.argmax(Q_value)

        self.epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / 10000

    def action(self, state):
        return np.argmax(self.Q_value.eval(feed_dict={
            self.state_input: [state]})[0])

    def weight_variable(self, shape):
        initial = tf.truncated_normal(shape)
        return tf.Variable(initial)

    def bias_variable(self, shape):
        initial = tf.constant(0.01, shape=shape)
        return tf.Variable(initial)


class News():
    def __init__(self, newsSentiment):
        self.newsSentiment = newsSentiment
        self.newsIndex = 0

    def render(self):
        # 尚未實作
        return

    def reset(self):
        self.newsIndex = 0
        return self.newsSentiment[self.newsIndex]

    # 0: 觀望, 1: 持有多單, 2: 持有空單
    def step(self, action):
        self.newsIndex += 1
        action_reward = self.newsSentiment[self.newsIndex][newsType - 1] - self.newsSentiment[self.newsIndex][newsType - 2]
        if (action == 0):
            action_reward = 0
        if (action == 2):
            action_reward = -1 * action_reward

        stock_done = False
        if self.newsIndex >= len(self.newsSentiment) - 1:
            stock_done = True
        else:
            stock_done = False
        return self.newsSentiment[self.newsIndex], action_reward, stock_done, 0

ENV_NAME = 'CartPole-v0'
EPISODE = 10000  # Episode limitation
STEP = 1000  # 300 # Step limitation in an episode
TEST = 10  # The number of experiment test every 100 episode


def main():
    # initialize OpenAI Gym env and dqn agent
    # env = gym.make(ENV_NAME)
    env = News(trainData)
    agent = DQN(env)

    print("begin!")
    for episode in range(EPISODE):
        # initialize task
        state = env.reset()

        # Train
        for step in range(STEP):
            action = agent.egreedy_action(state)  # e-greedy action for trai

            next_state, reward, done, _ = env.step(action)

            # Define reward for agent
            reward_agent = -1 if done else 0.1
            agent.perceive(state, action, reward, next_state, done)
            state = next_state
            if done:
                break

        # Test every 100 episodes
        if episode % 100 == 0:
            total_reward = 0

            for i in range(TEST):
                state = env.reset()

                for j in range(STEP):
                    env.render()
                    action = agent.action(state)  # direct action for test
                    state, reward, done, _ = env.step(action)
                    total_reward += reward
                    if done:
                        break

            ave_reward = total_reward / TEST
            print('episode: ', episode, 'Evaluation Average Reward:', ave_reward)
            if ave_reward >= 200:
                print("over!")
                break


if __name__ == '__main__':
    main()