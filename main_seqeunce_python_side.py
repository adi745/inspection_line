import cv2
from opcua import Client
import bottle_inspection as bottle_label

# global variables decleration
objects = None #global variable for holding all the OPCUA nodes, global scope
proximity_var = "bottle_detected"
eject_var = "eject_bottle_signal"
exit_var = "exit_script"
session_number_var = "session_number"
plc_var_path = ["0:Objects",
                 "2:DeviceSet", 
                 "4:CODESYS SoftMotion Win V3 x64",
                 "3:Resources",
                 "4:Application", 
                 "3:Programs",
                 "4:quality_control_main",
                 "var"] #saves a spot in the list for updating to the relevant variable we want to read

reference_image_name = "bottle_images//coca_cola_no_label.jpg"
reference_labeled_image_name = "bottle_images//coca_cola_no_label_contour.jpg"

image_name = None
labeled_image_name = None

last_session=0

def connect_opcua():
    
    global objects #declaring objects as global variable so all functions will have access to the outside variable which was declared

    client = Client("opc.tcp://DESKTOP-8GE1BLC:4840") #creating connection
    client.connect() #connecting
    print("OPCUA client is connected to server")

    objects = client.get_root_node() #reading everything on the server
    # print(objects)

def check_sensor():
    plc_var_path[len(plc_var_path)-1] = str("4:") + str(proximity_var)
    var_path = objects.get_child(plc_var_path)
    value = var_path.get_value()
    # if value:
    #     print("Proximity sensor active")
    return value

def activate_eject():
    plc_var_path[len(plc_var_path)-1] = str("4:") + str(eject_var)
    var_path = objects.get_child(plc_var_path)
    var_type = var_path.get_data_type_as_variant_type() #getting the variable type from the opcua server, getting it automatically
    value = var_path.set_value(True, var_type)
    print("Ejection activated")
    
    return var_type

def exit_script():
    plc_var_path[len(plc_var_path)-1] = str("4:") + str(exit_var)
    var_path = objects.get_child(plc_var_path)
    value = var_path.get_value()
    if value:
        print("Script closed")
    return value    

def get_session_number():
    plc_var_path[len(plc_var_path)-1] = str("4:") + str(session_number_var)
    var_path = objects.get_child(plc_var_path)
    value = var_path.get_value()
    
    return value

def grab_frame():
    global image_name, labeled_image_name
    image_name = reference_image_name
    labeled_image_name = reference_labeled_image_name

def classify_camera_image(image_name, labeled_image_name):
    return bottle_label.classify_image(image_name, labeled_image_name)
        

if __name__ == '__main__': #this is how we create a main function in python
    
    connect_opcua() #establishing the communication only once
    
    while(not exit_script()): #running unlimited
        if check_sensor() and last_session != get_session_number():
            if get_session_number == 5:
                last_session=0
            else:
                last_session = get_session_number()
            grab_frame()
            if classify_camera_image(image_name, labeled_image_name):
                activate_eject()
    # print("Alive")