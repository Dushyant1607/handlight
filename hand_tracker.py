import cv2
import mediapipe as mp
from config import MIN_DETECTION_CONFIDENCE, MIN_TRACKING_CONFIDENCE, MAX_HANDS


class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_styles = mp.solutions.drawing_styles
        self.results = None                               

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=MAX_HANDS,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
        )

    def find_hands(self, frame, draw=True):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        self.results = self.hands.process(rgb)
        rgb.flags.writeable = True

        if draw and self.results.multi_hand_landmarks:
            for hand_lm in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_lm,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_styles.get_default_hand_landmarks_style(),
                    self.mp_styles.get_default_hand_connections_style(),
                )
        return frame

    def get_landmark_positions(self, frame):             
        h, w, _ = frame.shape
        positions = []

        if self.results and self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            for lm in hand.landmark:
                positions.append((int(lm.x * w), int(lm.y * h)))

        return positions  # positions[4] = thumb tip, positions[8] = index tip