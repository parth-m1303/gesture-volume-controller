# main.py
# Day 6 - Extract thumb and index fingertip coordinates

import cv2
import mediapipe as mp
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

while True:
    success, frame = cap.read()

    if not success:
        print("Failed to grab frame")
        break

    # Convert BGR to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Run hand detection
    results = hands.process(rgb_frame)

    # Get frame dimensions — we need these to convert
    # landmark percentages into actual pixel positions
    h, w, _ = frame.shape
    # h = height of frame in pixels
    # w = width of frame in pixels
    # _ = number of color channels (3 for BGR) — we don't need this

    # Check if any hand was detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            # Draw all 21 landmarks (same as Day 5)
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # --- Extract Thumb Tip (Landmark 4) ---
            thumb_tip = hand_landmarks.landmark[4]

            # Convert from percentage (0.0-1.0) to actual pixels
            thumb_x = int(thumb_tip.x * w)
            thumb_y = int(thumb_tip.y * h)

            # --- Extract Index Finger Tip (Landmark 8) ---
            index_tip = hand_landmarks.landmark[8]

            # Convert from percentage to actual pixels
            index_x = int(index_tip.x * w)
            index_y = int(index_tip.y * h)

            # --- Draw a circle on Thumb Tip ---
            # cv2.circle(image, center, radius, color, thickness)
            # cv2.FILLED means the circle is filled in (not just outline)
            cv2.circle(frame, (thumb_x, thumb_y), 15, (255, 0, 255), cv2.FILLED)

            # --- Draw a circle on Index Finger Tip ---
            cv2.circle(frame, (index_x, index_y), 15, (255, 0, 255), cv2.FILLED)

            # --- Draw a line between the two fingertips ---
            cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), (255, 0, 255), 3)

            # --- Print coordinates to terminal (for debugging) ---
            # This helps us understand the values we're working with
            print(f"Thumb: ({thumb_x}, {thumb_y}) | Index: ({index_x}, {index_y})")

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