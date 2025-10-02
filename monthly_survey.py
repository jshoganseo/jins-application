import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta
import streamlit.components.v1 as components
import time


def time_elapsed(start_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    now = datetime.now()
    diff = relativedelta(now, start)
    return f"{diff.years} years, {diff.months} months"

start_date = "2024-01-14"
title = "Tracking our love life! 💛"

if "survey_started" not in st.session_state:
    st.session_state.survey_started = False
    st.session_state.animation_done = False

components.html(
    """
<script src="https://unpkg.com/@dotlottie/player-component@2.7.12/dist/dotlottie-player.mjs" type="module"></script>
<dotlottie-player src="https://lottie.host/0b88d0b0-55e2-41ac-93a3-d7a81068073d/w64xMKSOay.lottie"
                  background="transparent" speed="1" style="width: 300px; height: 300px" loop autoplay></dotlottie-player>
""",
    height=300,
)

st.markdown(
    st.secrets["credentials"]["2024"]
)
st.divider()
st.markdown(
    st.secrets["credentials"]["2025"]
)
st.divider()

if not st.session_state.survey_started:
    if st.button("Begin Survey"):
        st.session_state.survey_started = True

if st.session_state.survey_started:
    if not st.session_state.animation_done:
        placeholder = st.empty()
        for word in title.split(" "):
            placeholder.markdown(word + " ")
            time.sleep(0.2)
        st.session_state.animation_done = True
    else:
        st.subheader(title)

    google_form_url = st.secrets["credentials"]["survey"]
    components.html(
        f"""
        <iframe src="{google_form_url}" width="100%" height="800" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
        """,
        height=800,
    )
