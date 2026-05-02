import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
from PIL import Image

st.set_page_config(page_title="AITED Medical System", layout="wide")

# ---------------- SESSION ----------------
if "scanning" not in st.session_state:
    st.session_state.scanning = False

if "result" not in st.session_state:
    st.session_state.result = None

# ---------------- LOAD IMAGE ----------------
def load_image():
    img = Image.open("sample_ultrasound.jpg").convert("L")
    return np.array(img)

# ---------------- SIMULATE DETECTION ----------------
def detect(img):
    h, w = img.shape

    x = random.randint(int(h*0.3), int(h*0.7))
    y = random.randint(int(w*0.3), int(w*0.7))
    r = random.randint(20, 40)

    risk = random.randint(60, 90)

    if x < h/3:
        v = "Upper"
    elif x < 2*h/3:
        v = "Middle"
    else:
        v = "Lower"

    if y < w/3:
        hpos = "Left"
    elif y < 2*w/3:
        hpos = "Center"
    else:
        hpos = "Right"

    location = f"{v} {hpos}"

    return x, y, r, risk, location

# ---------------- STYLE ----------------
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #020617;
}
.card {
    background: #0f172a;
    padding: 20px;
    border-radius: 15px;
}
.big {
    font-size: 20px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧠 AITED SYSTEM")
page = st.sidebar.radio("Menu", [
    "Dashboard",
    "Scan",
    "Patients",
    "Analytics"
])

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.title("📊 System Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Scans", "128", "+12")
    c2.metric("High Risk", "32", "+5")
    c3.metric("Normal", "76", "-3")

    st.subheader("📈 Risk Trend")
    st.line_chart([30, 45, 60, 55, 82])

# ---------------- SCAN ----------------
elif page == "Scan":
    st.title("🔍 Ultrasound AI Scan")

    col1, col2 = st.columns([2,1])

    # -------- LEFT --------
    with col1:
        if st.button("▶ Start Scan"):
            st.session_state.scanning = True
            st.session_state.result = None

        if st.session_state.scanning:
            progress = st.progress(0)
            status = st.empty()

            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)
                status.text(f"Scanning... {i+1}%")

            st.success("Scan Complete")
            st.session_state.scanning = False

            img = load_image()
            x, y, r, risk, location = detect(img)

            fig, ax = plt.subplots()
            ax.imshow(img, cmap='gray')

            # 🔴 วงก้อน
            circle = plt.Circle((y, x), r, color='red', fill=False, linewidth=2)
            ax.add_patch(circle)

            ax.axis('off')
            st.pyplot(fig)

            st.session_state.result = {
                "risk": risk,
                "location": location,
                "x": x,
                "y": y
            }

    # -------- RIGHT --------
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="big">AI Diagnosis</div>', unsafe_allow_html=True)

        if st.session_state.result:
            r = st.session_state.result

            st.metric("Risk Score", f"{r['risk']}%")
            st.error("⚠️ Suspicious")

            st.write("📍 Location")
            st.write(f"{r['location']}")

            st.write("📌 Coordinates")
            st.write(f"X={r['x']}  Y={r['y']}")

            st.write("📏 Size ~1 cm")

        else:
            st.info("No scan yet")

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PATIENTS ----------------
elif page == "Patients":
    st.title("👤 Patient Records")

    st.dataframe({
        "Name": ["John Doe", "Jane Smith"],
        "Last Scan": ["30 Apr", "15 Apr"],
        "Risk": ["82%", "30%"],
        "Status": ["High Risk", "Normal"]
    })

# ---------------- ANALYTICS ----------------
elif page == "Analytics":
    st.title("🧪 Model Performance")

    c1, c2, c3 = st.columns(3)
    c1.metric("Sensitivity", "91%")
    c2.metric("Specificity", "76%")
    c3.metric("F1 Score", "0.83")

    st.bar_chart([91, 76, 83])    st.title("🧪 Model Evaluation")

    st.metric("Sensitivity", "91%")
    st.metric("Specificity", "76%")

    st.bar_chart([91, 76])
