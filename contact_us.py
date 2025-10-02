import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
import time
import os
import streamlit.components.v1 as components
from pathlib import Path


def send_email(sender_email, sender_password, receiver_email, subject, body, attachments):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach files
    for uploaded_file in attachments:
        bytes_data = uploaded_file.read()
        msg.attach(MIMEApplication(bytes_data, Name=uploaded_file.name))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        st.success('Ticket submitted successfully! 🚀')
    except Exception as e:
        st.error(f"Failed to submit ticket: {e}")

head = Path(__file__).parent if "__file__" in globals() else Path.cwd()

# Lottie animation
components.html(
    f"""
<script src="https://unpkg.com/@dotlottie/player-component@2.7.12/dist/dotlottie-player.mjs" type="module"></script>
<dotlottie-player src="https://lottie.host/b521f645-41bd-4a4a-97d0-2534a9d13825/IBILrCCcpe.lottie" background="transparent" speed="1" style="width: 300px; height: 300px" loop autoplay></dotlottie-player>
""",
    height=300,
)

st.title(':blue[*Contact Us*] 💌')
cdt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
sender_email = st.secrets["credentials"]["email"]
sender_password = st.secrets["credentials"]["emailp"]
receiver_email = st.secrets["credentials"]["email"]

subject = st.text_input(label="Subject:", value=f"Jin's Application, {cdt}", disabled=True)
body = st.text_area(':blue[Body]')
uploaded_files = st.file_uploader("", accept_multiple_files=True)

sentiment_options = ["Positive", "Negative"]
selected_sentiment = st.selectbox("Your sentiment:", ["Select..."] + sentiment_options)
if selected_sentiment != "Select...":
    st.markdown(f":blue[You selected:] {selected_sentiment}")

if st.button("Submit Ticket", type='primary'):
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()

    # Append star/sentiment to subject
    final_subject = subject
    if selected_sentiment != "Select...":
        final_subject += f" | Sentiment: {selected_sentiment}"

    send_email(sender_email, sender_password, receiver_email, final_subject, body, uploaded_files)
