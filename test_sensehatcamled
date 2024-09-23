from picamera2 import Picamera2
import time
import cv2
from sense_hat import SenseHat

# Initialize Picamera2 and Sense HAT
camera = Picamera2()
sense = SenseHat()

# Define colors for Sense HAT LED matrix
green = (0, 255, 0)
red = (255, 0, 0)
nothing = (0, 0, 0)

# Turn the LED matrix to a specific color
def set_led_color(color):
    logo = [color] * 64  # Fill the entire 8x8 matrix with the chosen color
    sense.set_pixels(logo)

# Configure the camera with the settings provided
config = camera.create_still_configuration(
    main={"size": (4056, 3040)},
    lores={"size": (480, 320)},
    display="lores",
    buffer_count=3,
    queue=False
)
camera.configure(config)

try:
    is_live = False  # Start with camera off
    is_recording = False  # Start with not recording

    while True:
        # Display instructions for the user
        print("\nEnter 'l' to turn on camera (green)")
        print("Enter 'r' to capture an image (red)")
        print("Enter 's' to stop camera (green again)")
        print("Enter 'q' to quit the program")

        user_input = input("Your choice: ").strip().lower()

        if user_input == 'l':
            if not is_live:
                print("Turning camera live...")
                camera.set_controls({"ExposureTime": 10000, "AnalogueGain": 5})  # Shutter time and signal boost
                camera.start(show_preview=True)
                set_led_color(green)  # LED turns green for live view
                time.sleep(5)  # Enjoy the live preview for 5 seconds
                is_live = True
            else:
                print("Camera is already live.")

        elif user_input == 'r':
            if is_live:
                print("Capturing image...")
                t_0 = time.monotonic()
                img = camera.capture_array("lores")  # Captures an image
                t_1 = time.monotonic()
                print("Image captured in {} seconds.".format(round(t_1 - t_0, 3)))
                print("Image width x height: {}".format(img.shape[0:2][::-1]))
                set_led_color(red)  # LED turns red for recording
                cv2.imshow("Captured Image", cv2.resize(img, (0, 0), fx=0.25, fy=0.25))  # Resize and display the image
                cv2.waitKey(0)  # Wait for a key press to close the image window
            else:
                print("Please turn on the camera first by pressing 'l'")

        elif user_input == 's':
            if is_live:
                print("Stopping the camera and returning to live mode...")
                camera.close()  # Stop the camera
                set_led_color(green)  # Return LED to green after stopping
                is_live = False
            else:
                print("The camera is not live. Please turn it on by pressing 'l'")

        elif user_input == 'q':
            print("Exiting program...")
            break
        else:
            print("Invalid input. Please enter 'l', 'r', 's', or 'q'.")

finally:
    if is_live:
        camera.close()  # Ensure the camera is closed properly
    sense.clear()  # Clear the LED matrix when done
    cv2.destroyAllWindows()  # Close any open image windows