import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
from PIL import Image

st.set_page_config(page_title="AITED Demo", layout="wide")

# SESSION
if "scanning" not in st.session_state:
    st.session_state.scanning = False

if "result" not in st.session_state:
    st.session_state.result = None

# LOAD IMAGE
def load_image():
    img = Image.open("sample_ultrasound.jpg").convert("L")
    return np.array(img)

# LOCATION
def get_location(x, y, h, w):
    vertical = "Upper" if x < h/3 else "Middle" if x < 2*h/3 else "Lower"
    horizontal = "Left" if y < w/3 else "Center" if y < 2*w/3 else "Right"
    return f"{vertical} {horizontal}"

# UI
st.sidebar.title("🧠 AITED DEMO")
page = st.sidebar.radio("Menu", ["Dashboard", "Scan"])

# DASHBOARD
if page == "Dashboard":
    st.title("📊 System Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Scans", "128")
    c2.metric("High Risk", "32")
    c3.metric("Normal", "76")

    st.line_chart([30, 45, 60, 55, 82])

# SCAN
elif page == "Scan":
    st.title("🔍 Ultrasound Scan")

    if st.button("▶ Start Scan"):
        st.session_state.scanning = True
        st.session_state.result = None

    if st.session_state.scanning:
        progress = st.progress(0)

        for i in range(100):
            time.sleep(0.01)
            progress.progress(i+1)

        st.success("Scan Complete")
        st.session_state.scanning = False

        img = load_image()
        h, w = img.shape

        # สุ่มตำแหน่งก้อน (demo)
        x = random.randint(int(h*0.3), int(h*0.7))
        y = random.randint(int(w*0.3), int(w*0.7))
        r = random.randint(20, 40)

        location = get_location(x, y, h, w)

        # plot
        fig, ax = plt.subplots()
        ax.imshow(img, cmap='gray')

        circle = plt.Circle((y, x), r, color='red', fill=False, linewidth=2)
        ax.add_patch(circle)

        ax.axis('off')
        st.pyplot(fig)

        # AI result (ดูสมจริง)
        risk = random.randint(60, 90)

        st.session_state.result = {
            "risk": risk,
            "location": location,
            "x": x,
            "y": y
        }

    # RESULT
    if st.session_state.result:
        r = st.session_state.result

        st.metric("Risk Score", f"{r['risk']}%")
        st.error("⚠️ Suspicious")

        st.subheader("📍 Tumor Location")
        st.write(f"Region: {r['location']}")
        st.write(f"Coordinates: X={r['x']} , Y={r['y']}")
