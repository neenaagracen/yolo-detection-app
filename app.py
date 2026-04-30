import streamlit as st
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
import sqlite3
import hashlib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="YOLO Detection App", layout="wide")

# ---------------- DATABASE ----------------
def connect_db():
    return sqlite3.connect("database.db")

def create_user_table():
    conn = connect_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?)",
              (username, hash_password(password)))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    data = c.fetchall()
    conn.close()
    return data

create_user_table()

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")   # ensure this file exists

model = load_model()

# ---------------- DETECTION ----------------
def detect_frame(frame):
    results = model(frame)
    return results[0].plot(), results

def detect_image(image):
    results = model(image)
    return results[0].plot(), results

def calculate_metrics(results):
    detections = []
    for r in results:
        for box in r.boxes:
            detections.append(float(box.conf))

    if len(detections) == 0:
        return {"message": "No objects detected"}

    return {
        "total_objects": len(detections),
        "avg_confidence": round(sum(detections)/len(detections), 3)
    }

# ---------------- SESSION STATE INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- MENU ----------------
menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- REGISTER ----------------
if choice == "Register":
    st.title("Register")

    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        register_user(user, password)
        st.success("Account created successfully!")

# ---------------- LOGIN ----------------
elif choice == "Login":
    st.title("Login")

    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(user, password):
            st.session_state.logged_in = True
            st.session_state.user = user
        else:
            st.error("Invalid Username or Password")

# ---------------- AFTER LOGIN ----------------
if st.session_state.logged_in:

    st.success(f"Welcome {st.session_state.user}")

    option = st.selectbox(
        "Detection Mode",
        ["Webcam", "Image Upload", "Video Upload"]
    )

    # ================= WEBCAM =================
    if option == "Webcam":
        st.subheader("📷 Live Webcam Detection")

        if st.button("Start Camera"):
            cap = cv2.VideoCapture(0)
            stframe = st.empty()

            for i in range(200):  # safe loop
                ret, frame = cap.read()

                if not ret:
                    st.error("Camera not working")
                    break

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                annotated, results = detect_frame(frame)

                stframe.image(annotated)

            cap.release()

    # ================= IMAGE =================
    elif option == "Image Upload":
        st.subheader("🖼 Image Detection")

        file = st.file_uploader(
            "Upload Image",
            type=["jpg", "jpeg", "png"]
        )

        if file is not None:
            image = Image.open(file)
            img_np = np.array(image)

            result_img, results = detect_image(img_np)

            st.image(result_img, caption="Detected Image")

            metrics = calculate_metrics(results)

            st.write("### 📊 Detection Summary")
            st.json(metrics)

    # ================= VIDEO =================
    elif option == "Video Upload":
        st.subheader("🎥 Video Detection")

        video_file = st.file_uploader(
            "Upload Video",
            type=["mp4", "avi", "mov"]
        )

        if video_file is not None:
            with open("temp.mp4", "wb") as f:
                f.write(video_file.read())

            cap = cv2.VideoCapture("temp.mp4")
            stframe = st.empty()

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                annotated, _ = detect_frame(frame)
                stframe.image(annotated)

            cap.release()