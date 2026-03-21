# main.py
# Day 7 - Calculate distance between thumb and index finger

import cv2
import mediapipe as mp
import numpy as np
import time

# --- MediaPipe Setup ---
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    max_num_hands=1
)

# --- Webcam Setup ---
cap = cv2.VideoCapture(0)
prev_time = 0

print("Hand tracking started. Press 'q' to quit.")
print("Watch the Distance value — note min and max as you move fingers!")

while True:
    success, frame = cap.read()

    if not success:
        print("Failed to grab frame")
        break

    # Convert BGR to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Run hand detection
    results = hands.process(rgb_frame)

    # Get frame dimensions
    h, w, _ = frame.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            # Draw all 21 landmarks
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # --- Extract Thumb Tip (Landmark 4) ---
            thumb_tip = hand_landmarks.landmark[4]
            thumb_x = int(thumb_tip.x * w)
            thumb_y = int(thumb_tip.y * h)

            # --- Extract Index Finger Tip (Landmark 8) ---
            index_tip = hand_landmarks.landmark[8]
            index_x = int(index_tip.x * w)
            index_y = int(index_tip.y * h)

            # --- Draw circles on both fingertips ---
            cv2.circle(frame, (thumb_x, thumb_y), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (index_x, index_y), 15, (255, 0, 255), cv2.FILLED)

            # --- Draw line between fingertips ---
            cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), (255, 0, 255), 3)

            # --- Calculate Euclidean Distance ---
            # This is the straight line distance between the two points
            # numpy's sqrt is cleaner than Python's math.sqrt for this
            distance = np.sqrt(
                (index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2
            )

            # Convert to integer so it displays cleanly
            distance = int(distance)

            # --- Display distance on screen ---
            cv2.putText(
                frame,
                f"Distance: {distance} px",
                (10, 70),                     # Below the FPS counter
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 0),                # Yellow color
                2
            )

            # Also print to terminal so we can observe the range
            print(f"Distance: {distance}px")

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