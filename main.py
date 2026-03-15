# main.py
# Day 4 - Added FPS counter to webcam feed

import cv2
import time

# Start webcam (0 = default camera)
cap = cv2.VideoCapture(0)

# We need to track time between frames to calculate FPS
# prev_time stores the time of the previous frame
prev_time = 0

print("Webcam started. Press 'q' to quit.")

while True:
    # Read a frame from the webcam
    success, frame = cap.read()

    # If the frame wasn't captured properly, stop
    if not success:
        print("Failed to grab frame")
        break

    # --- FPS Calculation ---
    # Get the current time
    current_time = time.time()

    # FPS = 1 divided by how many seconds passed since last frame
    fps = 1 / (current_time - prev_time)

    # Update prev_time for the next loop
    prev_time = current_time

    # Round FPS to a whole number so it looks clean on screen
    fps = int(fps)

    # Draw the FPS text on the frame
    # cv2.putText(image, text, position, font, size, color, thickness)
    cv2.putText(
        frame,
        f"FPS: {fps}",
        (10, 30),                    # Position: 10px from left, 30px from top
        cv2.FONT_HERSHEY_SIMPLEX,    # Font style
        1,                           # Font size
        (0, 255, 0),                 # Color: Green (in BGR format)
        2                            # Thickness of the text
    )

    # Show the frame in a window on screen
    cv2.imshow("Webcam Test", frame)

    # Wait for a key press. If 'q' is pressed, quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
print("Webcam released.")