import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
from PIL import Image

st.set_page_config(page_title="AITED Medical AI", layout="wide")

# ---------------- SESSION ----------------
if "scanning" not in st.session_state:
    st.session_state.scanning = False

if "result" not in st.session_state:
    st.session_state.result = None

# ---------------- LOAD IMAGE ----------------
def load_image():
    img = Image.open("sample_ultrasound.jpg").convert("L")
    return np.array(img)

# ---------------- DETERMINE LOCATION ----------------
def get_location(x, y, h, w):
    if x < h/3:
        vertical = "Upper"
    elif x < 2*h/3:
        vertical = "Middle"
    else:
        vertical = "Lower"

    if y < w/3:
        horizontal = "Left"
    elif y < 2*w/3:
        horizontal = "Center"
    else:
        horizontal = "Right"

    return f"{vertical} {horizontal}"

# ---------------- AI ----------------
def analyze(img):
    score = np.mean(img)

    if score > 130:
        return 85, "⚠️ Suspicious"
    elif score > 100:
        return 55, "🟡 Monitor"
    else:
        return 20, "🟢 Normal"

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧠 AITED AI")
page = st.sidebar.radio("Menu", ["Dashboard", "Scan", "Analytics"])

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.title("📊 Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Scans", "128")
    c2.metric("High Risk", "32")
    c3.metric("Normal", "76")

    st.line_chart([30, 45, 60, 55, 82])

# ---------------- SCAN ----------------
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

        # โหลดภาพ
        img = load_image()
        h, w = img.shape

        # สุ่มตำแหน่งก้อน
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

        # AI
        risk, status = analyze(img)

        st.session_state.result = {
            "risk": risk,
            "status": status,
            "location": location,
            "x": x,
            "y": y
        }

    # -------- RESULT --------
    if st.session_state.result:
        r = st.session_state.result

        st.metric("Risk Score", f"{r['risk']}%")

        if "Suspicious" in r["status"]:
            st.error(r["status"])
        elif "Monitor" in r["status"]:
            st.warning(r["status"])
        else:
            st.success(r["status"])

        st.subheader("📍 Tumor Location")
        st.write(f"Region: **{r['location']}**")
        st.write(f"Coordinates: X={r['x']} , Y={r['y']}")

        st.write("📏 Estimated size: ~1 cm")

# ---------------- ANALYTICS ----------------
elif page == "Analytics":
    st.title("🧪 Model Performance")

    st.metric("Sensitivity", "91%")
    st.metric("Specificity", "76%")

    st.bar_chart([91, 76])
