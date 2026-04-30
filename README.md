# Streamlit YOLO Object Detection App

## Description

This project is a web-based application built using Streamlit and YOLOv8 for real-time object detection. It allows users to detect objects using webcam, uploaded images, and videos.

---

## Features

* User Login and Registration (SQLite)
* Live Webcam Object Detection
* Image Upload Detection
* Video Upload Detection
* Bounding boxes with labels and confidence scores
* Detection summary (total objects and average confidence)

---

## Technologies Used

* Python
* Streamlit
* OpenCV
* YOLOv8 (Ultralytics)
* SQLite

---

## How to Run

1. Install required libraries:
   pip install -r requirements.txt

2. Run the application:
   streamlit run app.py

---

## Project Structure

project/
│── app.py
│── auth.py
│── database.db
│── yolov8n.pt
│── requirements.txt
│── README.md
│── images/

---

## Screenshots

### Login Page

![Login](images/login.png)

### Register Page

![Register](images/register.png)

### Webcam Detection

![Webcam](images/webcam.png)

### Image Detection

![Image](images/image_detection.png)

### Video Detection

![Video](images/video_detection.png)

---

## Output

* Real-time detection using webcam
* Detection on images and videos
* Displays bounding boxes with labels and confidence
* Provides detection summary

---

## Conclusion

This project demonstrates the integration of deep learning (YOLOv8) with a web interface (Streamlit) to perform real-time object detection.

---

## Author

* Your Name
