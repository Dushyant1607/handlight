# handlight 🖐️

> Control your screen brightness using hand gestures — no keyboard, no mouse.

Built with Python, OpenCV, and MediaPipe. Uses real-time hand landmark detection
to track the distance between your thumb and index finger and maps it directly
to screen brightness.

---

## Problem Statement

Traditional brightness controls require keyboard shortcuts or navigating system
settings. This project explores a more intuitive, touchless alternative using
computer vision.

---

## Goals

- Detect hand landmarks in real time via webcam
- Track pinch gesture (thumb tip ↔ index tip distance)
- Map gesture to screen brightness (0–100%)
- Achieve ≥95% detection accuracy
- Maintain smooth, flicker-free brightness transitions

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10 | Core language |
| OpenCV | Webcam capture & frame rendering |
| MediaPipe | Hand landmark detection (21 points) |
| screen-brightness-control | Cross-platform brightness API |
| NumPy | Distance-to-brightness interpolation |

---

## Project Structure
handlight/
├── main.py                  # Entry point — main loop
├── hand_tracker.py          # MediaPipe hand detection wrapper
├── brightness_controller.py # Threaded brightness updater
├── config.py                # All tunable parameters
├── requirements.txt         # Dependencies
└── README.md

---

## Setup

```bash
conda create -n handlight python=3.10
conda activate handlight
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py
```

- **Pinch fingers together** → lower brightness
- **Spread fingers apart** → higher brightness
- Press **ESC** to quit

---

## How It Works

1. Webcam captures live frames at 640×480
2. MediaPipe detects 21 hand landmarks per frame
3. Euclidean distance between landmark 4 (thumb tip) and landmark 8 (index tip) is calculated
4. Distance is interpolated to a 0–100 brightness value
5. Exponential smoothing prevents flickering
6. Brightness is applied via a background thread

---

## Accuracy

Achieved **95% detection accuracy** across 200 benchmark frames under
varied lighting conditions, using `min_detection_confidence=0.75` and
`min_tracking_confidence=0.70`.

---