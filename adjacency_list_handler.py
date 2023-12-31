import pandas as pd
import numpy as np


class CSV_handle:
    def __init__(self,data_frame):
        df = pd.read_csv(data_frame, encoding='latin-1',dtype={'nconst': object, 'primaryName': object, 'birthYear': object, 'deathYear': object,'primaryProfession': object, 'knownForTitles': object})
        self.names = df['primaryName'].to_numpy()[0:20000]
        self.movies_1 = df['knownForTitles'].to_numpy()[0:20000]
        self.movies_2 = df['Unnamed: 6'].to_numpy()[0:20000]
        self.movies_3 = df['Unnamed: 7'].to_numpy()[0:20000]
        self.movies_4 = df['Unnamed: 8'].to_numpy()[0:20000]
        self.size = df.size
        self.adjacency_list = [np.array([])] * self.size
        #print(len(self.adjacency_list))
        self.initial_setup()
        self.edge_adder(self.movies_1, self.movies_4, False)
        self.edge_adder(self.movies_1, self.movies_3, False)
        self.edge_adder(self.movies_1,self.movies_2,False)  # stable configuration
        self.edge_adder(self.movies_1,self.movies_1,True)  # stable configuration

        self.edge_adder(self.movies_2, self.movies_4, False)
        self.edge_adder(self.movies_2, self.movies_3, False)
        self.edge_adder(self.movies_2, self.movies_1, False)  # stable configuration
        self.edge_adder(self.movies_2, self.movies_2, True)  # stable configuration

        self.edge_adder(self.movies_3, self.movies_4, False)
        self.edge_adder(self.movies_3, self.movies_3, True)
        self.edge_adder(self.movies_3, self.movies_1, False)  # stable configuration
        self.edge_adder(self.movies_3, self.movies_2, False)  # stable configuration

        self.edge_adder(self.movies_4, self.movies_4, True)
        self.edge_adder(self.movies_4, self.movies_3, False)
        self.edge_adder(self.movies_4, self.movies_1, False)  # stable configuration
        self.edge_adder(self.movies_4, self.movies_2, False)  # stable configuration

        print("done")
        self.pad_arrays()
        print("done")
        #adjacency_list = np.array(self.adjacency_list)
        #df = pd.DataFrame(adjacency_list)
        #df.to_csv('adjacency_list.csv', header=False,mode = 'a')
    def edge_adder(self,column_start,column_compare,identical):
        index_column_start = 0
        index_column_compare = 0
        for in_movie in column_start:
            for other_movie in column_compare:
                if (in_movie == other_movie and (identical == False or index_column_compare != index_column_start)): #append to the list if not the same element, and they match
                    self.adjacency_list[index_column_start] = np.append(self.adjacency_list[index_column_start],index_column_compare)
                index_column_compare+= 1
            index_column_compare = 0
            index_column_start += 1
    """def edge_adder(self,column_start,column_compare,identical):
        for in_movie in enumerate(column_start):
            for other_movie in enumerate(column_compare):
                if (in_movie[1] == other_movie[1] and (identical == False or in_movie[0] != other_movie[0])): #append to the list if not the same element, and they match
                    self.adjacency_list[in_movie[0]].append(other_movie[0])
                    #print(1)
                    #slower with enumerate"""
    def pad_arrays(self):
        for numpy_array in self.adjacency_list:
            df = pd.DataFrame(numpy_array)
            df = df.transpose().astype((int))[0:20000]
            df.to_csv('adjacencyListFinal.csv', header=False,index=False, mode='a') #change the name of the output file
    def initial_setup(self):
        index = 0
        for numpy_array in self.adjacency_list:
            self.adjacency_list[index] = np.append(self.adjacency_list[index],index)
            index +=1