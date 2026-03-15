# main.py
# Day 3 - Testing webcam capture with OpenCV

import cv2

# Start webcam (0 = default camera)
cap = cv2.VideoCapture(0)

print("Webcam started. Press 'q' to quit.")

while True:
    # Read a frame from the webcam
    success, frame = cap.read()

    # If the frame wasn't captured properly, stop
    if not success:
        print("Failed to grab frame")
        break

    # Show the frame in a window on screen
    cv2.imshow("Webcam Test", frame)

    # Wait for a key press. If 'q' is pressed, quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
print("Webcam released.")