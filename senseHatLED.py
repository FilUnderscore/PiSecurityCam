from sense_hat import SenseHat
import time

class SenseHatLED:
    def __init__(self):
        self.sense = SenseHat()
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.yellow = (255, 255, 0)
        self.black = (0, 0, 0)

    def set_led_color(self, color):
        logo = [color] * 64  # Fill the entire 8x8 matrix with the chosen color
        self.sense.set_pixels(logo)

    def set_green(self):
        self.set_led_color(self.green)

    def set_red(self):
        self.set_led_color(self.red)

    def set_yellow(self):
        self.set_led_color(self.yellow)

    def clear(self):
        self.sense.clear()

    def blink_yellow(self):
        """Blink yellow and black for manual video recording"""
        while True:
            self.set_led_color(self.yellow)
            time.sleep(0.5)
            self.set_led_color(self.black)
            time.sleep(0.5)
            # Break when the user wants to stop recording
            if input("Enter 's' to stop manual video recording: ") == 's':
                self.set_green()  # Return to green when stopped
                break