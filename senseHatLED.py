from sense_hat import SenseHat
import time
import threading

class SenseHatLED:
    def __init__(self):
        self.sense = SenseHat()
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.yellow = (255, 255, 0)
        self.black = (0, 0, 0)
        self.blinking = False
        self.blinknig_thread = None

    def set_led_color(self, color):
        logo = [color] * 64  
        self.sense.set_pixels(logo)

    def set_green(self):
        self.set_led_color(self.green)

    def set_red(self):
        self.set_led_color(self.red)

    def set_yellow(self):
        self.set_led_color(self.yellow)

    def clear(self):
        self.sense.clear()
        


