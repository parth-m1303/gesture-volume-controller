# main.py
# Day 5 - Integrating MediaPipe for hand landmark detection

import cv2
import mediapipe as mp
import time

# --- MediaPipe Setup ---
# mp.solutions.hands gives us the hand tracking model
mp_hands = mp.solutions.hands

# mp.solutions.drawing_utils helps us draw the landmarks on screen
mp_draw = mp.solutions.drawing_utils

# Create the hand detector
# min_detection_confidence: how confident it must be before saying "I see a hand"
# max_num_hands: we only need to track 1 hand for our project
hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    max_num_hands=1
)

# --- Webcam Setup ---
cap = cv2.VideoCapture(0)
prev_time = 0

print("Hand tracking started. Press 'q' to quit.")

while True:
    success, frame = cap.read()

    if not success:
        print("Failed to grab frame")
        break

    # MediaPipe only works with RGB images
    # But OpenCV gives us BGR images by default
    # So we must convert before passing to MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Pass the RGB frame into MediaPipe for hand detection
    results = hands.process(rgb_frame)

    # Check if any hands were detected
    if results.multi_hand_landmarks:
        # Loop through each detected hand (we set max to 1, but good habit)
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw all 21 landmarks and the connections between them
            mp_draw.draw_landmarks(
                frame,                        # Draw on original BGR frame
                hand_landmarks,               # The landmark data
                mp_hands.HAND_CONNECTIONS     # Lines connecting the landmarks
            )

    # --- FPS Counter ---
    current_time = time.time()
    fps = int(1 / (current_time - prev_time))
    prev_time = current_time

    cv2.putText(frame, f"FPS: {fps}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Webcam released.")