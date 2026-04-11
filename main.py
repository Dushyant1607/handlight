import cv2
import time
from config import FRAME_WIDTH, FRAME_HEIGHT
from hand_tracker import HandTracker

tracker = HandTracker()

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    prev_time = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)

        frame = tracker.find_hands(frame)

        landmarks = tracker.get_landmark_positions(frame)

        if landmarks:
            print(f"Thumb tip: {landmarks[4]} | Index tip: {landmarks[8]}")

        # FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time + 1e-6)
        prev_time = curr_time
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Brightness Control", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()