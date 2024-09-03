import cv2
# creating a function for checking the label on each bottle
 
original_image_color = "bottle_images//coca_cola_no_label.jpg"
image = "bottle_images//coca_cola_no_label.jpg"
labeled_image = "bottle_images//coca_cola_no_label_contour.jpg"

def check_label(contours, original_image_color):

    for cnt in contours:
        epsilon = 0.1 * cv2.arcLength(curve=cnt,closed=True) #Contour perimeter, True stands for if it's closed contour
        approx = cv2.approxPolyDP(curve=cnt, epsilon=epsilon, closed=True)
        area = cv2.contourArea(contour=cnt) #calculates the area of each contour, this way we can eliminate the background noise
        # print(area)
        # print(len(approx))
        if (len(approx)==4) and ((area < 20000.0) and (area > 2440.0)):
            cv2.drawContours(image=original_image_color, contours=cnt, contourIdx=-1, color=(0,255,0), thickness=2) 
            # print(area)
            print("No Issue. Label Detected")
            return 1
        # iterate on every contour 
        #contourIdx=-1 means we should draw all the contours, using the condition on area we eliminate the background noise
        #but we didn't find the label yet --> we will need another functions for that

def classify_image(image_name, labeled_image_name):
    original_image_color = cv2.imread(image_name)
    original_image = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE) 
    # for the adaptive Thresholding we need to read the image as grayscale
    # this is a binary thersholding algorithm --> we will need to adjust it each time so we will use instead adaptive threshold
    # ht, image = cv2.threshold(original_image, 220, 255, cv2.THRESH_BINARY)  #255 the 
    image = cv2.adaptiveThreshold(src=original_image, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=11, C=6) 
    #11 is the area that will be scanned next to the image, 5 is the contrast --> gathered from trial and error, changed the contrast to 6
    # looks better, also the mean looks better than the gaussian
    contours, hier = cv2.findContours(image=image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    #RETR_TREE --> returns in case of one contour which is inside the other a tree form (like label inside a bottle)
    #method is the way to draw these contours, the output contours returns an array of all the contours we are getting
    if (check_label(contours, original_image_color) != 1):
        print("No Label detected. Activate Ejection")
        activate_ejection = 1
    else:
        activate_ejection = 0        

    # cv2.imwrite("bottle_images//beer_pilsner_BINARY.jpg", image)
    cv2.imwrite(labeled_image_name, original_image_color)

    return activate_ejection

if __name__ == '__main__': #this is how we create a main function in python
    classify_image(image, labeled_image)
