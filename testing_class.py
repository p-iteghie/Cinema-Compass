from adjacency_list_handler import CSV_handle
from array_holder import Columns
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from IPython.display import display
import numpy as np
import csv
import imdb
import networkx as nx
from matplotlib import pyplot as plt
from pyvis.network import Network


def BFS(adjacency_list,desired_name,names):
    queue = [0]
    visited = set()
    while(len(queue) != 0 or len(visited) != len(adjacency_list)): #while there's still items in the queue, and not all nodes visited
        #code below here is handling a non-connected graph
        if len(queue) == 0: #get the next disjoint node
            for index in range(20001):
                if(index not in visited):
                    queue.append(index)
                    break

        #code below is for a regular graph
        current_node = int(queue.pop(0))
        visited.add(current_node)  # adds the edge to the set
        #print(names[current_node]) TOIWEHGOIUEHOIGHJEIOGHIRJHOIGRHIOGHEOIRHGOIHROIHGRORHEOIRGHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        if(names[current_node] == desired_name):
            return current_node
        neighbors = adjacency_list[current_node] #the array at index
        for edge in neighbors[1:]:
            if (int(edge) not in visited):
                queue.append(edge)
    return -1

def DFS(adjacency_list,desired_name,names):
    queue = [0]
    visited = set()
    while(len(queue) != 0 or len(visited) != len(adjacency_list)): #while there's still items in the queue, and not all nodes visited
        #code below here is handling a non-connected graph
        if len(queue) == 0: #get the next disjoint node
            for index in range(20001):
                if(index not in visited):
                    queue.append(index)
                    break

        #code below is for a regular graph
        current_node = int(queue.pop())
        visited.add(current_node)  # adds the edge to the set
        #print(names[current_node]) TOIWEHGOIUEHOIGHJEIOGHIRJHOIGRHIOGHEOIRHGOIHROIHGRORHEOIRGHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        if(names[current_node] == desired_name):
            return current_node
        neighbors = adjacency_list[current_node] #the array at index
        for edge in neighbors[1:]:
            if (int(edge) not in visited):
                queue.append(edge)
    return -1

def rebuild_adjacency(file_name):
    adjacency_list_final = [[]] * 20001
    index = 0
    file = open(file_name)
    lines = file.readlines()
    for line in lines:
        temp_line = line.strip("\n")
        temp_array = temp_line.split(",")
        adjacency_list_final[index] = temp_array
        index += 1
        if (index == 20001):
            break
    file.close()
    return adjacency_list_final


super_array = rebuild_adjacency("adjacency_listF.csv") #IF YOU CHANGE FILE NAME CHANGE THIS AS WELL
structure = Columns("data.csv")
print("built the array")
print(BFS(super_array,"Federico Fellini",structure.names))
print(DFS(super_array,"Federico Fellini",structure.names))

structure.movies_1[DFS(super_array,"Federico Fellini",structure.names)]



#new_object = CSV_handle("data.csv")    MAKES THE LIST
