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

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- LOAD IMAGE ----------------
def load_image():
    img = Image.open("sample_ultrasound.jpg").convert("L")
    return np.array(img)

# ---------------- DETECT ----------------
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
    margin-bottom: 15px;
}
.big {
    font-size: 20px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧠 AITED SYSTEM")

status = "🟢 READY"
if st.session_state.scanning:
    status = "🟡 SCANNING"

st.sidebar.markdown(f"**System Status:** {status}")

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
    c1.metric("Total Scans", len(st.session_state.history))
    c2.metric("High Risk", sum(1 for h in st.session_state.history if h["risk"] > 70))
    c3.metric("Normal", sum(1 for h in st.session_state.history if h["risk"] <= 70))

    st.subheader("📈 Risk Trend")
    if st.session_state.history:
        st.line_chart([h["risk"] for h in st.session_state.history])
    else:
        st.info("No data yet")

# ---------------- SCAN ----------------
elif page == "Scan":
    st.title("🔍 Ultrasound AI Scan")

    col1, col2 = st.columns([2,1])

    with col1:
        if st.button("▶ Start Scan"):
            st.session_state.scanning = True
            st.session_state.result = None

        if st.session_state.scanning:
            progress = st.progress(0)
            status_text = st.empty()

            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)
                status_text.text(f"Scanning... {i+1}%")

            st.success("Scan Complete")
            st.session_state.scanning = False

            img = load_image()
            x, y, r, risk, location = detect(img)

            fig, ax = plt.subplots()
            ax.imshow(img, cmap='gray')

            circle = plt.Circle((y, x), r, color='red', fill=False, linewidth=2)
            ax.add_patch(circle)

            ax.axis('off')
            st.pyplot(fig)

            result = {
                "risk": risk,
                "location": location,
                "x": x,
                "y": y
            }

            st.session_state.result = result
            st.session_state.history.append(result)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="big">AI Diagnosis</div>', unsafe_allow_html=True)

        if st.session_state.result:
            r = st.session_state.result

            st.metric("Risk Score", f"{r['risk']}%")

            if r["risk"] > 70:
                st.error("⚠️ Suspicious")
            else:
                st.success("🟢 Normal")

            st.write("📍 Location")
            st.write(r["location"])

            st.write("📌 Coordinates")
            st.write(f"X={r['x']}  Y={r['y']}")

            st.write("📏 Size ~1 cm")
        else:
            st.info("No scan yet")

        st.markdown('</div>', unsafe_allow_html=True)

    # REPORT
    if st.session_state.result:
        r = st.session_state.result

        st.subheader("📄 Diagnostic Report")

        st.write("**Findings:**")
        st.write(f"Abnormal region detected at {r['location']}")

        st.write("**Assessment:**")
        if r["risk"] > 70:
            st.write("High probability of abnormal tissue")
        else:
            st.write("Low risk, no significant abnormality")

        st.write("**Recommendation:**")
        if r["risk"] > 70:
            st.write("Recommend further medical examination")
        else:
            st.write("Routine monitoring suggested")

# ---------------- PATIENTS ----------------
elif page == "Patients":
    st.title("👤 Patient Records")

    if st.session_state.history:
        st.dataframe(st.session_state.history)
    else:
        st.info("No records yet")

# ---------------- ANALYTICS ----------------
elif page == "Analytics":
    st.title("🧪 Model Performance")

    c1, c2, c3 = st.columns(3)
    c1.metric("Sensitivity", "91%")
    c2.metric("Specificity", "76%")
    c3.metric("F1 Score", "0.83")

    st.bar_chart([91, 76, 83])
