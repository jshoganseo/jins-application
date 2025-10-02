import streamlit as st
import os 
from pathlib import Path


head = Path(__file__).parent if "__file__" in globals() else Path.cwd()
st.title(":blue[*~ Our Journey Thus Far ~*]")
st.markdown("Redacted for privacy reasons.")
'''
files = []
for file in os.listdir(os.path.join(head, 'photo_gallery')):
    files.append(os.path.join(os.path.join(head, 'photo_gallery'),file))

row1 = st.columns(6)
row2 = st.columns(6)
row3 = st.columns(6)
row4 = st.columns(6)
row5 = st.columns(6)
rows = [row1, row2, row3, row4, row5]

x = 0
for row in rows:
    for col in row:
        with col:
            try:
                st.image(files[x])
            except:
                pass
        x+=1
'''