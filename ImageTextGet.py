from openai import OpenAI
import os
import cv2
import UploadImageToCloud as up

client = OpenAI(api_key="Key Here")

def get_text_from_image():
    
    getCapture()
    script_dir = os.path.dirname(__file__)
    image_file = os.path.join(script_dir, 'current_image.jpg')
    up.upload_to_google_cloud(image_file)

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [{
                    "type": "text",
                    "text": "I want to describe this image in detail and also include recognision of all objects and distances between said objects in detail."
                },
                {
                    "type": "image_url",
                    "image_url": "https://storage.googleapis.com/comc_gptapi_robot_images/current_image.jpg"
                }]
            }
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content

def getCapture():
    # Initialize the camera
    cap = cv2.VideoCapture(0)  # 0 is usually the default camera

    # Try setting the camera brightness to maximum
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 1.0)

    # Capture a single frame
    ret, frame = cap.read()

    # Save the captured image
    if ret:
        '''# Convert the image to the HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        # Add 'increase_by' to the V channel
        lim = 255 - 100
        v[v > lim] = 255
        v[v <= lim] += 100

        # Merge channels back and convert to BGR color space
        final_hsv = cv2.merge((h, s, v))
        frame_bright = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

        # Save the postprocessed image
        cv2.imwrite('current_image.jpg', frame_bright)'''
        cv2.imwrite('current_image.jpg', frame)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()