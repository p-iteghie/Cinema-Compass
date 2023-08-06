import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import imdb
import networkx as nx
import time
from pyvis.network import Network
import testing_class as ts
from array_holder import Columns

# initialize all variables and the web app
st.set_page_config(page_title="Cinema Compass", layout="wide", page_icon=":film_projector:", menu_items={'Get Help': None, 'Report a Bug': None, 'About': "Select an actor to run BFS & DFS and display other actors they're connected to."})
df = pd.read_csv("data.csv", encoding='latin-1', dtype={'nconst': object, 'primaryName': object, 'birthYear': object, 'deathYear': object, 'primaryProfession': object, 'knownForTitles': object})
ia = imdb.Cinemagoer()
coworkers = pd.DataFrame()
coworkerList = []
noneChosen = True
actorList = ["Please choose."]
movieIds = []
movieList = []
coworkerDict = {}
bfsArray = []
dfsArray = []
superArray = ts.rebuild_adjacency("adjacencyListFinal.csv")
structure = Columns("data.csv")
bfsTime = 0
dfsTime = 0

if "actor" not in st.session_state:  # add key to session state for web app
    st.session_state.actor = "Please choose."


def getMovieNames():  # gets all the information for the chosen actor
    global movieList, noneChosen, movieIds, coworkers, coworkerList, coworkerDict
    curActor = st.session_state.actor
    if curActor == 'Please choose.':
        noneChosen = True
        movieIds = []
        movieList = []
        coworkers = coworkers.iloc[0:0]
        coworkerList = []
        coworkerDict = {}
    else:
        noneChosen = False
        movieIds = df.loc[df['primaryName'] == curActor, 'knownForTitles':].values.flatten().tolist()
        movieList = []
        for x in movieIds:
            movieList.append(ia.get_movie(x[2:])['title'])
        coworkers = df.loc[(df['primaryName'] != curActor) & (df.isin(movieIds).any(axis=1))]
        coworkerList = [curActor] + coworkers['primaryName'].tolist()
        for y in range(len(coworkerList)):
            coworkerDict[coworkerList[y]] = y


choose_actor = st.sidebar.selectbox(  # the sidebar menu
    "Pick an Actor",
    actorList + df['primaryName'].tolist(),
    key='actor',
    on_change=getMovieNames()
)

actorNetwork = Network(  # initialize the actor graph
    height='600px',
    bgcolor='#181818',
    font_color='white'
    )

# change the physics properties of the actor graph
actorNetwork.set_options('''
const options = {
  "physics": {
    "repulsion": {
      "springConstant": 0.01,
      "nodeDistance": 70
    },
    "minVelocity": 0.75,
    "solver": "repulsion"
  }
}
''')

# write web app's title
if not noneChosen:
    st.title(f"Finding {st.session_state.actor}", anchor=False, help=None)
    st.markdown(f'{st.session_state.actor} has been in _{movieList[0]}_, _{movieList[1]}_, _{movieList[2]}_, and _{movieList[3]}_.')
else:
    st.title(":film_projector: Cinema Compass", anchor=False, help=None)

# create adjacency matrix for the actor and coworker graph
if not noneChosen:
    adjMatrix = np.zeros((len(coworkerDict), len(coworkerDict)), dtype=int)

    for i in range(len(coworkerDict)):
        adjMatrix[0][i] = 1
        adjMatrix[i][0] = 1
    for i in range(len(movieIds)):
        temp = coworkers.loc[(df.isin(movieIds[i:i+1]).any(axis=1))]
        temp.reset_index(inplace=True, drop=True)
        for j in range(len(temp.index)):
            for k in range(len(temp.index)):
                adjMatrix[coworkerDict[temp.loc[j, 'primaryName']]][coworkerDict[temp.loc[k, 'primaryName']]] = 1

    np.fill_diagonal(adjMatrix, 0)  # remove self-loops
    adjDF = pd.DataFrame(adjMatrix)
    nxGraph = nx.from_pandas_adjacency(adjDF)
    actorNetwork.from_nx(nxGraph)

    for key, value in coworkerDict.items():  # add actor name and information to each node
        actorNetwork.get_node(value)['label'] = key
        actorNetwork.get_node(value)['font']['size'] = 10
        actorNetwork.get_node(value)['title'] = ""
        actorNetwork.get_node(value)['color'] = "#59A5D8"
        currIds = df.loc[df['primaryName'] == key, 'knownForTitles':].values.flatten().tolist()
        for i in range(len(currIds)):
            if currIds[i] in movieIds:
                actorNetwork.get_node(value)['title'] += f"{movieList[movieIds.index(currIds[i])]}, "
        actorNetwork.get_node(value)['title'] = actorNetwork.get_node(value)['title'][:-2]
    actorNetwork.get_node(0)['size'] = 25
    actorNetwork.get_node(0)['color'] = "#496F5D"

    startTime = time.process_time()  # time breadth first search
    bfsArray = ts.BFS(superArray, st.session_state.actor, structure.names)
    endTime = time.process_time()
    bfsTime = endTime - startTime

    startTime = time.process_time()  # time depth first search
    dfsArray = ts.DFS(superArray, st.session_state.actor, structure.names)
    endTime = time.process_time()
    dfsTime = endTime - startTime

# access the actor graph as a html file
try:
    path = '/tmp'
    actorNetwork.save_graph(f'{path}/movieGraph.html')
    htmlFile = open(f'{path}/movieGraph.html', 'r', encoding='utf-8')
except:
    actorNetwork.save_graph('movieGraph.html')
    htmlFile = open('movieGraph.html', 'r', encoding='utf-8')

# display the actor graph and outcomes of both search algorithms
components.html(htmlFile.read(), height=635)
bfsCol, dfsCol = st.columns(2)

with bfsCol:
    st.header("Breadth First Search", anchor=False, help=None)
    if not noneChosen:
        if len(bfsArray) == 1:
            text = "actor"
        else:
            text = "actors"
        st.caption(f"To find {st.session_state.actor} from Fred Astaire with BFS, it took {len(bfsArray):,} {text} and {bfsTime:.5f} seconds.")
        with st.spinner('Loading searched actors...'):
            for i in range(len(bfsArray)):
                st.markdown(str(i + 1) + '. ' + bfsArray[i])
    else:
        st.markdown("Waiting for choice.")

with dfsCol:
    st.header("Depth First Search", anchor=False, help=None)
    if not noneChosen:
        if len(dfsArray) == 1:
            text = "actor"
        else:
            text = "actors"
        st.caption(f"To find {st.session_state.actor} from Fred Astaire with DFS, it took {len(dfsArray):,} {text} and {dfsTime:.5f} seconds.")
        with st.spinner('Loading searched actors...'):
            for i in range(len(dfsArray)):
                st.markdown(str(i+1) + '. ' + dfsArray[i])
        st.toast(":white_check_mark: Finished!")
    else:
        st.markdown("Waiting for choice.")
