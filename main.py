import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import imdb
from pyvis.network import Network

st.set_page_config(page_title="Cinema Compass", layout="wide")
df = pd.read_csv("data.csv", dtype={'nconst':object,'primaryName':object,'birthYear':object,'deathYear':object,'primaryProfession':object,'knownForTitles':object}) #convert to github link later
ia = imdb.Cinemagoer()
disableMovie = True
actorList = ["Please choose."]
movieIds = []
movieList = []

if "actor" not in st.session_state:
    st.session_state.actor = "Please choose."

def getMovieNames():
    global movieList,disableMovie,movieIds
    curActor = st.session_state.actor
    if curActor == 'Please choose.':
        disableMovie = True
        movieList = []
    else:
        disableMovie = False
        df.set_index("primaryName", inplace=True)
        idString = df.loc[curActor:curActor, 'knownForTitles':].values.flatten().tolist()
        movieIds = idString[0].split(",")
        movieList = []
        for x in movieIds:
            movieList.append(ia.get_movie(x[2:])['title'])
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