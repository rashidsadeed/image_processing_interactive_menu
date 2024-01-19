import numpy as np
import pandas as pd
import cv2

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
                                "Geometry":["Quadrilateral", "Triangle", "Pentagon","Quadrilateral",
                                "Triangle", "Pentagon","Quadrilateral", "Triangle", "Pentagon",
                                "Quadrilateral", "Triangle", "Pentagon"], 
                                 "price":[30,200,80,100,150,90,180,150,130,160,200,100]})

# Define masks for different colors
colors = [
    ("Yellow", np.array([20, 100, 100]), np.array([40, 255, 255])),
    ("Red", np.array([0, 100, 20]), np.array([10, 255, 255])),
    ("Red", np.array([170, 100, 20]), np.array([180, 255, 255])),  # Handling red in the HSV space
    ("Green", np.array([40, 50, 50]), np.array([90, 255, 255])),
    ("Blue", np.array([90, 50, 50]), np.array([130, 255, 255]))
]

class Customer:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.order = []

    def place_order(self, object):
        self.order.append(object)
    
    def get_age(self):
        return self.age
    
    def get_name(self):
        return self.name

    def get_order_list(self):
        return self.order
    
    def __str__(self):
        return f"""Name:{self.name},
        age:{self.age},
        order: {self.order}"""

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
    
    def get_name(self):
        return self.name
    
    def __str__(self):
        return f"this is {self.name}, is in the {self.color} category, is associated with the {self.shape} shape, and is {self.price}TL"

class ColorMask():
    def __init__(self, color, lower_bound, upper_bound, hsv_frame, kernel, imageFrame):
        self.color = color
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.hsv_frame = hsv_frame
        self.kernel = kernel
        self.imageFrame = imageFrame
        self.result = None

    def color_mask(self):
        cmask = cv2.inRange(self.hsv_frame, self.lower_bound, self.upper_bound)
        cmask = cv2.dilate(cmask, self.kernel)
        self.result = cmask  # Use the mask directly

def matcher(color, shape, df, order):
    if (color in df.Color.values) and (shape in df.Geometry.values):
        name = df[(df.Geometry == shape) & (df.Color == color)].food.values[0]
        if len(order) <= 1:
            if df[df.food == name].Category.values not in ["Main Course", "Starters"]:
                print(f"{65*"*"}\n")
                print("the first two items should be a starter and a main course meal, please select accordingly\n")
                print(f"{65*"*"}\n")
                #***this BREAK function should be tested and tried***#
                name = None
        elif color in [i.get_color for i in order]:
            print("you cannot have more than one meal from the same color, please select another meal instead")
            name = None
        
        if name != None:
            category = df[(df.Geometry == shape) & (df.Color == color)].Category.values[0]
            price = df[(df.Geometry == shape) & (df.Color == color)].price.values[0]
            #order confirmation
            print(f"{65*"*"}\n")
            confirmation = str(input(f"the item is {name}, do you confirm - YES/NO")).upper()
            if confirmation == "YES":
                order.append(Meal(name, color, shape, category, price))
                print(f"{name} has been added to your order\n")
                print(f"{65*"*"}\n")
            
            elif confirmation == "NO":
                print("select something else\n")
                print(f"{65*"*"}\n")

                #continue

            else:
                print("you have entered an invalid input, please respond in yes or no")

    else:
        print("object shape and color not in menu. please select from the menu items")
###implementing a while or for loop here might be helpful

def greating(menu):
    print(menu)
    print(f"\n{"*"*14}OpenCV object detection restaurant{"*"*14}\n")
    name = str(input("Can I please have your name? "))
    age = int(input("\nAnd also your age please? "))
    print(f'\n{"*"*65}')
    print(f'{"*"*65}')
    print(f"""**Welcome to OODR Mr./Ms./Mrs. {name}. This is an interactive order\n**placement system. you can select from our menu above and put the\n**corresponding object infront of the camera to add the item to your order\n{"*"*65}
**Note that you have to select at least one main course and one starter item.\n**We hope you'll have a greate experience at our restaurant, Enjoy!!!!!""")
    print(f'{"*"*65}')
    print(f'{"*"*65}\n')
    return name, age