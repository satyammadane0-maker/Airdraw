import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self, max_num_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )

    def find_hands(self, frame, draw=True):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if results.multi_hand_landmarks and draw:
            for hand in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand,
                    self.mp_hands.HAND_CONNECTIONS,
                )

        return results

    def get_landmarks(self, results, frame_shape):
        if not results.multi_hand_landmarks:
            return None

        hand = results.multi_hand_landmarks[0]
        height, width = frame_shape[:2]

        landmarks = []
        for point in hand.landmark:
            x = max(0, min(width - 1, int(point.x * width)))
            y = max(0, min(height - 1, int(point.y * height)))
            landmarks.append((x, y))

        return landmarks
