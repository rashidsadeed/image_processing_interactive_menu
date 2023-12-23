import cv2
import numpy as np
import sys
import pandas as pd

menu = pd.DataFrame({"food":["Soup", "Cheese Platter", "Garlic Bread",
                              "Crispy Chicken", "Fihs & Chips", "Omlet",
                                "Meatballs", "Casseroles", "Fajitas",
                                "Souffle", "Tiramisu", "Cheesecake"],
                                "Category":["Starters","Starters",
                                "Starters","Snacks", "Snacks","Snacks",
                                "Main Course","Main Course", "Main Course",
                                "Dessert","Dessert","Dessert"],
                                "Color":["Blue","Blue","Blue","Yellow",
                                "Yellow","Yellow", "Red","Red","Red",
                                "Green","Green","Green"], 
                                "Shape":["Circle","Circle","Circle",
                                "Triangle", "Triangle","Triangle",
                                "Quadrilateral","Quadrilateral",
                                "Quadrilateral", "Pentagon","Pentagon",
                                "Pentagon"]})

class Customer:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.order = []

    def place_order(self, object):
        self.order.append(object)
    
    def get_age(self):
        return self.age
    
    def get_nane(self):
        return self.name

    def get_order_list(self):
        return self.order
    
    def __str__(self):
        return f"Name:{self.name},
        age:{self.age},
        order: {self.order}"

class Meal:
    def __init__(self,name, color,shape, category, price):
        self.color = color
        self.price = price
        self.name = name
        self.shape = shape
        self.category = category

    def get_price(self):
        return self.price

    def get_color(self):
        return self.color
    
    def get_shape(self):
        return self.shape
    
    def get_category(self):
        return self.category
    
    def __str__(self):
        return f"this is {self.name}, is in the {self.color} category, is associated with the {self.shape} shape, and is {self.price}TL"

class ColorMask():
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

soup = Meal("Soup", "Blue", "Circle", "Starters", 50)
cheese_platter = Meal("cheese_platter", "Blue", "Circle","Starters", 150)
garlic_bread = Meal("garlic_bread", "Blue", "Circle","Starters", 80)

crispy_chicken = ("Crispy_chicken", "Yellow", "Triangle","Snacks", 120)
fish_chips = ("Fish & Chips", "Yellow", "Triangle","Snacks", 80)
omlet = ("Omlet", "Yellow", "Triangle","Snacks", 75)

meatballs = Meal("Meatballs", "Red", "Quadrilateral","Main Course", 150)
casseroles = Meal("Casseroles", "Red", "Quadrilateral","Main Course", 120)
fajitas = Meal("Fajitas", "Red", "Quadrilateral","Main Course", 100)

souffle = Meal("Souffle", "Green", "Pentagon", "Dessert", 60)
tiramisu = Meal("Tirasum", "Green", "Pentagon", "Dessert", 80)
cheesecake = Meal("cheesecake", "Green", "Pentagon", "Dessert", 75)





s = 0
if len(sys.argv) > 1:
    s = sys.argv[1]

source = cv2.VideoCapture(s)
win_name = "Real-time color and shape recognition"
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

while cv2.waitKey(1) != 27:
    has_frame, frame = source.read()
    if not has_frame:
        break
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((5, 5), "uint8")

    # Define masks for different colors
    colors = [
        ("yellow", np.array([35, 94, 68]), np.array([45, 255, 255])),
        ("red", np.array([0, 100, 20]), np.array([10, 255, 255])),
        ("red", np.array([170, 100, 20]), np.array([180, 255, 255])),  # Handling red in the HSV space
        ("green", np.array([25, 52, 72]), np.array([102, 255, 255])),
        ("blue", np.array([94, 80, 2]), np.array([120, 255, 255]))
    ]

    # Apply masks for color detection
    for color_name, lower, upper in colors:
        color_mask = ColorMask(color_name, lower, upper, hsv_frame, kernel, frame)
        color_mask.color_mask()

        contours, _ = cv2.findContours(color_mask.result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 300:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"{color_name.capitalize()} Color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (0, 255, 0))

                # Shape detection within the contours
                epsilon = 0.03 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)

                shape = ""
                if len(approx) == 3:
                    shape = 'Triangle'
                elif len(approx) == 4:
                    shape = 'Quadrilateral'
                elif len(approx) == 5:
                    shape = 'Pentagon'
                elif len(approx) == 6:
                    shape = 'Hexagon'
                else:
                    shape = 'Circle'

                cv2.putText(frame, shape, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0))

    cv2.imshow(win_name, frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        source.release()
        cv2.destroyAllWindows()
        break
