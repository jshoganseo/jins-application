import streamlit as st
import time
from pathlib import Path
import streamlit.components.v1 as components


head = Path(__file__).parent if "__file__" in globals() else Path.cwd()
calendar_tail = "quickstart.py"
monthly_tail = "monthly_survey.py"
photo_tail = "photobooth.py"
jingpt_tail = "jingpt.py"
gallery_tail = "photo_gallery.py"
contact_tail = "contact_us.py"
song_tail = head / "media/LE SSERAFIM Perfect Night 8bit.mp3"
side_logo = head / "media/Cool Text - 480148577890494.png"

# --- SESSION STATE INIT ---
for key, default in [("current_page", "Home 🏠"), 
                     ("animation_done", False),
                     ("logged_in", False),
                     ("login_clicked", False)]:
    if key not in st.session_state:
        st.session_state[key] = default

# --- LOGIN FUNCTION ---
def login():
    st.title("🔐 Please Sign In")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            valid_username = st.secrets["credentials"]["username"]
            valid_password = st.secrets["credentials"]["password"]

            if username == valid_username and password == valid_password:
                st.session_state.logged_in = True
                st.session_state.login_clicked = True  # flag to trigger app rerender
            else:
                st.error("Invalid username or password ❌")

# --- PAGE LOADER ---
def load_page(file_name):
    path = head / file_name
    if path.exists():
        exec(path.read_text(), {"st": st, "__name__": "__main__"})
    else:
        st.error(f"Page not found: {file_name}")

# --- STARTUP PAGE ---
def startup():
    heading = "Welcome to your Application :sunflower:"
    st.title(":blue[✨Happy Birthday Jin!✨] 🎂")

    if not st.session_state.animation_done:
        placeholder = st.empty()
        for word in heading.split(" "):
            placeholder.markdown(word + " ")
            time.sleep(0.3)
        st.session_state.animation_done = True
    else:
        st.markdown(heading)

    st.balloons()

    if song_tail.exists():
        with open(str(song_tail), "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")
    else:
        st.warning("Song file not found.")

    components.html(
        """
        <script src="https://unpkg.com/@dotlottie/player-component@2.7.12/dist/dotlottie-player.mjs" type="module"></script>
        <dotlottie-player src="https://lottie.host/97aa93a3-c078-4e62-91b2-562a11a10328/ZtQw271y7L.lottie" 
                          background="transparent" speed="1" style="width: 300px; height: 300px" loop autoplay></dotlottie-player>
        """,
        height=300,
    )

    st.markdown(st.secrets["credentials"]["surprise"])

# --- PAGES ---
pages = {
    "Home 🏠": startup,
    "Calendar 📆": lambda: load_page(calendar_tail),
    "Monthly Love Survey ✍️": lambda: load_page(monthly_tail),
    "Photobooth 📸": lambda: load_page(photo_tail),
    "JinGPT 💻": lambda: load_page(jingpt_tail),
    "Photo Gallery 🖼️": lambda: load_page(gallery_tail),
    "Contact Us ✉️": lambda: load_page(contact_tail),
}

# --- MAIN APP FUNCTION ---
def main_app():
    st.sidebar.image(str(side_logo), width=200)

    # Sidebar navigation
    st.session_state.current_page = st.sidebar.radio(
        "Go to",
        list(pages.keys()),
        index=list(pages.keys()).index(st.session_state.current_page),
        key="sidebar_radio"
    )

    # Render page
    page_to_render = pages.get(st.session_state.current_page, startup)
    page_to_render()

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.login_clicked = False  # reset flag

# --- ENTRY POINT ---
if st.session_state.logged_in or st.session_state.login_clicked:
    main_app()
else:
    login()
