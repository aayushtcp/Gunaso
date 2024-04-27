import cv2
import numpy as np

def detect_violence(image):
    # Convert the Django UploadedFile object to numpy array
    nparr = np.fromstring(image.read(), np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate average intensity of the grayscale image
    avg_intensity = np.mean(gray_image)
    
    # Violence Detection
    threshold_violence = 162  # threshold for violence intensity
    is_violent = avg_intensity > threshold_violence

    # Blood Detection
    # Convert image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for red color in HSV
    lower_red = np.array([0, 0, 0])
    upper_red = np.array([136, 8, 8])
    # 255 90 0 

    # Create a mask to isolate red regions
    mask = cv2.inRange(hsv_image, lower_red, upper_red)

    # Count the number of red pixels
    red_pixel_count = cv2.countNonZero(mask)

    # Define a threshold for the number of red pixels to consider as blood
    blood_threshold = 5000  # Adjust this value based on your requirements

    # Determine if there is blood in the image
    has_blood = red_pixel_count > blood_threshold

    print(f"Is violent: {is_violent}")
    print(f"Has blood level: {red_pixel_count}")
    print(f"The avg_intensity is: {avg_intensity}")

    # Determine the final result based on violence and blood detection
    if is_violent or has_blood:
        return True
    else:
        return False
