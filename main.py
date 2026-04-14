import cv2
import math
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
            thumb = landmarks[4]
            index = landmarks[8]
            distance = math.hypot(index[0] - thumb[0],
                                  index[1] - thumb[1])
            print(f"Distance: {int(distance)}px")

            # Commit b1c2d3 — gesture visuals
            cv2.line(frame, thumb, index, (0, 255, 255), 2)
            cv2.circle(frame, thumb, 10, (255, 0, 200), cv2.FILLED)
            cv2.circle(frame, index, 10, (255, 0, 200), cv2.FILLED)
            mid = ((thumb[0] + index[0]) // 2,
                   (thumb[1] + index[1]) // 2)
            cv2.circle(frame, mid, 7, (0, 255, 100), cv2.FILLED)

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time + 1e-6)
        prev_time = curr_time
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Brightness Control", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()