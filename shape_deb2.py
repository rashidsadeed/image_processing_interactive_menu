import numpy as np 
import sys
import cv2

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
    
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(grey_frame, 150, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        epsilon = 0.06 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        x, y, w, h = cv2.boundingRect(approx)
        x_mid = x + int(w / 2)
        y_mid = y - 10
        
        coordinates = (x_mid, y_mid)
        color = (0, 0, 0)
        font = cv2.FONT_HERSHEY_SIMPLEX

        if len(approx) == 3:
            cv2.putText(frame, 'Triangle', coordinates, font, 0.5, color)
            cv2.drawContours(frame, [approx], 0, (0, 0, 0), 2)

        elif len(approx) == 4:
            cv2.putText(frame, 'Quadrilateral', coordinates, font, 0.5, color)
            cv2.drawContours(frame, [approx], 0, (0, 0, 0), 2)

        elif len(approx) == 5:
            cv2.putText(frame, 'Pentagon', coordinates, font, 1, color)
            cv2.drawContours(frame, [approx], 0, (0, 0, 0), 2)

        elif len(approx) == 6:
            cv2.putText(frame, 'Hexagon', coordinates, font, 1, color)
            cv2.drawContours(frame, [approx], 0, (0, 0, 0), 2)

        else:
            cv2.putText(frame, 'Circle', coordinates, font, 1, color)
            cv2.drawContours(frame, [approx], 0, (0, 0, 0), 2)

    cv2.imshow(win_name, frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        source.release()
        cv2.destroyAllWindows()
        break
