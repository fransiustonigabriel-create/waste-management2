import streamlit as st

st.set_page_config(page_title="AI Waste Predictor", page_icon="♻️", layout="wide")

dashboard  = st.Page("dashboard.py",  title="Interactive Dashboard", icon="📊", default=True)
armada     = st.Page("armada.py",     title="Armada Management",     icon="🚛")
simulator  = st.Page("simulator.py",  title="Event Simulator",       icon="🎛️")
map_route  = st.Page("map_route.py",  title="Rute Armada",           icon="🗺️")
chatbot    = st.Page("chatbot.py",   title="AI Assistant",          icon="🤖")

pg = st.navigation([dashboard, armada, simulator, map_route, chatbot])
pg.run()    