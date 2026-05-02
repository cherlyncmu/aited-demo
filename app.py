import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
from PIL import Image
import cv2
from ultralytics import YOLO

st.set_page_config(page_title="AITED AI Detection", layout="wide")

# โหลดโมเดล
model = YOLO("yolov8n.pt")

# ---------------- SESSION ----------------
if "scanning" not in st.session_state:
    st.session_state.scanning = False

if "result" not in st.session_state:
    st.session_state.result = None

# ---------------- LOAD IMAGE ----------------
def load_image():
    img = Image.open("sample_ultrasound.jpg").convert("RGB")
    return np.array(img)

# ---------------- LOCATION ----------------
def get_location(cx, cy, h, w):
    vertical = "Upper" if cy < h/3 else "Middle" if cy < 2*h/3 else "Lower"
    horizontal = "Left" if cx < w/3 else "Center" if cx < 2*w/3 else "Right"
    return f"{vertical} {horizontal}"

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧠 AITED AI")
page = st.sidebar.radio("Menu", ["Scan"])

# ---------------- SCAN ----------------
if page == "Scan":
    st.title("🔍 AI Tumor Detection")

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
        h, w, _ = img.shape

        # -------- AI DETECT --------
        results = model(img)

        boxes = results[0].boxes

        fig, ax = plt.subplots()
        ax.imshow(img)

        detections = []

        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                conf = float(box.conf[0])

                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                loc = get_location(cx, cy, h, w)

                # วาดกรอบ
                rect = plt.Rectangle(
                    (x1, y1), x2-x1, y2-y1,
                    linewidth=2, edgecolor='red', facecolor='none'
                )
                ax.add_patch(rect)

                ax.text(x1, y1-5, f"{conf:.2f}",
                        color='red', fontsize=10)

                detections.append({
                    "conf": conf,
                    "location": loc,
                    "cx": cx,
                    "cy": cy
                })

        ax.axis('off')
        st.pyplot(fig)

        st.session_state.result = detections

    # -------- RESULT --------
    if st.session_state.result:
        st.subheader("📊 Detection Result")

        for i, d in enumerate(st.session_state.result):
            st.write(f"### 🔴 Object {i+1}")
            st.write(f"Confidence: {round(d['conf']*100,1)}%")
            st.write(f"Location: {d['location']}")
            st.write(f"Position: X={d['cx']}, Y={d['cy']}")
