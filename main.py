import sys
from classes_funcs import *

#customer order
order = []
name = None
age = None

#welcome note, menu representation and getting customer info
name, age = greating(menu)


#creating customer object
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

#green - red -  blue - yellow
rgb_colors = {"green":(0,255,0), "red":(0,0,255), "blue":(255,0,0), "yellow":(153,255,255)}

while cv2.waitKey(1) != 27:
    has_frame, frame = source.read()
    if not has_frame:
        break
    
    #temporary place holder for color and shape
    color_temp = set([])
    shape_temp = set([])


    #create hue-saturation-value mask for color and gray mask for shape detection
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((5, 5), "uint8")

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
               # order.append(str(f"{color_name}-{shape}"))
               
               #set temp
                color_temp = str(color_name)
                shape_temp = str(shape)
                cv2.imshow(win_name, frame)
                print(color_temp, shape_temp)
                
                ###algorithm
                if customer.get_age() >= 18:#adult
                    if len(order) < 5:
                        print("Please place the menu objects infront of the camera\n")
                        print(f"you have {len(order)} items in the order list. you can order {4-len(order)} more items\n")
                        in_frame = input("is your item in the frame? - YES or NO ").upper()
                        if in_frame == "YES":
                            print(f"\n{color_temp} - {shape_temp}\n")
                            matcher(color_temp, shape_temp, menu, order)

                        
                        #confirms the order of the customer
                        if len(order) >= 2:
                            order_confirm = None
                            while order_confirm not in ["YES", "NO"]:
                                print(f"{65*"*"}\n")
                                order_confirm = str(input(f"your order is {[i.get_name() for i in order]}, do you confirm to finalize? - YES/NO" )).upper()
                                if order_confirm == "YES":
                                    print(f'\n{"*"*65}')
                                    print(f'{"*"*65}\n')
                                    print (f"** your order is \n {[i.get_name() for i in order]} \n")
                                    print (f"** the total price for your order will be {sum(i.get_price() for i in order)}. you can pay at the counter.\n Thanks for dinning at OODR")
                                    print(f'\n{"*"*65}')
                                    print(f'{"*"*65}')
                                    sys.exit(0)
                                    
                                elif order_confirm == "NO":
                                    print("\nplease show your next item to the camera")
                                    continue
                                else:
                                    print("\nPlease respond in YES or NO ")
                else:
                    print("\nWe are sorry, but restaurant policy is to serve to adults only.")
                    sys.exit(0)

          
if cv2.waitKey(1) & 0xFF == ord('q'):
    source.release()
    cv2.destroyAllWindows()
    #break
