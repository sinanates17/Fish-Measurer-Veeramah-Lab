import cv2
# Define the reference object length and width (in centimeters)
REF_OBJECT_LENGTH = 1.905
REF_OBJECT_WIDTH = 1.905
cap = cv2.VideoCapture(0) # Use default camera
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
fgbg = cv2.createBackgroundSubtractorMOG2()
# Capture the reference object
_, ref_frame = cap.read()
ref_frame = cv2.resize(ref_frame, (500, 500))
ref_gray = cv2.cvtColor(ref_frame, cv2.COLOR_BGR2GRAY)
ref_gray = cv2.GaussianBlur(ref_gray, (5, 5), 0)
ref_threshold = cv2.threshold(ref_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
ref_contours, _ = cv2.findContours(ref_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Sort the contours by the y-coordinate of the top-most point
ref_contours = sorted(ref_contours, key=lambda x: cv2.boundingRect(x)[1])
# Use the first contour as the reference object
if ref_contours:
    ref_contour = ref_contours[0]
    ref_rect = cv2.boundingRect(ref_contour)
    ref_w, ref_h = ref_rect[2], ref_rect[3]
    ref_pixel_length = max(ref_w, ref_h)
    ref_pixel_per_cm = ref_pixel_length / REF_OBJECT_LENGTH
    ref_pixel_per_cm_width = ref_pixel_length / REF_OBJECT_WIDTH
while True:
    ret, frame = cap.read()
    if not ret: # check if the frame was successfully read
        break
    fgmask = fgbg.apply(frame)
    contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # loop over the contours and draw rectangles around the moving objects
    for contour in contours:
        if cv2.contourArea(contour) > 500:
            (x, y, w, h) = cv2.boundingRect(contour)
            aspect_ratio = float(w)/h
            if aspect_ratio > 0.5 and cv2.mean(frame[y:y+h, x: x+w])[0] > 50: # filter out shadows
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # Calculate the length and width of the object of interest
                pixel_length = max(w, h)
                pixel_width = min(w, h)
                if ref_pixel_length and pixel_length and ref_pixel_per_cm and ref_pixel_per_cm_width:
                    length = pixel_length / ref_pixel_per_cm
                    width = pixel_width / ref_pixel_per_cm_width
                    cv2.putText(frame, f”Length: {length:.2f} cm, Width: {width:.2f} cm”, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow(‘frame’, frame)
    if cv2.waitKey(1) == ord(‘q’): # press ‘q’ to exit
        break
cap.release()
cv2.destroyAllWindows()