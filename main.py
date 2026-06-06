import cv2
import math
import time
import numpy as np
from config import FRAME_WIDTH, FRAME_HEIGHT, MIN_DISTANCE, MAX_DISTANCE
from hand_tracker import HandTracker
from brightness_controller import BrightnessController

tracker = HandTracker()
bc = BrightnessController()


def draw_hud(frame, brightness, fps, hand_detected):
    h, w = frame.shape[:2]

    bar_x, bar_y, bar_w, bar_h = 30, 100, 24, 300
    filled = int(bar_h * brightness / 100)
    cv2.rectangle(frame, (bar_x, bar_y),
                  (bar_x + bar_w, bar_y + bar_h), (50, 50, 50), 2)
    cv2.rectangle(frame, (bar_x, bar_y + bar_h - filled),
                  (bar_x + bar_w, bar_y + bar_h),
                  (0, 255, 200), cv2.FILLED)

    cv2.putText(frame, f"{int(brightness)}%",
                (bar_x - 2, bar_y + bar_h + 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 200), 2)

    cv2.putText(frame, "Brightness",
                (bar_x - 5, bar_y - 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)

    cv2.putText(frame, f"FPS: {int(fps)}",
                (w - 110, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 100), 2)

    status_color = (0, 255, 100) if hand_detected else (0, 100, 255)
    status_text = "Hand: Detected" if hand_detected else "Hand: None"
    cv2.putText(frame, status_text, (w - 180, h - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, status_color, 1)

    cv2.putText(frame, "Pinch to control brightness",
                (w // 2 - 130, h - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)

    return frame


def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    prev_time = 0
    brightness = 50.0

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        frame = tracker.find_hands(frame)
        landmarks = tracker.get_landmark_positions(frame)

        hand_detected = len(landmarks) >= 9

        if landmarks:
            thumb = landmarks[4]
            index = landmarks[8]
            distance = math.hypot(index[0] - thumb[0],
                                  index[1] - thumb[1])
            brightness = float(np.interp(distance,
                                         [MIN_DISTANCE, MAX_DISTANCE],
                                         [0, 100]))
            bc.set_target(brightness)

            cv2.line(frame, thumb, index, (0, 255, 255), 2)
            cv2.circle(frame, thumb, 10, (255, 0, 200), cv2.FILLED)
            cv2.circle(frame, index, 10, (255, 0, 200), cv2.FILLED)
            mid = ((thumb[0] + index[0]) // 2,
                   (thumb[1] + index[1]) // 2)
            cv2.circle(frame, mid, 7, (0, 255, 100), cv2.FILLED)

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time + 1e-6)
        prev_time = curr_time

        frame = draw_hud(frame, brightness, fps, hand_detected)

        cv2.imshow("Brightness Control", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    bc.stop()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()