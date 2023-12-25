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
                                "Geometry":["Square", "Triangle", "Pentagon","Square",
                                "Triangle", "Pentagon","Square", "Triangle", "Pentagon",
                                "Square", "Triangle", "Pentagon"], 
                                 "price":[1,2,3,4,5,6,7,8,9,10,11,12]})


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

def matcher(color, shape, df):
    if (color in df.Color.values) and (shape in df.Geometry.values):
        name = df[(df.Geometry == shape) & (df.Color == color)].food.values[0]
        if len(order) == 0 or len(order) == 1:
            if df[df.food == name].Category not in ["Main Course", "Starter"]:
                print("the first two items should be a starter and a main course meal, please select accordingly")
                #***this BREAK function should be tested and tried***#
                name = None
        elif color in [i.get_color for i in order]:
            print("you cannot have more than one meal from the same color, please select another meal instead")
            name = None
        
        if name != None:
            category = df[(df.Geometry == shape) & (df.Color == color)].Category.values[0]
            price = df[(df.Geometry == shape) & (df.Color == color)].price.values[0]
            #order confirmation
            confirmatoin = str(input(f"the item is {food}, do you confirm - YES/NO")).capitalize()
            if confirmation == "YES":
                order.append(Meal(name, color, shape, category, price))
            
            elif confirmation == "NO":
                continue

            else:
                print("you have entered an invalid input, please respond in yes or no")

    else:
        print("object shape and color not in menu. please select from the menu items")

####get customer info
name = str(input("What is your name"))
age = int(input("What is your name"))
customer = Customer(name,age)

#Check if the system recognizes a webcam
s = 0
if len(sys.argv) > 1:
    s = sys.argv[1]

#Get live video feed from the webcam
source = cv2.VideoCapture(s)

#Create window for video 
win_name = "Real-time color and shape recognition"
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

#customer order set
order = []

while cv2.waitKey(1) != 27:
    has_frame, frame = source.read()
    if not has_frame:
        break
    
    #create hue-saturation-value mask for color and gray mask for shape detection
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
                cv2.putText(frame, str(color_name), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
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

                cv2.putText(frame, shape, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0))
                order.append(str(f"{color_name}-{shape}"))

                ########algorithm
                if customer.get_age >= 18:#adult
                    while len(order) < 5:
                        print("Please place the menu objects infront of the camera")
                        print("****Note: You have to select at least one main course and one starter!!****")
                        print(f"you have {len(order)} items in the order list. you can orders {4-len(order)} items more")

                        matcher(color_name, shape, menu)
                        
                        #confirms the order of the customer
                        if len(order) >= 2:
                            order_confirm = str(input(f"your order is {order.items()}, do you confirm? - YES/NO")).capitalize()
                            if order_confirm == "YES":
                                print(order)
                                break
                            elif order_confirm == "NO":
                                continue
                            else:
                                print("Please respond in YES or NO")
                        
"""in this section, we had an <else> statement for the possibility that the customer is
underage, in which case the number of items allowed in the order would change, but as of 
the latest description of the project by the teacher, this section is no longer needed"""
                                
    cv2.imshow(win_name, frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        source.release()
        cv2.destroyAllWindows()
        break
