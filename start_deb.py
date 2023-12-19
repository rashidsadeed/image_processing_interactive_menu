import cv2
import numpy as np
import sys

class Mask():
    def __init__(self, color, lower_bound, upper_bound, hsv_frame, kernel, imageFrame):
        self.color = color
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.hsv_frame = hsv_frame
        self.imageFrame = imageFrame
        self.result = None

    def color_mask(self):
        cmask = cv2.inRange(self.hsv_frame, self.lower_bound, self.upper_bound)
        cmask = cv2.dilate(cmask, kernel)
        self.result = cmask  # Use the mask directly

s = 0
if len(sys.argv) > 1:
    s = sys.argv[1]

source = cv2.VideoCapture(s)
win_name = "Real-time color and image recognition"
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

while cv2.waitKey(1) != 27:
    has_frame, frame = source.read()
    if not has_frame:
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    kernel = np.ones((5, 5), "uint8")

    # Define masks for different colors
    colors = [
        ("yellow", np.array([35, 94, 68]), np.array([45, 255, 255])),
        ("red", np.array([0, 100, 20]), np.array([10, 255, 255])),
        ("red", np.array([170, 100, 20]), np.array([180, 255, 255])),  # Handling red in the HSV space
        ("green", np.array([25, 52, 72]), np.array([102, 255, 255])),
        ("blue", np.array([94, 80, 2]), np.array([120, 255, 255])),
        ("black", np.array([0, 0, 0]), np.array([180, 255, 30])),
        ("orange", np.array([5, 50, 50]), np.array([15, 255, 255]))
    ]

    # Apply masks and find contours
    for color_name, lower, upper in colors:
        color_mask = Mask(color_name, lower, upper, hsv_frame, kernel, frame)
        color_mask.color_mask()

        contours, _ = cv2.findContours(color_mask.result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 300:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"{color_name.capitalize()} Color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (0, 255, 0))

    cv2.imshow(win_name, frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        source.release()
        cv2.destroyAllWindows()
        break
