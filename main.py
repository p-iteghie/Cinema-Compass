import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import imdb
import networkx as nx
from pyvis.network import Network

st.set_page_config(page_title="Cinema Compass", layout="wide")
df = pd.read_csv("data.csv", encoding='latin-1', dtype={'nconst':object,'primaryName':object,'birthYear':object,'deathYear':object,'primaryProfession':object,'knownForTitles':object}) #convert to github link later
ia = imdb.Cinemagoer()
coworkers = pd.DataFrame()
coworkerList = []
disableMovie = True
actorList = ["Please choose."]
movieIds = []
movieList = []

if "actor" not in st.session_state:
    st.session_state.actor = "Please choose."

def getMovieNames():
    global movieList,disableMovie,movieIds,coworkers,coworkerList
    curActor = st.session_state.actor
    if curActor == 'Please choose.':
        disableMovie = True
        movieIds = []
        movieList = []
        coworkers = coworkers.iloc[0:0]
        coworkerList = []
    else:
        disableMovie = False
        movieIds = df.loc[df['primaryName'] == curActor, 'knownForTitles':].values.flatten().tolist()
        movieList = []
        #for x in movieIds:
        #    movieList.append(ia.get_movie(x[2:])['title']) #FIXME
        coworkers = df.loc[(df['primaryName'] != curActor) & (df.isin(movieIds).any(axis=1))]
        coworkerList = [curActor] + coworkers['primaryName'].tolist()
    coworkers
    st.write(movieIds) # testing

choose_actor = st.sidebar.selectbox(
    "Pick an Actor",
    actorList + df['primaryName'].tolist(),
    key='actor',
    on_change=getMovieNames()
)

actorNetwork = Network(
    height='600px',
    bgcolor='#181818',
    font_color='white'
    )

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


coworkerDict = {} # we can make the adjacency matrix using only numbers with this dictionary

for i in range(len(coworkerList)):
    coworkerDict[coworkerList[i]] = i

st.write(coworkerDict)
adjMatrix = np.zeros((len(coworkerDict),len(coworkerDict)), dtype=int)

for i in range(len(coworkerDict)):
    adjMatrix[0][i] = 1
    adjMatrix[i][0] = 1
for i in range(len(movieIds)):
    temp = coworkers.loc[(df.isin(movieIds[i:i+1]).any(axis=1))]
    temp.reset_index(inplace=True,drop=True)
    #FIXME maybe add column that has the titles of the common movies so that it can be later added to the nodes' titles
    temp #delete later
    for j in range(len(temp.index)):
        for k in range(len(temp.index)):
            adjMatrix[coworkerDict[temp.loc[j, 'primaryName']]][coworkerDict[temp.loc[k, 'primaryName']]] = 1
np.fill_diagonal(adjMatrix, 0)
adjDF = pd.DataFrame(adjMatrix)
nxGraph = nx.from_pandas_adjacency(adjDF)
actorNetwork.from_nx(nxGraph)
#actorNetwork.get_node(0)['size']=20 #FIXME needs to run only if it exists
for key, value in coworkerDict.items():
    actorNetwork.get_node(value)['label'] = key
    actorNetwork.get_node(value)['font']['size'] = 10

#person = ia.get_person(df.loc[df['primaryName'] == st.session_state.actor, 'nconst'].values.flatten().tolist()[0][2:])
#st.write(person['headshot'])

try: # idk what path should be rn
    path = '/tmp'
    actorNetwork.save_graph(f'{path}/movieGraph.html')
    HtmlFile = open(f'{path}/movieGraph.html', 'r', encoding='utf-8')
except:
    actorNetwork.save_graph('movieGraph.html')
    HtmlFile = open('movieGraph.html', 'r', encoding='utf-8')


components.html(HtmlFile.read(), height=635)