# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 08:28:17 2020

@author: ss21930
"""
#%%
from collections import defaultdict, deque
import numpy as np
import time

def read_input_graph(file_path):
    G = defaultdict(list)
    all_vert = []
    with open(file_path, 'r') as reader:
        line_num=0
        for line in reader.readlines():
            edge = line.split()
            G[int(edge[0])].append(int(edge[1]))
            all_vert.extend([int(edge[0]),int(edge[1])])
            line_num = line_num+1
    
    sink_vertices = set(all_vert).difference(set(G.keys()))
    for sink_vertex in sink_vertices:
        G[sink_vertex] = []
    return G

def reverse_graph(G):
    '''u -> v becomes v -> u''' 
    rev_graph = defaultdict(list)
    for u in G.keys():
        for v in G[u]:
            rev_graph[v].append(u)       
    sink_vertices = set(G.keys()).difference(set(rev_graph.keys()))
    for sink_vertex in sink_vertices:
        rev_graph[sink_vertex] = []   
    return rev_graph

def dfs_iterative_fin_time(G, s, color, finish_time_dict, time):
    S = deque()
    S.append(s)
    while len(S)!=0:
        v = S.pop() 
        if color[v]!=2:
            S.append(v)
            if color[v] == 0:
                color[v] = 1
            all_adj_discovered=True
            
            for w in G[v]:
                if color[w]==0:
                    S.append(w)
                    all_adj_discovered=False
        
            if all_adj_discovered==True:
                color[v]=2
                finish_time_dict[time]=v
                time=time+1
                S.pop()      
    return time 

def get_finishing_times(G):
    ''' Returns a dict with keys indicating finish time and value being the vertex'''
    color = dict(zip(G.keys(), [0]*len(G)))
    finish_time_dict = defaultdict()
    time = 1
    for vertex in range(1, len(G)+1):
        if color[vertex]==0:
            time = dfs_iterative_fin_time(G, vertex, color, \
                                                           finish_time_dict,time)
    return finish_time_dict

def scc_dfs_iterative(G, s, explored_status_scc, scc):
    explored_status_scc[s]=1
    S = deque()
    S.append(s)
    scc.append(s)
    while len(S)!=0:
        v = S.pop()
        for neigh_vertex in G[v]:
            if explored_status_scc[neigh_vertex]==0:
                explored_status_scc[neigh_vertex]=1
                S.append(neigh_vertex)
                scc.append(neigh_vertex)
    return None
        
def scc_kosaraju(G):
    rev_G = reverse_graph(G)
    finish_time_dict = get_finishing_times(rev_G) 
    explored_status_scc = dict(zip(G.keys(), [0]*len(G)))
    scc_list = []
    for finish_time in range(len(G),0,-1):
        vertex = finish_time_dict[finish_time]
        if explored_status_scc[vertex]==0:
            scc = []
            scc_dfs_iterative(G, vertex, explored_status_scc, scc)
            scc_list.append(scc)
    return scc_list

def find_largest_sccs(file_path, top_n=5):
    start_time = time.time()
    G = read_input_graph(file_path)	
    print('Time taken to read input:', time.time() - start_time, 'seconds')
    scc_list = scc_kosaraju(G)
    scc_size_list = [int(len(scc)) for scc in scc_list]
    sorted_scc_size_list = sorted(scc_size_list, reverse=True)
    
    size_largest_sccs = np.zeros(top_n, dtype=int)
    
    for i in range(min(len(scc_list), top_n)):
        size_largest_sccs[i] = sorted_scc_size_list[i]
        
    return list(size_largest_sccs)

#%%
file_path = 'scc_input_cases/programming_assignment_input.txt'
start_time = time.time()
largest_sccs = find_largest_sccs(file_path)
print('Total Execution Time:', time.time() - start_time, 'seconds')