import streamlit as st
import time
from datetime import datetime
import os
from PIL import Image
import io
import json
import streamlit.components.v1 as components
from pathlib import Path


def overlay_images(background_path, overlays, position=(0, 0), opacity=1.0):
    try:
        background = Image.open(background_path).convert("RGBA")
    except:
        background = background_path
    overlay = overlays.convert("RGBA")
    if overlay.size[0] > background.size[0] or overlay.size[1] > background.size[1]:
        overlay.thumbnail((background.size[0], background.size[1]))
    if opacity < 1.0:
        overlay = Image.blend(
            Image.new("RGBA", overlay.size, (0, 0, 0, 0)), overlay, opacity
        )
    background.paste(overlay, position, overlay)
    return background


def enlarge_photo(pic):
    img = Image.open(pic)
    new_size = (460, 345)
    # resized_img = img.resize(new_size, Image.LANCZOS) # or Image.BICUBIC, Image.NEAREST
    resized_img = img.resize(new_size, Image.BICUBIC)  # or Image.BICUBIC, Image.NEAREST
    return resized_img


head = Path(__file__).parent if "__file__" in globals() else Path.cwd()
blank = "media/Filmstrip-High-Quality-PNG.png"
col1, col2 = st.columns(2)
with col1:
    st.title(":blue[Photobooth] 📸")
with col2:
    components.html(
        f"""
<script src="https://unpkg.com/@dotlottie/player-component@2.7.12/dist/dotlottie-player.mjs" type="module"></script>
<dotlottie-player src="https://lottie.host/0e663cc0-d5f9-40cb-a659-3954800ab47b/AN3L3IdG0I.lottie" background="transparent" speed="1" style="width: 300px; height: 300px" loop autoplay></dotlottie-player>
    """,
        height=300,
    )
st.markdown("⚠️ Needs review")
enable = st.checkbox("Enable camera")

c1, c2, c3, c4 = st.columns(4)
colList = [c1, c2, c3, c4]

pics = {}
p1, p2 = st.columns(2)
p3, p4 = st.columns(2)
pList = [p1, p2, p3, p4]
for x in range(4):
    with pList[x]:
        picture = st.camera_input(
            f"Take a picture: {x+1}", disabled=not enable, key="pic" + f"{x+1}"
        )
        if picture:
            with colList[x]:
                st.image(picture)
                pics[x + 1] = picture

if st.button("Prepare Photostrip!"):
    with st.status("Preparing photos...", expanded=True) as status:
        st.write("Searching for photos...")
        time.sleep(2)
        st.write("Found photos.")
        time.sleep(1)
        st.write("Preparing photos...")
        time.sleep(1)
        status.update(label="Preparation complete!", state="complete", expanded=False)

    finalpic1 = overlay_images(
        os.path.join(head, blank), enlarge_photo(pics[1]), position=(100, 50)
    )
    finalpic2 = overlay_images(finalpic1, enlarge_photo(pics[2]), position=(100, 435))
    finalpic3 = overlay_images(finalpic2, enlarge_photo(pics[3]), position=(100, 820))
    finalpic4 = overlay_images(finalpic3, enlarge_photo(pics[4]), position=(100, 1205))
    buffer = io.BytesIO()
    finalpic4.save(buffer, format="PNG")
    buffer.seek(0)

    st.download_button(
        label="Download Photostrip",
        data=buffer,
        file_name="Photostrip_" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".jpg",
        type="primary",
    )