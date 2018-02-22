#!/usr/bin/env python
# coding=utf-8
'''
Author:Tai Lei
Date:Do 15 Feb 2018 09:30:40 CST
Info:
'''

import numpy as np
import queue
from heapq import *
from collections import deque
import time

class IntelligentScissor():

    def __init__(self, img):

        '''
        @img: numpy array
        @seed: [row,column]
        '''
        self.height = img.shape[0]
        self.width = img.shape[1]
        self.img = img.reshape(self.height, self.width, -1).astype(np.float32)
        self.dim = self.img.shape[2]
        self.pad_img = np.lib.pad(self.img, 
                ((1,1),(1,1),(0,0)), 'constant', constant_values=0)

        self.link_cost = np.zeros((self.height, self.width, 8),
                dtype=np.float32)
        self.cost_graph=np.zeros((self.height*3, self.width*3, self.dim),
                dtype=np.float32)
        self.node_dict = {}

        self.INITIAL =0
        self.ACTIVE  =1
        self.EXPAND  =2
        self.BORDER  =3
        self.link_calculation()
        self.generate_all_node_dict()
        
    def coordinate2key(self, pose):
        return self.width*pose[0]+pose[1]

    def key2coordinate(self, key):
        return (key//self.width, key%self.width)

    def get_path(self, pose):
        path = []
        path.append(pose)
        pose = (pose[1],pose[0])
        pose_key = self.coordinate2key(pose)
        while self.node_dict[pose_key].prev_node != None:
            new_pose_key = self.node_dict[pose_key].prev_node 
            new_pose_node = self.node_dict[new_pose_key]
            new_pose = self.key2coordinate(new_pose_key)
            path.append((new_pose[1],new_pose[0]))
            pose_key = new_pose_key
        return path

    def link_calculation(self):

        up_down = self.pad_img[:-2,:,:] - self.pad_img[2:,:,:]
        link_cost_0 = np.abs(up_down[:,1:-1,:] + up_down[:,2:,:])/4
        self.link_cost[:,:,0] = np.sqrt(np.sum(link_cost_0**2, axis=2)/self.dim)

        left_right = self.pad_img[:,:-2,:] - self.pad_img[:,2:,:]
        link_cost_6 = np.abs(left_right[1:-1,:,:] + left_right[2:,:,:])/4
        self.link_cost[:,:,6] = np.sqrt(np.sum(link_cost_6**2, axis=2)/self.dim)

        link_cost_1 = np.abs(self.pad_img[:-2,1:-1,:]-self.pad_img[1:-1,2:,:])/np.sqrt(2)
        self.link_cost[:,:,1] = np.sqrt(np.sum(link_cost_1**2, axis=2)/self.dim)

        link_cost_7 = np.abs(self.pad_img[1:-1,2:,:]-self.pad_img[2:,1:-1,:])/np.sqrt(2)
        self.link_cost[:,:,7] = np.sqrt(np.sum(link_cost_7**2, axis=2)/self.dim)

        self.link_cost[ :,   1:,  4] = self.link_cost[ :,   :-1,  0]
        self.link_cost[1:,    :,  2] = self.link_cost[ :-1, :,    6]
        self.link_cost[1:,   1:,  3] = self.link_cost[ :-1, :-1,  7]
        self.link_cost[ :-1, 1:,  5] = self.link_cost[1:,   :-1,  1]

        link_length = np.array([1,np.sqrt(2),1,np.sqrt(2),1,np.sqrt(2),1,np.sqrt(2)])
        self.link_cost = ((np.max(self.link_cost)-self.link_cost)*link_length)/2
        self.cost_graph[1::3,2::3,:]=self.link_cost[:,:,:1]\
                +np.zeros(self.dim)
        self.cost_graph[ ::3,2::3,:]=self.link_cost[:,:,1:2]\
                +np.zeros(self.dim)
        self.cost_graph[ ::3,1::3,:]=self.link_cost[:,:,2:3]\
                +np.zeros(self.dim)
        self.cost_graph[ ::3, ::3,:]=self.link_cost[:,:,3:4]\
                +np.zeros(self.dim)
        self.cost_graph[1::3, ::3,:]=self.link_cost[:,:,4:5]\
                +np.zeros(self.dim)
        self.cost_graph[2::3, ::3,:]=self.link_cost[:,:,5:6]\
                +np.zeros(self.dim)
        self.cost_graph[2::3,1::3,:]=self.link_cost[:,:,6:7]\
                +np.zeros(self.dim)
        self.cost_graph[2::3,2::3,:]=self.link_cost[:,:,7:8]\
                +np.zeros(self.dim)
        self.cost_graph[1::3,1::3,:]=self.img
        return self.cost_graph

    def cost_map_generation(self):
        self.update_seed_node(self.seed)
        self.update_node_dict()
        self.pq = []
        heappush(self.pq, (0, self.coordinate2key(self.seed)))
        while len(self.pq)>0:
            prev_pop = heappop(self.pq)
            prev_node_key = prev_pop[1]
            prev_cost = prev_pop[0]

            prev_node_obj = self.node_dict[prev_node_key]
            if prev_node_obj.state == self.EXPAND:
                continue
            prev_node_obj.state = self.EXPAND
            self.node_dict[prev_node_key] = prev_node_obj
            for n_pose in prev_node_obj.neighbours:
                n_pose_node = self.node_dict[n_pose[0]]
                n_pose_state = n_pose_node.state
                if n_pose_state==self.EXPAND:
                    continue
                elif n_pose_state==self.INITIAL:
                    new_cost = prev_cost+n_pose[1]
                    heappush(self.pq, (new_cost, n_pose[0]))
                    n_pose_node.state = self.ACTIVE
                    n_pose_node.cost = new_cost
                    n_pose_node.prev_node = prev_node_key
                    self.node_dict[n_pose[0]]=n_pose_node
                elif n_pose_state==self.ACTIVE:
                    new_cost = prev_cost+n_pose[1]
                    old_cost = self.node_dict[n_pose[0]].cost
                    if old_cost>new_cost:
                        heappush(self.pq, (new_cost, n_pose[0]))
                        n_pose_node.prev_node = prev_node_key
                        n_pose_node.cost = new_cost
                        self.node_dict[n_pose[0]]=n_pose_node


    def get_neighbor_nodes(self, pose):
        row = pose[0]
        column = pose[1]
        return [(row  ,  column+1),
                (row-1,  column+1),
                (row-1,  column  ),
                (row-1,  column-1),
                (row  ,  column-1),
                (row+1,  column-1),
                (row+1,  column  ),
                (row+1,  column+1)]

    def get_neighbor_node_keys(self, pose, link_cost):
        row = pose[0]
        column = pose[1]
        return [[self.coordinate2key((row  ,  column+1)), link_cost[0]],
                [self.coordinate2key((row-1,  column+1)), link_cost[1]],
                [self.coordinate2key((row-1,  column  )), link_cost[2]],
                [self.coordinate2key((row-1,  column-1)), link_cost[3]],
                [self.coordinate2key((row  ,  column-1)), link_cost[4]],
                [self.coordinate2key((row+1,  column-1)), link_cost[5]],
                [self.coordinate2key((row+1,  column  )), link_cost[6]],
                [self.coordinate2key((row+1,  column+1)), link_cost[7]]]

    def generate_all_node_dict(self):
        for i in range(1,self.height-1):
            for j in range(1,self.width-1):
                self.node_dict[self.coordinate2key((i,j))]=\
                        PQ_Node(None, self.INITIAL, self.get_neighbor_node_keys((i,j), self.link_cost[i][j]), 0)
        self.margin_node_update()

    def update_seed(self, seed):
        self.seed = (seed[1], seed[0])
    
    def update_seed_node(self, seed):
        seed_key = self.coordinate2key(seed) 
        seed_node = self.node_dict[seed_key]
        seed_node.prev_node = None
        self.node_dict[seed_key] = seed_node

    def update_node_dict(self):
        for key in self.node_dict:
            node_ = self.node_dict[key]
            node_.state = self.INITIAL
            self.node_dict[key]=node_
        self.margin_node_update()

    def margin_node_update(self):
        for i in [0, self.height-1]:
            for j in range(self.width):
                self.node_dict[self.coordinate2key((i,j))]=\
                        PQ_Node(None, self.EXPAND, None, 0)
        for i in range(self.height):
            for j in [0, self.width-1]:
                self.node_dict[self.coordinate2key((i,j))]=\
                        PQ_Node(None, self.EXPAND, None, 0)
    
    def update_path_dict(self, all_path):
        for path in all_path:
            for node in path:
                self.node_dict[self.coordinate2key((node[1],node[0]))]=\
                        PQ_Node(None, self.BORDER, None, 0)

    def generate_mask(self, path_point):
        mask = np.zeros((self.height, self.width),dtype=np.int32)
        dq = deque()
        inside_flag = False
        self.update_node_dict()
        self.update_path_dict(path_point)
        seed_row = np.random.randint(1, self.height-1)
        seed_column = np.random.randint(1, self.width-1)
        seed_key = self.coordinate2key((seed_row, seed_column))
        while self.node_dict[seed_key].state==self.BORDER:
            seed_row = np.random.randint(1, self.height-1)
            seed_column = np.random.randint(1, self.width-1)
            seed_key = self.coordinate2key((seed_row, seed_column))
        dq.append(seed_key)
        while len(dq) > 0:
            root_key = dq.popleft()
            root_node = self.node_dict[root_key]
            root_row = root_key//self.width
            root_column = root_key%self.width
            mask[root_row][root_column]=1
            self.node_dict[root_key] = root_node
            for n_pose in root_node.neighbours[::2]:
                n_pose_node = self.node_dict[n_pose[0]]
                n_pose_state = n_pose_node.state
                if n_pose_state == self.INITIAL:
                    dq.append(n_pose[0])
                    n_pose_node.state = self.ACTIVE
                    self.node_dict[n_pose[0]] = n_pose_node
                elif ((inside_flag == False) and (n_pose_state==self.EXPAND)):
                    inside_flag = True
                    continue
                else:
                    continue
        if inside_flag == True:
            mask = 1-mask
        return mask

class PQ_Node():
    def __init__(self, prev_node, state, neighbours, cost):
        self.prev_node = prev_node
        self.state = state
        self.neighbours = neighbours
        self.cost = cost

if __name__=="__main__":
    import cv2
    #img = cv2.imread("../images/test2.jpg", cv2.IMREAD_GRAYSCALE)
    img = cv2.imread("../images/test3.jpeg")
    #img = cv2.resize(img, (15,15))
    seed = (240,199)
    obj = IntelligentScissor(img)
    #obj.link_calculation()
    #start = time.time()
    #obj.generate_all_node_dict()
    #print ("node dict time:", time.time()-start)
    obj.update_seed(seed)
    start = time.time()
    obj.cost_map_generation()
    print ("cost map time:", time.time()-start)
    obj.get_path((266,165))
