from adjacency_list_handler import CSV_handle
from array_holder import Columns

def BFS(adjacency_list,desired_name,names):
    queue = [0]
    visited = set()
    order = []
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
        order.append(names[current_node])
        if(names[current_node] == desired_name):
            return order
        neighbors = adjacency_list[current_node] #the array at index
        for edge in neighbors[1:]:
            if (int(edge) not in visited):
                queue.append(edge)
                visited.add(int(edge))
    return []

def DFS(adjacency_list,desired_name,names):
    stack = [0]
    visited = set()
    order = []
    while(len(stack) != 0 or len(visited) != len(adjacency_list)): #while there's still items in the stack, and not all nodes visited
        #code below here is handling a non-connected graph
        if len(stack) == 0: #get the next disjoint node
            for index in range(20001):
                if(index not in visited):
                    stack.append(index)
                    break

        #code below is for a regular graph
        current_node = int(stack.pop())
        visited.add(current_node)  # adds the edge to the set
        order.append(names[current_node])
        if(names[current_node] == desired_name):
            return order
        neighbors = adjacency_list[current_node] #the array at index
        for edge in neighbors[1:]:
            if (int(edge) not in visited):
                stack.append(edge)
                visited.add(int(edge))
    return []

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

# new_object = CSV_handle("data.csv") MAKES THE LIST
