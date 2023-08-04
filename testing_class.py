from adjacency_list_handler import CSV_handle
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import imdb
import networkx as nx
from matplotlib import pyplot as plt
from pyvis.network import Network

nxGraph = nx.read_adjlist("adjacency_list5.csv") #MUST SAVE AS CSV (Macintosh) TRY THIS IF CODE NO WORK
nx.draw(nxGraph, with_labels=True, node_size=100, alpha=1, linewidths=10)

plt.show()
#new_object = CSV_handle("data.csv")
