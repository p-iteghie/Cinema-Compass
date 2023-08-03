import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import imdb
from pyvis.network import Network

st.set_page_config(page_title="Cinema Compass", layout="wide")
df = pd.read_csv("data.csv", encoding='latin-1', dtype={'nconst':object,'primaryName':object,'birthYear':object,'deathYear':object,'primaryProfession':object,'knownForTitles':object}) #convert to github link later
ia = imdb.Cinemagoer()
coworkers = pd.DataFrame()
disableMovie = True
actorList = ["Please choose."]
movieIds = []
movieList = []

if "actor" not in st.session_state:
    st.session_state.actor = "Please choose."

def getMovieNames():
    global movieList,disableMovie,movieIds,coworkers
    curActor = st.session_state.actor
    if curActor == 'Please choose.':
        disableMovie = True
        movieIds = []
        movieList = []
        coworkers = coworkers.iloc[0:0]
    else:
        disableMovie = False
        movieIds = df.loc[df['primaryName'] == curActor, 'knownForTitles':].values.flatten().tolist()
        movieList = []
        #for x in movieIds:
        #    movieList.append(ia.get_movie(x[2:])['title']) #FIXME
        coworkers = df.loc[(df['primaryName'] != curActor) & (df.isin(movieIds).any(axis=1))]
    coworkers
    st.write(movieList) # testing

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

actorNetwork.add_node(1, label=choose_actor) # testing

try: # idk what path should be rn
    path = '/tmp'
    actorNetwork.save_graph(f'{path}/movieGraph.html')
    HtmlFile = open(f'{path}/movieGraph.html', 'r', encoding='utf-8')
except:
    actorNetwork.save_graph('movieGraph.html')
    HtmlFile = open('movieGraph.html', 'r', encoding='utf-8')


components.html(HtmlFile.read(), height=635)