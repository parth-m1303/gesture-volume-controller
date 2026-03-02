# main.py
# Day 3 - Testing webcam capture with OpenCV

import cv2

# Start webcam (0 = default camera)
cap = cv2.VideoCapture(0)

print("Webcam started. Press 'q' to quit.")

while True:
    # Read a frame from webcam
    success, frame = cap.read()

    # If frame wasn't captured, skip
    if not success:
        print("Failed to grab frame")
        break

    # Show the frame in a window
    cv2.imshow("Webcam Test", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release webcam and close window
cap.release()
cv2.destroyAllWindows()
print("Webcam released.")