import cv2

def get_capture():
    # Initialize the camera
    print("1")
    cap = cv2.VideoCapture(0)  # 0 is usually the default camera

    # Try setting the camera brightness to maximum
    print("2")
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 1.0)

    # Capture a single frame
    ret, frame = cap.read()

    # Save the captured image
    if ret:
        cv2.imwrite('current_image.jpg', frame)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

get_capture()